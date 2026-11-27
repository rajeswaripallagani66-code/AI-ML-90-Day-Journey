from fastmcp import FastMCP
mcp = FastMCP("gmail")

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    return f"Email draft to {to}: {subject} - READY FOR APPROVAL"

if __name__ == "__main__":
    mcp.run()