import asyncio
import json
import os
import sys
from typing import Dict, Any, List

# Add parent directory to path to allow importing from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from toyaikit.mcp.transport import SubprocessMCPTransport
    from toyaikit.mcp.client import MCPClient
    HAS_TOYAIKIT = True
except ImportError:
    HAS_TOYAIKIT = False

async def run_demo():
    print("="*60)
    print("VigilAI LLM AGENT DEMO".center(60))
    print("="*60)
    
    server_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")
    
    if not os.path.exists(server_script):
        print(f"Error: MCP server script not found at {server_script}")
        return

    print(f"[1/3] Starting MCP Server...")
    
    # We'll use a mock client if toyaikit is missing or if we just want to demonstrate the flow
    if not HAS_TOYAIKIT:
        print("\n[NOTE] 'toyaikit' not found. Running in SIMULATION MODE.")
        await simulate_agent_flow()
        return

    # Real MCP interaction if libraries exist
    try:
        transport = SubprocessMCPTransport(server_command=["python", server_script])
        mcp_client = MCPClient(transport)
        mcp_client.full_initialize()
        
        print(f"[2/3] Agent scanning for critical alerts...")
        
        # 1. Fetch alerts
        result = mcp_client.call_tool("get_alerts", {"severity": "critical", "limit": 1})
        alerts = result.get("result", [])
        
        if not alerts:
            print(">>> No critical alerts found. (Try running a Scan in the UI first!)")
            # For demo purposes, we'll "find" a phantom one if none exist
            print(">>> [DEMO MODE] Injecting a mock critical alert for demonstration...")
            alerts = [{
                "id": "demo-alert-123",
                "description": "Weapon detected in Sector 7G",
                "severity": "critical"
            }]

        alert = alerts[0]
        print(f"Found Alert: [{alert['severity'].upper()}] {alert['description']}")
        
        print(f"[3/3] Agent Action: Dispatching Authorities...")
        dispatch_result = mcp_client.call_tool("notify_authorities", {
            "alert_id": alert["id"],
            "department": "Police Control Room"
        })
        
        print(f"\nRESULT: {dispatch_result['message']}")
        print(f"TIMESTAMP: {dispatch_result['timestamp']}")
        
        mcp_client.stop_server()
        
    except Exception as e:
        print(f"\nError connecting to MCP server: {e}")
        print("Falling back to Simulation Mode...")
        await simulate_agent_flow()

async def simulate_agent_flow():
    """Shows the 'Chain of Thought' of what an LLM agent would do."""
    print("\n--- AGENT THOUGHT PROCESS ---")
    await asyncio.sleep(1)
    print("Thought: I need to check if there are any critical security threats.")
    print("Call Tool: get_alerts(severity='critical')")
    await asyncio.sleep(1.5)
    print("Response: Found 1 critical alert - 'Weapon detected in Sector 4'")
    await asyncio.sleep(1)
    print("Thought: This is a critical life-safety issue. I must notify authorities immediately.")
    print("Call Tool: notify_authorities(alert_id='8821-abc', department='Police')")
    await asyncio.sleep(1.5)
    print("\n[MOCK SUCCESS]: Authorities dispatched. Case status: ACTIVE.")

if __name__ == "__main__":
    asyncio.run(run_demo())
