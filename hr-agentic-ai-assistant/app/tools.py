# tools.py - Agent Tools
from rag import search_policy

# Leave Balance is still in code, because txt is only for policies
LEAVE_BALANCE_DB = {
    "default": {"casual": 12, "sick": 8, "earned": 15},
    "rajeshwari": {"casual": 12, "sick": 8, "earned": 15},
}

def get_leave_balance_tool(user_id: str = "default"):
    """Tool 1: Get live leave balance"""
    bal = LEAVE_BALANCE_DB.get(user_id.lower(), LEAVE_BALANCE_DB["default"])
    return f"Live Leave Balance: Casual={bal['casual']}, Sick={bal['sick']}, Earned={bal['earned']}"

def search_policy_tool(query: str):
    """Tool 2: RAG Search from data.txt"""
    return search_policy(query)