import gradio as gr
import os
from dotenv import load_dotenv
from mcp import StdioServerParameters
from smolagents import ToolCallingAgent, MCPClient, OpenAIServerModel, GradioUI, PromptTemplates
import json

load_dotenv()

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
      model_id="gpt-4.1-2025-04-14",  # or "gpt-3.5-turbo" for cheaper option # TODO use cheaper model
      api_key=os.getenv("OPENAI_API_KEY"),
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
                            
  # def create_search_result_list():
  #   """Create a scrollable list for search results"""
  #   if not search_results["search_results"]:
  #       return "No search results yet. Ask a question to see results here!"
    
  #   list_items = []
  #   for lid, result in search_results["search_results"].items():
  #       title = result.get('title', 'N/A')
  #       file_ref = result.get('ops:Label_File_Info.ops:file_ref', 'N/A')
        
  #       # Create list item with title and link
  #       list_item = f"""
  #       <div style="
  #           display: flex;
  #           justify-content: space-between;
  #           align-items: center;
  #           padding: 12px 15px;
  #           border-bottom: 1px solid #eee;
  #           background-color: #f8f9fa;
  #           transition: background-color 0.2s;
  #       " onmouseover="this.style.backgroundColor='#e9ecef'" onmouseout="this.style.backgroundColor='#f8f9fa'">
  #           <span style="
  #               flex: 1;
  #               font-size: 14px;
  #               color: #333;
  #               margin-right: 15px;
  #               overflow: hidden;
  #               text-overflow: ellipsis;
  #               white-space: nowrap;
  #           ">{title}</span>
  #           <a href="{file_ref}" target="_blank" style="
  #               color: #007bff;
  #               text-decoration: none;
  #               font-size: 12px;
  #               padding: 6px 12px;
  #               background-color: #007bff;
  #               color: white;
  #               border-radius: 4px;
  #               white-space: nowrap;
  #               transition: background-color 0.2s;
  #           " onmouseover="this.style.backgroundColor='#0056b3'" onmouseout="this.style.backgroundColor='#007bff'">Open</a>
  #       </div>
  #       """
  #       list_items.append(list_item)
    
  #   # Wrap in a scrollable container
  #   scrollable_list = f"""
  #   <div style="
  #       max-height: 400px;
  #       overflow-y: auto;
  #       border: 1px solid #ddd;
  #       border-radius: 8px;
  #       background-color: white;
  #   ">
  #       {"".join(list_items)}
  #   </div>
  #   """
    
  #   return scrollable_list

  # def chat_with_agent(message, history):
  #     """Handle chat interaction and return both response and updated search results"""
  #     try:
  #         response = str(agent.run(message))
  #         # Return both the response and the HTML list
  #         html_list = create_search_result_list()
  #         return response, html_list
  #     except Exception as e:
  #         html_list = create_search_result_list()
  #         return f"Error: {str(e)}", html_list
  agent = ToolCallingAgent(tools=[*tools], model=model, max_steps=3,
  step_callbacks=[my_callback], stream_outputs=True)

  agent.prompt_templates["final_answer"]["post_messages"] = agent.prompt_templates["final_answer"]["post_messages"] + """Return all of the search results to display to the user. 
  In the returned search results, output the URNs (identifiers) as additional information alongside the result.
  You will propose to the user several next steps they can take to continue refining their search within the NASA Planetary Data System and ask them to choose."""

  agent.prompt_templates["system_prompt"] = agent.prompt_templates["system_prompt"] + """This MCP server provides access to NASA's Planetary Data System (PDS) Registry API. The NASA PDS is a collection of XML files following
the PDS4 standard and are organized into three hierarchical levels: bundles, collections, and observationals, in that order. 
Observationals are the "labels" or metadata for actual NASA data. Every PDS4 file is associated by a unique URN identifier 
(ex. urn:nasa:pds:context:investigation:mission.juno is the URN for the Juno Mission).

You will search context products first, using search_investigations, search_targets, search_instruments, search_instrument_hosts. Once you have gathered the URNs
of the context products. Use the URNs to call the search collections tool and return data collections filtered by the chosen context products.
"""

  # Create a custom interface with multiple components
  # with gr.Blocks(title="Agent with MCP Tools") as demo:
      # gr.Markdown("# Agent with MCP Tools")
      # gr.Markdown("This is a simple agent that uses MCP tools to answer questions.")
      
      # with gr.Row():
      #     with gr.Column(scale=2):
      #         # Chat interface
      #         chatbot = gr.Chatbot(height=400)
      #         msg = gr.Textbox(label="Your message", placeholder="Ask about investigations...")
      #         submit_btn = gr.Button("Submit")
              
      #         # Example buttons
      #         gr.Examples(
      #             examples=["Tell me about investigations related to the Moon"],
      #             inputs=msg
      #         )
          
      #     with gr.Column(scale=1):
      #         # Search results display
      #         gr.Markdown("## Search Results")
      #         search_results_display = gr.HTML(
      #             value="No search results yet. Ask a question to see results here!",
      #             label="Search Results"
      #         )
      
      # # Event handlers
      # def user(user_message, history):
      #     return "", history + [[user_message, None]]
      
      # def bot(history):
      #     user_message = history[-1][0]
      #     response, html_boxes = chat_with_agent(user_message, history)
      #     history[-1][1] = response
      #     return history, html_boxes
      
      # # Connect the components
      # msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
      #     bot, chatbot, [chatbot, search_results_display]
      # )
      # submit_btn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
      #     bot, chatbot, [chatbot, search_results_display]
      # )
  
  demo = GradioUI(agent, reset_agent_memory=False)
  demo.launch()
finally:
  mcp_client.disconnect()