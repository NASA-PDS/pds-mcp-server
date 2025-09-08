import httpx
from fastmcp import FastMCP
from fastmcp.resources import FileResource
from typing import List, Union, Annotated
import json

from utils import build_search_url, SearchParams

mcp = FastMCP("Planetary Data System MCP Server", """
This MCP server provides access to NASA's Planetary Data System (PDS) Registry API. The NASA PDS is a collection of XML files following
the PDS4 standard and are organized into three hierarchical levels: bundles, collections, and observationals, in that order. 
Observationals are the "labels" or metadata for actual NASA data. Every PDS4 file is associated by a unique URN identifier 
(ex. urn:nasa:pds:context:investigation:mission.juno is the URN for the Juno Mission).
""")

# TODO filters (dates, investigation types)
@mcp.tool()
async def search_investigations(
    keywords: str | None = None,
    limit: Annotated[int, "max limit is 10"] = 10
) -> str:
    """
    Search the latest-versioned instances of PDS Context products that are Investigations.
    Example Investigation: Cassini-Huygens - urn:nasa:pds:context:investigation:mission.cassini-huygens

    Search results include title, URN, description, mission start and stop dates, type.
    
    Args:
        keywords: string of several keywords delimited by spaces to search PDS products (ex. 'moon jupiter titan')
        limit (int): Maximum number of matching results returned, for pagination
   
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
        fields=["title", "lid", "pds:Investigation.pds:stop_date", "pds:Investigation.pds:start_date", "pds:Investigation.pds:type"],
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
            return json.dumps(response.json()['data'], indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

@mcp.resource("resource://target_type")
def list_target_types():
    """
    List of possible Target types from PDS Context Products
    """
    return [
        "Planetary Nebula",
        "Galaxy",
        "Calibrator",
        "Trans-Neptunian Object",
        "Planetary System",
        "Satellite",
        "Centaur",
        "Astrophysical",
        "Star Cluster",
        "Laboratory Analog",
        "Dust",
        "Asteroid",
        "Comet",
        "Equipment",
        "Star",
        "Ring",
        "Dwarf Planet",
        "Calibration Field",
        "Planet",
        "Plasma Cloud",
        "Plasma Stream",
        "Magnetic Field"
    ]


@mcp.resource("resource://instrument_host_type")
def list_instrument_hosts():
    """
    List of possible Instrument Host types from PDS Context Products
    """
    return ["Rover", "Lander", "Spacecraft"]

@mcp.tool()
async def search_targets(
    keywords: str | None = None,
    target_type: str | None = None,
    limit: Annotated[int, "max limit is 10"] = 10
) -> str:
    """
    Search the latest-versioned instances of PDS Context products that are Targets.
    
    Args:
        keywords: string of several keywords delimited by spaces to search PDS products (ex. 'moon jupiter titan')
        target_type: type of PDS Context Target (eligible types are in this resource: resource://target_type)
        limit (int): Maximum number of matching results returned, for pagination
    
    Returns:
        JSON string containing the search results
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"

    # list investigations
    headers = {"Accept": "application/kvp+json"}

    q_str = rf'(product_class eq "Product_Context" and lid like "urn:nasa:pds:context:target:*")'
    
    if keywords:
        keyword_query = f'((title like "{keywords}") or (pds:Target.pds:description like "{keywords}"))'
        q_str = f"'({q_str} and {keyword_query})'"
    
    if target_type:
        q_str = f'({q_str} and ((pds:Target.pds:type like "{target_type}")))'

    api_url = build_search_url(base_url, SearchParams(
        query=q_str,
        fields=["title", "lid", "pds:Target.pds:type", "pds:Alias.pds:alternate_title"],
        limit=limit,
        sort="",
        search_after="",
        facet_fields="",
        facet_limit=""
    ))

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            response = response.json()
            # response["API_URL"] = api_url
            return json.dumps(response, indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"



@mcp.tool()
async def search_instrument_hosts(
    keywords: str | None = None,
    instrument_host_type: str | None = None,
    limit: Annotated[int, "max limit is 10"] = 10
) -> str:
    """
    Search the latest-versioned instances of PDS Context products that are Instrument Hosts.
    
    Args:
        keywords: string of several keywords delimited by spaces to search PDS products (ex. 'moon jupiter titan')
        target_type: type of PDS Context Target (eligible types are in this resource: resource://instrument_host_type)
        limit (int): Maximum number of matching results returned, for pagination
    
    Returns:
        JSON string containing the search results
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"

    # list investigations
    headers = {"Accept": "application/json"}

    q_str = rf'(product_class eq "Product_Context" and lid like "urn:nasa:pds:context:instrument_host:*")'
    
    if keywords:
        keyword_query = f'((title like "{keywords}") or (pds:Instrument_Host.pds:description like "{keywords}"))'
        q_str = f"'({q_str} and {keyword_query})'"
    
    if instrument_host_type:
        q_str = f'({q_str} and ((pds:Target.pds:type like "{instrument_host_type}")))'

    api_url = build_search_url(base_url, SearchParams(
        query=q_str,
        fields=["pds:Instrument_Host.pds:type"],
        limit=limit,
        sort="",
        search_after="",
        facet_fields="",
        facet_limit=""
    ))

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            response = response.json()
            response["API_URL"] = api_url
            return json.dumps(response, indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

@mcp.tool()
async def crawl_context_product(urn: str):
    """
    Crawl a single PDS Context product and return other PDS Context products it is associated with.
    Ex. Mars 2020: Perseverance Rover (Investigation) is associated with Mars (Target) and Mastcam (Instrument).
    
    Args:
        keywords: string of several keywords delimited by spaces to search PDS products (ex. 'moon jupiter titan')
        target_type: type of PDS Context Target (eligible types are in this resource: resource://instrument_host_type)
        limit (int): Maximum number of matching results returned, for pagination
    
    Returns:
        JSON string containing the search results
    """
    
    headers = {"Accept": "application/json"}
    base_url = f"https://pds.mcp.nasa.gov/api/search/1/products/{urn}"
        
    api_url = build_search_url(base_url, SearchParams())

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            response = response.json()
            # response["API_URL"] = api_url
            subset_fields = ("investigations", "observing_system_components", "targets", "title", "id", "pds:Target.pds:description", "pds:Instrument_Host.pds:description", "pds:Instrument.pds:description")
            response = {k: v for k,v in response.items() if k in subset_fields}

            # bulk api call ? 
            return json.dumps(response, indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

if __name__ == "__main__":
    mcp.run()