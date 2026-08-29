from mcp.server import MCPServer

mcp = MCPServer("Company Tools")


@mcp.tool()
def get_company_info() -> str:
    """Get basic company information."""
    return "Company headquarters: Dublin. Employees: 1200."


if __name__ == "__main__":
    mcp.run()