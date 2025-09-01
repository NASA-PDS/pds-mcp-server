import httpx
from fastmcp import FastMCP
from fastmcp.resources import FileResource
from typing import List, Union
import aiofiles
import json

from utils import build_search_url, SearchParams

mcp = FastMCP("Planetary Data System MCP Server", """
This MCP server provides access to NASA's Planetary Data System (PDS) Registry API. The NASA PDS is a collection of XML files following
the PDS4 standard and are organized into three hierarchical levels: bundles, collections, and observationals, in that order. 
Observationals are the "labels" or metadata for actual NASA data.
""")

@mcp.tool()
async def search_investigations(
    keywords: list[str] | None,
    limit: int = 10
) -> str:
    """
    Search the latest-versioned instances of PDS Context products that are Investigations.
    
    Args:
        keywords: list of keywords to search PDS products
        limit (int): Maximum number of matching results returned, for pagination (default: 5 unless otherwise specified)
   
    Returns:
        JSON string containing the search results
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"

    # list investigations
    headers = {"Accept": "application/kvp+json"}

    q_str = rf'(product_class eq "Product_Context" and lid like "urn:nasa:pds:context:investigation:*")'

    if keywords:
        keywords_str = " ".join(keywords)
        keyword_query = f'((title like "{keywords_str}") or (description like "{keywords_str}"))'
        q_str = f"'({q_str} and {keyword_query})'"

    api_url = build_search_url(base_url, SearchParams(
        query=q_str,
        fields=["title", "lid", "pds:Investigation.pds:stop_date", "pds:Investigation.pds:start_date", "pds:Investigation.pds:type", "pds:Investigation.pds:description"],
        limit=limit,
        sort="",
        search_after="",
        facet_fields='',
        facet_limit=""
    ))


    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"




if __name__ == "__main__":
    mcp.run()