import httpx
import requests
from fastmcp import FastMCP
from typing import Union
import json

from utils import build_search_url, SearchParams, clean_urn

mcp = FastMCP("Planetary Data System MCP Server", """
This MCP server provides access to NASA's Planetary Data System (PDS) Registry API. The NASA PDS is a collection of XML files following
the PDS4 standard and are organized into three hierarchical levels: bundles, collections, and observationals, in that order. 
Observationals are the "labels" or metadata for actual NASA data. Every PDS4 file is associated by a unique URN identifier 
(ex. urn:nasa:pds:context:investigation:mission.juno is the URN for the Juno Mission).
""")

@mcp.tool()
async def search_investigations(
    keywords: str | None = "",
    limit: int = 10
) -> str:
    """
    Search PDS Context products that are Investigations (missions/projects).
    
    Investigations are organized missions or projects that collect scientific data.
    Example: Cassini-Huygens - urn:nasa:pds:context:investigation:mission.cassini-huygens
    
    Use for queries about space missions, mission timelines, or finding missions that studied specific targets.
    
    Args:
        keywords (str): Space-delimited search terms (e.g. 'mars rover', 'jupiter cassini')
        limit (int): Max results (default 10)
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
        fields=["title", "lid", "pds:Investigation.pds:stop_date", "pds:Investigation.pds:start_date", "pds:Investigation.pds:type", "ops:Label_File_Info.ops:file_ref"],
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
    List of types of Targets
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
    List of types of Instrument Hosts
    """
    return ["Rover", "Lander", "Spacecraft"]

@mcp.resource("resource://instrument_type")
def list_instruments():
    """
    List of types of Instruments
    """
    return ["Energetic Particle Detector", "Plasma Analyzer", "Regolith Properties", "Spectrograph", "Imager", "Atmospheric Sciences", "Spectrometer", "Radio-Radar", "Ultraviolet Spectrometer", "Small Bodies Sciences", "Dust", "Particle Detector", "Photometer", "Polarimeter", "Plasma Wave Spectrometer"]

@mcp.resource("resource://investigation_type")
def list_investigation_type():
    """
    List of types of Investigations
    """
    return ["Field Campaign", "Other Investigation", "Individual Investigation", "Mission", "Observing Campaign"]

