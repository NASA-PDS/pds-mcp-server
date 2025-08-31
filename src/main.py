from fastmcp import FastMCP
import asyncio
from modular_pds_mcp_server import mcp as modular_pds


# Define main server
main_mcp = FastMCP(name="PDS Registry MCP Server")

# Import subservers
async def setup():
    await main_mcp.import_server(modular_pds, prefix="modular")

# Result: main_mcp now contains prefixed components:
# - Tool: "{prefix}_get_forecast"
# - Resource: "data://{prefix}/cities/supported" 

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run()