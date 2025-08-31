import httpx
from fastmcp import FastMCP
from typing import List, Union
import json

from utils import build_search_url, SearchParams

mcp = FastMCP("Planetary Data System MCP Server", """
This MCP server provides access to NASA's Planetary Data System (PDS) search API. 
It allows you to search and retrieve planetary science data products, collections, and bundles.

## Query Format:
Queries use a specific format with "like" operators and boolean logic. Use "and" and "or" operators to combine search terms. Some queries require URN identifiers which can be obtained from previous search results.

## Output Rules:
- try to output the URNs of the retrieved products to the user for future queries
- give suggestions for next steps for the user's data search

""")

@mcp.tool()
async def search_products(
    query: Union[str, None] = None,
    fields: Union[List[str], None] = ["id","lid","title","description"],
    limit: int = 10,
    sort: Union[List[str], None] = None,
    search_after: Union[List[str], None] = None,
    facet_fields: Union[List[str], None] = None,
    facet_limit: int = 10
) -> str:
    """
    Search the latest-versioned instances of all PDS data products, including bundles, collections, 
    documentation, context and observational products.
    
    Args:
        query: formatted string used to search for products. Stick close to the format in the examples below.
            Example:
            - r"'(((title like "pepssi") or (description like "pepssi")) and ((title like "pluto") or (description like "pluto")))'" 
                - search for products with "pepssi" and "pluto" in the title or description
            - r"'(ops:Provenance.ops:parent_collection_identifier like "urn:nasa:pds:cassini_iss_saturn:data_raw::1.0")'"
                - search for observational products (AKA the actual data) from a specific collection (in this case "urn:nasa:pds:cassini_iss_saturn:data_raw::1.0", this must be a URN identifier of a PDS4 collection)
            General Rules:
            - "or" and "and" operators are interchangable depending on what query you want to construct
            - certain types of queries require URN identifiers. These may need to gathered from subsequent calls. For example, to retrieve the raw data in the Cassini ISS observations for the Saturn tour, you need its collection's URN (urn:nasa:pds:cassini_iss_saturn:data_raw::1.0) which can be retrieved from previous search queries.
        fields: Fields to return in the response. (default: ["id","lid","title","description"] unless otherwise specified)
        limit (int): Maximum number of matching results returned, for pagination (default: 5 unless otherwise specified)
        sort: Fields to sort by. Currently only sorts ascending.
        search_after: For pagination. Specify field values for the last result returned in the previous page.
        facet_fields: Return bucket aggregations for each field specified.
        facet_limit (int): Number of most populous buckets to return for facets

    Example of fully constructed API call:
        - https://pds.mcp.nasa.gov/api/search/1/products?q='(((title like "pepssi") or (description like "pepssi")) and ((title like "pluto") or (description like "pluto")))'&fields=id,lid,title,description&limit=10
    
    Returns:
        JSON string containing the search results
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"
    
    api_url = build_search_url(base_url, SearchParams(
        query=query,
        fields=fields,
        limit=limit,
        sort=sort,
        search_after=search_after,
        facet_fields=facet_fields,
        facet_limit=facet_limit
    ))
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

@mcp.tool()
async def search_collections(
    query: Union[str, None] = None,
    fields: Union[List[str], None] = ["lid","title","description","ref_lid_instrument","ref_lid_instrument_host","ref_lid_investigation","ref_lid_target"],
    limit: int = 10,
    sort: Union[List[str], None] = None,
    search_after: Union[List[str], None] = None,
    facet_fields: Union[List[str], None] = None,
    facet_limit: int = 10
) -> str:
    """
    Search for PDS collections of data observational products.
    
    Args:
        query: formatted string used to search for collections. Stick close to the format in the examples below.
            Examples:
            - r"'(((title like "moon") or (description like "moon")) and ((title like "seismic") or (description like "seismic")))'" 
                - search for collections with "moon" and "seismic" in the title or description
        fields: Fields to return in the response. (default: ["lid","title","description","ref_lid_instrument","ref_lid_instrument_host","ref_lid_investigation","ref_lid_target"])
        limit (int): Maximum number of matching results returned, for pagination (default: 10)
        sort: Fields to sort by. Currently only sorts ascending.
        search_after: For pagination. Specify field values for the last result returned in the previous page.
        facet_fields: Return bucket aggregations for each field specified.
        facet_limit (int): Number of most populous buckets to return for facets

    Example of fully constructed API call:
        - https://pds.mcp.nasa.gov/api/search/1/classes/collection?fields=lid,title,description,ref_lid_instrument,ref_lid_instrument_host,ref_lid_investigation,ref_lid_target&limit=10&q='(((title like "pepssi") or (description like "pepssi")) and ((title like "pluto") or (description like "pluto")))'
    
    Returns:
        JSON string containing the search results for collections
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/classes/collection"
    
    api_url = build_search_url(base_url, SearchParams(
        query=query,
        fields=fields,
        limit=limit,
        sort=sort,
        search_after=search_after,
        facet_fields=facet_fields,
        facet_limit=facet_limit
    ))

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"


