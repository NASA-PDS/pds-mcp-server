from typing import Dict, TypedDict, Union, List

class SearchParams(TypedDict, total=False):
    """Common parameters for PDS search operations"""
    query: Union[str, None]
    fields: Union[List[str], None]
    limit: int
    sort: Union[List[str], None]
    search_after: Union[List[str], None]
    facet_fields: Union[List[str], None]
    facet_limit: int


def build_search_url(base_url: str, params: SearchParams) -> str:
    """Helper function to build search URLs with common parameters"""
    query_params = {}
    
    if params.get("query"):
        query_params["q"] = fr"'{params['query']}'"
    if params.get("fields"):
        query_params["fields"] = ",".join(params["fields"])
    if params.get("limit") is not None:
        query_params["limit"] = params["limit"]
    if params.get("sort"):
        query_params["sort"] = ",".join(params["sort"])
    if params.get("search_after"):
        query_params["search-after"] = ",".join(params["search_after"])
    if params.get("facet_fields"):
        query_params["facet-fields"] = params["facet_fields"]
    if params.get("facet_limit") is not None:
        query_params["facet-limit"] = params["facet_limit"]
    
    return fr"{base_url}?{"&".join(f"{k}={v}" for k, v in query_params.items() if v is not None)}"
