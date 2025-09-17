import os
from dotenv import load_dotenv
from mcp import StdioServerParameters
from smolagents import ToolCallingAgent, MCPClient, OpenAIServerModel
from gradio_smolagents_ui import GradioUI

load_dotenv()

try:
  mcp_client = MCPClient(server_parameters=StdioServerParameters(
        command=os.getenv("PYTHON_PATH"),
        args=[
          os.getenv("MCP_SERVER_PATH")
        ],
  ))

  tools = mcp_client.get_tools()
  model = OpenAIServerModel(
      model_id="gpt-4.1-2025-04-14",
  )


  agent = ToolCallingAgent(tools=[*tools], model=model, max_steps=3, stream_outputs=True)

  agent.prompt_templates["final_answer"]["post_messages"] = agent.prompt_templates["final_answer"]["post_messages"] + """
  First, identify relevant context products using search_investigations (missions), search_targets (celestial bodies), search_instruments (scientific instruments),
  or search_instrument_hosts (spacecraft/platforms) based on the user's query. Second, use the URNs from these context products to call search_collections 
  with appropriate filters to find actual data collections. Use get_product for detailed information about specific products when needed.
  """

  agent.prompt_templates["system_prompt"] = agent.prompt_templates["system_prompt"] + """

# Info. on interacting with the PDS MCP server

This MCP server provides access to NASA's Planetary Data System (PDS) Registry API. The NASA PDS is a collection of XML files following
the PDS4 standard and are organized into three hierarchical levels: bundles, collections, and observationals, in that order. 
Observationals are the "labels" or metadata for actual NASA data. Every PDS4 file is associated by a unique URN identifier 
(ex. urn:nasa:pds:context:investigation:mission.juno is the URN for the Juno Mission).

Present all search results with clear titles, descriptions, and displayed URN identifiers. 
Organize results with section headers and include key metadata (missions, targets, instruments, dates, access URLs). 
Always conclude by proposing 3-5 specific next steps for the user, such as refining searches by specific instruments/targets,
exploring detailed product information, or expanding to related missions/datasets. Format these as numbered choices asking 
"What would you like to do next?" to guide continued exploration of the PDS.
"""

  
  demo = GradioUI(agent, reset_agent_memory=False, enable_api_key_input=True)
  demo.launch()
finally:
  mcp_client.disconnect()