@mcp.tool()
async def search_targets(
    keywords: str | None = "",
    target_type: str | None  = "",
    limit: int = 10
) -> str:
    """
    Search PDS Context products that are Targets (celestial bodies, phenomena).
    
    Targets are objects of scientific study: planets, moons, asteroids, comets, etc.
    Example: Mars - urn:nasa:pds:context:target:planet.mars
    
    Use for queries about specific celestial bodies, finding targets by type, or targets studied by missions.
    
    Args:
        keywords (str): Space-delimited search terms (e.g. 'jupiter moon', 'asteroid belt')
        target_type (str): Filter by type (found in resource://target_type)
        limit (int): Max results (default 10)
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
    keywords: str | None = "",
    instrument_host_type: str | None = "",
    limit: int = 10
) -> str:
    """
    Search PDS Context products that are Instrument Hosts (spacecraft, rovers, telescopes).
    
    Instrument Hosts are platforms that carry scientific instruments: spacecraft, rovers, landers, telescopes.
    Example: Cassini Orbiter - urn:nasa:pds:context:instrument_host:spacecraft.cassini
    
    Use for queries about specific spacecraft, rovers, or platforms that carry instruments.
    
    Args:
        keywords (str): Space-delimited search terms (e.g. 'mars rover', 'voyager spacecraft')
        instrument_host_type (str): Filter by type (found in resource://instrument_host_type)
        limit (int): Max results (default 10)
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"

    # list investigations
    headers = {"Accept": "application/json"}

    q_str = rf'(product_class eq "Product_Context" and lid like "urn:nasa:pds:context:instrument_host:*")'
    
    if keywords:
        keyword_query = f'((title like "{keywords}") or (pds:Instrument_Host.pds:description like "{keywords}"))'
        q_str = f"'({q_str} and {keyword_query})'"
    
    if instrument_host_type:
        q_str = f'({q_str} and ((pds:Instrument_Host.pds:type like "{instrument_host_type}")))'

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
            # response["API_URL"] = api_url
            return json.dumps(response, indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"


@mcp.tool()
async def search_instruments(
    keywords: str | None = "",
    instrument_type: str | None = "",
    limit: int = 10
) -> str:
    """
    Search the latest-versioned instances of PDS Context products that are Instruments.
    
    Instruments are scientific devices (cameras, spectrometers, etc.) used on spacecraft to collect data.
    Example: Cassini RADAR - urn:nasa:pds:context:instrument:radar.cassini
    
    Use for queries about specific instruments, instrument types, or instruments on missions/spacecraft.
    
    Args:
        keywords (str): Space-delimited search terms (e.g. 'camera mars', 'spectrometer cassini')
        instrument_type (str): Filter by type (found in resource://instrument_type)
        limit (int): Max results (default 10)
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"

    # list investigations
    headers = {"Accept": "application/json"}

    q_str = r'(product_class eq "Product_Context" and lid like "urn:nasa:pds:context:instrument:*")'
    
    if keywords:
        keyword_query = f'((title like "{keywords}") or (pds:Instrument.pds:description like "{keywords}"))'
        q_str = f"'({q_str} and {keyword_query})'"
    
    if instrument_type:
        q_str = f'({q_str} and ((pds:Instrument.pds:type like "{instrument_type}")))'

    api_url = build_search_url(base_url, SearchParams(
        query=q_str,
        fields=["pds:Instrument.pds:type"],
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
async def crawl_context_product(urn: str):
    """
    Crawl a single PDS Context product and return other PDS Context products it is associated with.
    Ex. Mars 2020: Perseverance Rover (Investigation) is associated with Mars (Target) and Mastcam (Instrument), so it returns Mars and Mastcam.

    WARNING: Takes a long time to run and performs several sequential API calls. Use wisely.
    
    Args:
        keywords: string of several keywords delimited by spaces to search PDS products (ex. 'moon jupiter titan')
        target_type: type of PDS Context Target (eligible types are in this resource: resource://instrument_host_type)
        limit: Maximum number of matching results returned, for pagination
    
    Returns:
        JSON string containing the search results
    """
    
    headers = {"Accept": "application/json"}
    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"

    # Clean the URN to remove version information
    clean_urn_id = clean_urn(urn)
    api_url = base_url+f"/{clean_urn_id}"

    # print(api_url)
    response = requests.get(api_url, headers=headers)
    response = response.json()
    # print(json.dumps(response, indent=2))

    response = {k: v for k,v in response.items() if k in ("investigations", "observing_system_components", "targets", "title", "id")}

    urn_dict = {
        "investigations": {},
        "observing_system_components": {},
        "targets": {}
    }

    if 'investigations' in response:
        for item in response['investigations']:
            urn_dict["investigations"][item['id']] = item['href']
    if 'observing_system_components' in response:
        for item in response['observing_system_components']:
            urn_dict["observing_system_components"][item['id']] = item['href']
    if 'targets' in response:
        for item in response['targets']:
            urn_dict["targets"][item['id']] = item['href']

    # bulk api

    # Create a results dict with the same structure as urn_dict
    results = {
        "investigations": {},
        "observing_system_components": {},
        "targets": {}
    }

    for category in urn_dict:
        for urn_id, href in urn_dict[category].items():
            # print(f"Fetching: {href}")
            resp = requests.get(href, headers={"Accept": "application/kvp+json"})
            if resp.status_code == 200:
                try:
                    # Only keep a subset of keys from the response, e.g., title, description, id, etc.
                    data = resp.json()
                    subset_keys = ["title", "description", "id"]
                    results[category][urn_id] = {k: v for k, v in data.items() if k in subset_keys}
                except Exception as e:
                    print(f"Error decoding JSON for {href}: {e}")
            else:
                print(f"Failed to fetch {href}: {resp.status_code}")

    return json.dumps(results, indent=2)

@mcp.tool()
async def search_collections(
    ref_lid_instrument: str | None = "",
    ref_lid_target: str | None = "",
    ref_lid_instrument_host: str | None  = "",
    ref_lid_investigation: str | None = "",
    limit: int = 10
) -> str:
    """
    Search PDS data collections filtered by instrument, target, instrument host, or investigation.
    Example: Mars Reconnaissance Orbiter HiRISE data collections targeting Mars.
    
    Args:
        ref_lid_instrument (str): URN identifier for instrument (e.g. urn:nasa:pds:context:instrument:mars2020.mastcamz)
        ref_lid_target (str): URN identifier for target (e.g. urn:nasa:pds:context:target:planet.mars)
        ref_lid_instrument_host (str): URN identifier for instrument host (e.g. urn:nasa:pds:context:instrument_host:spacecraft.mars2020)
        ref_lid_investigation (str): URN identifier for investigation (e.g. urn:nasa:pds:context:investigation:mission.mars2020)
        limit (int): Max results (default 10)
    """

    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"
    headers = {"Accept": "application/kvp+json"}

    # Base query for Product_Collection
    q_str = r'(product_class eq "Product_Collection")'
    
    # Add filters for each provided parameter
    filters = []
    
    if ref_lid_instrument:
        clean_instrument = clean_urn(ref_lid_instrument)
        filters.append(f'(ref_lid_instrument eq "{clean_instrument}")')
    
    if ref_lid_target:
        clean_target = clean_urn(ref_lid_target)
        filters.append(f'(ref_lid_target eq "{clean_target}")')
    
    if ref_lid_instrument_host:
        clean_host = clean_urn(ref_lid_instrument_host)
        filters.append(f'(ref_lid_instrument_host eq "{clean_host}")')
    
    if ref_lid_investigation:
        clean_investigation = clean_urn(ref_lid_investigation)
        filters.append(f'(ref_lid_investigation eq "{clean_investigation}")')
    
    # Combine all filters
    if filters:
        q_str = f'({q_str} and {" and ".join(filters)})'

    api_url = build_search_url(base_url, SearchParams(
        query=q_str,
        fields=["title", "lid", "ref_lid_instrument", "ref_lid_target", "ref_lid_instrument_host", "ref_lid_investigation", "ops:Label_File_Info.ops:file_ref"],
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
            data = response.json()['data']
            for item in data:
                if 'ops:Label_File_Info.ops:file_ref' in item:
                    file_ref = item['ops:Label_File_Info.ops:file_ref']
                    # Remove the filename and go one level up to the directory
                    if file_ref:
                        # Split by '/' and remove the last part (filename), then rejoin
                        path_parts = file_ref.split('/')
                        if len(path_parts) > 1:
                            # Remove the last part (filename) to get the directory
                            directory_path = '/'.join(path_parts[:-1])
                            item['ops:Label_File_Info.ops:file_ref'] = directory_path
            return json.dumps(data, indent=2)
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

@mcp.tool()
async def get_product(urn: str) -> str:
    """
    Get a single PDS product by its URN identifier.
    """
    headers = {"Accept": "application/json"}
    base_url = "https://pds.mcp.nasa.gov/api/search/1/products"
    
    # Clean the URN to remove version information
    clean_urn_id = clean_urn(urn)
    api_url = base_url+f"/{clean_urn_id}"
    response = requests.get(api_url, headers=headers)
    response = response.json()
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    mcp.run()