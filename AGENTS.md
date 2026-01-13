# AI System Development (AGENTS.md)

This document describes how AI tools and agentic workflows were used to build, refactor, and verify the VigilAI system.

## AI Tools Used
- **Antigravity (Google DeepMind)**: The primary AI agent used for project development, implementation of features, and alignment with evaluation criteria.
- **MCP (Model Context Protocol)**: Used by the agent to interact with the local filesystem, run terminal commands, and perform browser-based verification.

## Development Workflow
The system was developed using an agentic loop:
1. **Planning**: The agent analyzed requirements and created `implementation_plan.md`.
2. **Execution**: The agent modified the codebase to implement features (e.g., video scanning, React state updates).
3. **Verification**: The agent used a browser subagent and terminal tools to verify the functionality and logs.
4. **Correction**: Based on verification results (e.g., CORS errors, missing imports), the agent performed self-correction and iterative improvements.

## MCP Usage
The following MCP-standardized tools were instrumental:
- `run_command`: For building, testing, and running the backend/frontend servers.
- `view_file` / `replace_file_content`: For codebase exploration and modification.
- `browser_subagent`: For end-to-end UI verification and visual confirmation.
- `task_boundary`: For maintaining a structured task UI and summary for the user.

## Prompts & Guidance
Development followed a "Plan-First" approach, ensuring alignment with user requests before jumping into code. Each major change was preceded by a plan review request.
