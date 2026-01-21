# VigilAI LLM Agent Demo Guide

This guide explains how to demonstrate the agentic capabilities of the VigilAI backend using the Model Context Protocol (MCP).

## Prerequisites

1. Ensure the backend is running:
   ```powershell
   cd backend
   python main.py
   ```
2. (Optional) Set your API key if you want real LLM interaction:
   ```powershell
   # Windows
   $env:OPENAI_API_KEY = "your-key-here"
   ```

## Scenario: Automatic Threat Response

The core of the demo is showing how an LLM can "decide" to call tools based on what it finds in the surveillance data.

### Step 1: Trigger a Critical Alert
1. Open the VigilAI Dashboard (http://localhost:5173).
2. Click the **"Scan Now"** button.
3. If your video folder contains a sample that triggers a `critical` threat (like a weapon), the UI will show a red toast notification.
   - *Note: If no critical threat is found, the demo script will inject a mock one for you.*

### Step 2: Run the Agent Demo
Open a new terminal and run:
```powershell
python backend/mcp/demo_agent.py
```

### What to Look For:
- **Live Feed**: The dashboard now features an auto-playing video of a street (using `travel_video_normal.mp4`).
- **Security Aesthetic**: Look for the pulsating red **"REC"** indicator and the grainy noise overlay that gives it a realistic CCTV feel.
- **Scan Interaction**: When you click "Scan Now", the neon scan-line will pass over the live video.
- **Handshake**: The agent connects to the `mcp_server.py`.
- **Discovery**: The agent asks "What tools do I have?" and finds `get_alerts` and `notify_authorities`.
- **Reasoning**: The agent fetches recent critical alerts.
- **Action**: Upon finding a weapon detection, the agent calls `notify_authorities` automatically.

## How it Works (The MCP Part)
The `mcp_server.py` acts as a **bridge**. It doesn't just provide data; it provides **capabilities** (Tools) to the LLM:
1. **Tool Definition**: The server defines `@mcp.tool()` functions.
2. **Standardized Protocol**: Using MCP, the LLM knows exactly how to call these functions without any manual glue code.
3. **Autonomous Loop**: The agent can chain these tools (e.g., Get Alert -> Analyze -> Notify) to solve complex surveillance tasks.
