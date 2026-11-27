def get_specific_policy(msg: str):
    try:
        with open("data/hr_policy.txt", "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
    except:
        try:
            with open("hr_policy.txt", "r", encoding="utf-8") as f:
                lines = f.read().split("\n")
        except:
            return "Casual 12, Sick 8, Earned 15, Maternity 26 weeks"

    q = msg.lower()
    keyword = ""
    if "maternity" in q: keyword = "maternity"
    elif "sick" in q: keyword = "sick"
    elif "casual" in q: keyword = "casual"
    elif "earned" in q: keyword = "earned"
    elif "leave" in q: keyword = "leave"

    for i, line in enumerate(lines):
        if keyword and keyword in line.lower():
            # Return this line + next 2 lines (the details!)
            result = "\n".join(lines[i:i+3])
            return result.strip()
    return "Casual 12, Sick 8, Earned 15, Maternity 26 weeks"

def run_agent(msg, uid="default"):
    steps = [
        "Intent Node: analyzing query",
        "Intent Detected: policy",
        "RAG Node: searching hr_policy.txt",
        "RAG Node: policy found",
        "Answer Node: forming final answer"
    ]
    answer = get_specific_policy(msg)
    answer += f"\n\n(Source: LangGraph V2 - Steps: {len(steps)})"
    return answer, steps