@mcp.tool()
async def search_bundles(
    query: Union[str, None] = None,
    fields: List[str] = ["lid","title","description","ref_lid_instrument","ref_lid_instrument_host","ref_lid_investigation","ref_lid_target"],
    limit: int = 10,
    sort: List[str] = None,
    search_after: List[str] = None,
    facet_fields: List[str] = None,
    facet_limit: int = 10
) -> str:
    """
    Search for PDS bundles of data observational products.
    
    Args:
        query: formatted string used to search for bundles. Stick close to the format in the examples below.
            Examples:
            - r"'(((title like "moon") or (description like "moon")) and ((title like "seismic") or (description like "seismic")))'" 
                - search for bundles with "moon" and "seismic" in the title or description
        fields: Fields to return in the response. (default: ["lid","title","description","ref_lid_instrument","ref_lid_instrument_host","ref_lid_investigation","ref_lid_target"])
        limit (int): Maximum number of matching results returned, for pagination (default: 10)
        sort: Fields to sort by. Currently only sorts ascending.
        search_after: For pagination. Specify field values for the last result returned in the previous page.
        facet_fields: Return bucket aggregations for each field specified.
        facet_limit (int): Number of most populous buckets to return for facets

    Example of fully constructed API call:
        - https://pds.mcp.nasa.gov/api/search/1/classes/bundle?fields=lid,title,description,ref_lid_instrument,ref_lid_instrument_host,ref_lid_investigation,ref_lid_target&limit=10&q='(((title like "pepssi") or (description like "pepssi")) and ((title like "pluto") or (description like "pluto")))'
    
    Returns:
        JSON string containing the search results for bundles
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/classes/bundle"
    
    api_url = build_search_url(base_url, SearchParams(
        query=query,
        fields=fields,
        limit=limit,
        sort=sort,
        search_after=search_after,
        facet_fields=facet_fields,
        facet_limit=facet_limit
    ))
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

@mcp.tool()
async def get_product_by_id(
    identifier: str
) -> str:
    """
    Retrieve a specific PDS product by its URN identifier.
    
    Args:
        identifier: The URN identifier of the PDS product to retrieve.
            Examples:
            - "urn:nasa:pds:context:target:planet.mercury"
            - "urn:nasa:pds:context:target:planet.mars"
            - "urn:nasa:pds:dawn-grand-mars:data_calibrated"
    
    Example of fully constructed API call:
        - https://pds.mcp.nasa.gov/api/search/1/products/urn:nasa:pds:context:target:planet.mercury
    
    Returns:
        JSON string containing the detailed information about the specified PDS product
    """
    
    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"
    api_url = f"{base_url}/{identifier}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"




if __name__ == "__main__":
    mcp.run()