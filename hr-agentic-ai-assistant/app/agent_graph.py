from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    user_id: str
    query: str
    intent: str
    balance: Optional[str]
    policy: Optional[str]
    approval: Optional[str]
    messages: List[str]
    steps: List[str]
    loops: int

def intent_node(state: AgentState):
    q = state["query"].lower()
    steps = state.get("steps", []) + ["Intent Node: analyzing query"]
    print(f"[LangGraph] Intent Node: {q}")
    if any(w in q for w in ["balance", "left", "remaining", "how many"]):
        intent = "balance"
    elif any(w in q for w in ["book", "apply", "request leave"]):
        intent = "booking"
    elif any(w in q for w in ["email", "send", "manager", "notify"]):
        intent = "email"
    else:
        intent = "policy"
    steps.append(f"Intent Detected: {intent}")
    return {"intent": intent, "steps": steps, "loops": state.get("loops",0)+1}

def rag_node(state: AgentState):
    steps = state["steps"] + ["RAG Node: searching hr_policy.txt"]
    print("[LangGraph] RAG Node running...")
    q = state["query"].lower()
    if "sick" in q:
        policy = "Sick Leave Policy:\n- 8 Sick Leaves per year\n- Medical certificate required if more than 2 days."
    elif "casual" in q:
        policy = "Casual Leave Policy:\n- 12 Casual Leaves per year\n- Max 3 at a time\n- Cannot be carried forward."
    elif "earned" in q:
        policy = "Earned Leave Policy:\n- 15 Earned Leaves per year\n- Can carry forward up to 30 days."
    elif "wfh" in q or "work from home" in q:
        policy = "WFH Policy:\n- 2 days WFH per week allowed\n- Manager approval required."
    else:
        policy = "Casual 12, Sick 8, Earned 15. Ask specific policy."
    steps.append("RAG Node: policy found")
    return {"policy": policy, "steps": steps}

def db_node(state: AgentState):
    steps = state["steps"] + ["DB Node: fetching leave balance"]
    print("[LangGraph] DB Node running...")
    for attempt in range(2):
        try:
            from app.tools import get_leave_balance_tool
            balance = get_leave_balance_tool(state["user_id"])
            steps.append(f"DB Node: success on attempt {attempt+1}")
            return {"balance": balance, "steps": steps}
        except Exception as e:
            print(f"DB Retry {attempt+1} failed: {e}")
            try:
                from tools import get_leave_balance_tool
                balance = get_leave_balance_tool(state["user_id"])
                return {"balance": balance, "steps": steps + [f"DB Node: success on retry {attempt+1}"]}
            except Exception as e2:
                steps.append(f"DB Node: retry {attempt+1} failed")
    return {"balance": "Live Leave Balance: Casual=12, Sick=8, Earned=15 (fallback)", "steps": steps + ["DB Node: fallback used"]}

def booking_node(state: AgentState):
    steps = state["steps"] + ["Booking Node: checking approval"]
    print("[LangGraph] Booking Node running...")
    return {"approval": "Booking Node: Leave request noted. Manager approval required. (Demo)", "steps": steps}

def email_node(state: AgentState):
    steps = state["steps"] + ["Email Node: preparing email"]
    print("[LangGraph] Email Node running...")
    return {"approval": "Email Node: Email draft ready to send to manager. (Demo)", "steps": steps}

def answer_node(state: AgentState):
    steps = state["steps"] + ["Answer Node: forming final answer"]
    print(f"[LangGraph] Answer Node. Steps: {steps}")
    parts = []
    if state.get("policy"): parts.append(state["policy"])
    if state.get("balance"): parts.append(state["balance"])
    if state.get("approval"): parts.append(state["approval"])
    if not parts: parts.append("I can help with leave policy, balance, booking and email.")
    final = "\n\n".join(parts) + f"\n\n(Source: LangGraph V2 - Steps: {len(steps)})"
    return {"messages": [final], "steps": steps}

def route_intent(state: AgentState):
    if state["intent"] == "balance": return "db_node"
    if state["intent"] == "booking": return "booking_node"
    if state["intent"] == "email": return "email_node"
    return "rag_node"

def build_graph():
    g = StateGraph(AgentState)
    g.add_node("intent", intent_node)
    g.add_node("rag_node", rag_node)
    g.add_node("db_node", db_node)
    g.add_node("booking_node", booking_node)
    g.add_node("email_node", email_node)
    g.add_node("answer_node", answer_node)
    g.set_entry_point("intent")
    g.add_conditional_edges("intent", route_intent, {"rag_node": "rag_node", "db_node": "db_node", "booking_node": "booking_node", "email_node": "email_node"})
    g.add_edge("rag_node", "answer_node")
    g.add_edge("db_node", "answer_node")
    g.add_edge("booking_node", "answer_node")
    g.add_edge("email_node", "answer_node")
    g.add_edge("answer_node", END)
    return g.compile()

graph = build_graph()

def run_agent(query: str, user_id: str = "default"):
    print(f"\n=== LangGraph V2 START: {query} ===")
    result = graph.invoke({"user_id": user_id, "query": query, "intent": "", "balance": None, "policy": None, "approval": None, "messages": [], "steps": [], "loops": 0})
    print(f"=== LangGraph V2 STEPS: {result['steps']} ===")
    return result["messages"][-1] if result["messages"] else "No answer", result["steps"]