from fastmcp import FastMCP
mcp = FastMCP("rag")

@mcp.tool()
def search_policy(query: str) -> str:
    with open("hr_policy.txt") as f:
        text = f.read()
    return text[:1000]

if __name__ == "__main__":
    mcp.run()