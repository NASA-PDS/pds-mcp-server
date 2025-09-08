import gradio as gr
import os
from dotenv import load_dotenv
from mcp import StdioServerParameters
from smolagents import InferenceClientModel, CodeAgent, ToolCallingAgent, ToolCollection, MCPClient, OpenAIServerModel
import json

load_dotenv()

# with MCPClient(server_parameters=StdioServerParameters(
#       command=os.getenv("PYTHON_PATH"),
#       args=[
#         os.getenv("MCP_SERVER_PATH")
#       ],
# )) as tools:
#     # Tools from the remote server are available
#     print("\n".join(f"{t.name}: {t.description}" for t in tools))
try:
  mcp_client = MCPClient(server_parameters=StdioServerParameters(
        command=os.getenv("PYTHON_PATH"),
        args=[
          os.getenv("MCP_SERVER_PATH")
        ],
  ))

  tools = mcp_client.get_tools()

  # model = InferenceClientModel(token=os.getenv("HF_TOKEN"))
  model = OpenAIServerModel(
      model_id="gpt-5",  # or "gpt-3.5-turbo" for cheaper option
      api_key=os.getenv("OPENAI_API_KEY")
  )


  search_results = {"search_results": {}}

  def my_callback(step_info, agent=None):
    # print(f"Step {step_info.step_number} completed!")
    # print(f"Tool calls: {step_info.tool_calls}")
    # print(f"Observations: {step_info.observations}")
    global search_results
    
    # Check if this step has tool calls
    if step_info.tool_calls:
        for tool_call in step_info.tool_calls:
            # Check if the tool call is for search_investigations
            if tool_call.name == "search_investigations":
                print(f"Found search_investigations tool call!")
                print(f"Arguments: {tool_call.arguments}")
                
                # Extract search results from observations
                if step_info.observations:
                    try:
                        # The observations contain the search results
                        # Parse the JSON results if they're in the observations
                        observations_text = step_info.observations
                        try:
                            
                            results = json.loads(observations_text)
                              # print(f"Results: {results}")
                              # print(f"Captured {len(results.get('data', []))} search results")
                            for result in results:
                              search_results["search_results"][result["lid"]] = result 
                        except json.JSONDecodeError:
                            # If JSON parsing fails, store the raw observations
                            print(f"JSON parsing failed for {observations_text}")
                    except Exception as e:
                        print(f"Error processing search results: {e}")
                print("Search results", search_results)
                            



  agent = ToolCallingAgent(tools=[*tools], model=model, max_steps=3, step_callbacks=[my_callback])

  demo = gr.ChatInterface(
      fn=lambda message, history: str(agent.run(message)),
      type="messages",
      examples=["Tell me about investigations related to the Moon"],
      title="Agent with MCP Tools",
      description="This is a simple agent that uses MCP tools to answer questions."
  )

  demo.launch()
finally:
  mcp_client.disconnect()