# --- FAKE DB FOR DAY 1 ---
LEAVE_DB = {
    "EMP001": {"casual": 12, "sick": 8, "earned": 15},
    "EMP002": {"casual": 5, "sick": 3, "earned": 10},
}

POLICY_DOCS = [
    "Casual Leave: Employee gets 12 casual leaves per year. Must apply 2 days before.",
    "Sick Leave: Employee gets 8 sick leaves per year. Medical certificate needed if more than 2 days.",
    "Earned Leave: Employee gets 15 earned leaves per year. Can carry forward max 30 days.",
    "Work From Home: Allowed 2 days per week with manager approval.",
    "Working Hours: 9 AM to 6 PM, Monday to Friday.",
]

def get_leave_balance(emp_id: str):
    data = LEAVE_DB.get(emp_id, {"casual": 0, "sick": 0, "earned": 0})
    return f"Leave Balance for {emp_id}: Casual={data['casual']}, Sick={data['sick']}, Earned={data['earned']}"

def search_policy(question: str):
    q = question.lower()
    results = []
    for doc in POLICY_DOCS:
        for word in q.split():
            if len(word) > 3 and word in doc.lower():
                results.append(doc)
                break
    if not results:
        return POLICY_DOCS[:2]
    return results