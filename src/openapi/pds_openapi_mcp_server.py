import httpx
from fastmcp import FastMCP

# # Create an HTTP client for the PDS Registry API
client = httpx.AsyncClient(base_url="https://pds.mcp.nasa.gov/api/search/1")
# Load your OpenAPI spec 
openapi_spec = httpx.get("https://pds.mcp.nasa.gov/api/search/1/api-docs").json()

# Create the MCP server from the OpenAPI spec
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="PDS Registry API Server",
)

if __name__ == "__main__":
    mcp.run()