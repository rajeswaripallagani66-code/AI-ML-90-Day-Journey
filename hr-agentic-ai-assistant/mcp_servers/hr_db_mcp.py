from fastmcp import FastMCP
mcp = FastMCP("hr-db")

@mcp.tool()
def get_balance(user_id: str) -> str:
    return f"Balance for {user_id}: 18 days"

@mcp.tool()
def book_leave(user_id: str, date: str) -> str:
    return f"Leave booked for {user_id} on {date}, pending approval"

if __name__ == "__main__":
    mcp.run()