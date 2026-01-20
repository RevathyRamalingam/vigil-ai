import os
import asyncio
import json
from typing import List, Dict, Any

from toyaikit.mcp.transport import SubprocessMCPTransport
from toyaikit.mcp.client import MCPClient
from toyaikit.llm import OpenAIClient
from openai import OpenAI

async def run_llm_mcp_interaction():
    # 1. Configuration
    server_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")
    
    # Check for OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("WARNING: OPENAI_API_KEY not found in environment.")
        print("This script will demonstrate the tool-calling setup but cannot make real LLM calls.")
        print("Please set OPENAI_API_KEY to run the full simulation.")
    
    # 2. Setup MCP Client and Server
    print(f"Starting MCP Server: {server_script}...")
    transport = SubprocessMCPTransport(server_command=["python", server_script])
    mcp_client = MCPClient(transport)
    
    try:
        # Initialize handshake
        print("Initializing MCP Handshake...")
        mcp_client.full_initialize()
        
        # Get available tools
        mcp_tools = mcp_client.get_tools()
        print(f"Available tools from MCP Server: {[t['name'] for t in mcp_tools]}")
        
        if not api_key:
            # Mock interaction if no API key
            print("\n--- Mock Interaction (No API Key) ---")
            print("Prompt: 'Are all cameras working?'")
            print("Action: LLM would choose 'get_camera_status'...")
            result = mcp_client.call_tool("get_camera_status", {})
            print(f"Server Response: {json.dumps(result, indent=2)}")
            return

        # 3. Real LLM Interaction (using OpenAI)
        print("\n--- Starting Real LLM Interaction (OpenAI) ---")
        
        # Direct OpenAI client for more control over tools if needed
        # but we'll try to use Toyaikit's structure
        client = OpenAI(api_key=api_key)
        
        # Format tools for OpenAI
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t["inputSchema"]
                }
            }
            for t in mcp_tools
        ]
        
        prompts = [
            "Are there any critical alerts right now?"
        ]
        
        for prompt in prompts:
            print(f"\nUser: {prompt}")
            
            messages = [
                {"role": "system", "content": "You are the VigilAI Assistant. You have access to real-time surveillance data via tools. Use them to answer questions about cameras and alerts."},
                {"role": "user", "content": prompt}
            ]
            
            # turn-based loop
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=openai_tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            print(f"AI: {response_message.content if response_message.content else '[Thought: Needs to call tools]'}")
            
            # Handle tool calls
            if response_message.tool_calls:
                messages.append(response_message)
                
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"  [Tool Call]: {tool_name}({tool_args})")
                    tool_result = mcp_client.call_tool(tool_name, tool_args)
                    
                    # Convert tool result to string
                    tool_result_str = json.dumps(tool_result)
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_name,
                        "content": tool_result_str,
                    })
                
                # Get final response from LLM
                second_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                )
                print(f"AI (Final): {second_response.choices[0].message.content}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        mcp_client.stop_server()

if __name__ == "__main__":
    asyncio.run(run_llm_mcp_interaction())
