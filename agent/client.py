"""
Claude SDK Client Configuration
===============================

Functions for creating and configuring the Claude Agent SDK client.
"""

import json
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient
from claude_agent_sdk.types import HookMatcher

from security import bash_security_hook


# =============================================================================
# Project Emergence: An experiment in autonomous agent creativity
# =============================================================================
PROJECT_DESCRIPTION = """You are part of Project Emergence, an experiment in autonomous agent creativity.

You have creative freedom to build or extend a React-based application. Each agent session adds to the project - you might be the first (seed) agent deciding what to build, or a later contributor adding features.

Key files to check:
- project_vision.md: What we're building and why
- feature_log.json: What features exist
- claude-progress.txt: Notes from previous agents
- session_log.json: Record of all sessions

Your constraints:
- Must use React for the frontend
- May add a thin backend if needed (Express, Fastify, etc.)
- What to build is up to you (or previous agents)
"""
# =============================================================================


# Chrome DevTools MCP tools for browser automation
DEVTOOLS_TOOLS = [
    "mcp__chrome-devtools__click",
    "mcp__chrome-devtools__fill",
    "mcp__chrome-devtools__fill_form",
    "mcp__chrome-devtools__hover",
    "mcp__chrome-devtools__navigate_page",
    "mcp__chrome-devtools__new_page",
    "mcp__chrome-devtools__list_pages",
    "mcp__chrome-devtools__select_page",
    "mcp__chrome-devtools__close_page",
    "mcp__chrome-devtools__take_screenshot",
    "mcp__chrome-devtools__take_snapshot",
    "mcp__chrome-devtools__press_key",
    "mcp__chrome-devtools__evaluate_script",
    "mcp__chrome-devtools__wait_for",
    "mcp__chrome-devtools__list_console_messages",
    "mcp__chrome-devtools__get_console_message",
    "mcp__chrome-devtools__list_network_requests",
    "mcp__chrome-devtools__get_network_request",
]

# Built-in tools
BUILTIN_TOOLS = [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash",
]


def create_client(project_dir: Path, model: str) -> ClaudeSDKClient:
    """
    Create a Claude Agent SDK client with multi-layered security.

    Uses existing Claude CLI authentication - no API key needed.

    Args:
        project_dir: Directory for the project
        model: Claude model to use

    Returns:
        Configured ClaudeSDKClient

    Security layers (defense in depth):
    1. Sandbox - OS-level bash command isolation prevents filesystem escape
    2. Permissions - File operations restricted to project_dir only
    3. Security hooks - Bash commands validated against an allowlist
       (see security.py for ALLOWED_COMMANDS)
    """
    # Create comprehensive security settings
    # Note: Using relative paths ("./**") restricts access to project directory
    # since cwd is set to project_dir
    security_settings = {
        "sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True},
        "permissions": {
            "defaultMode": "acceptEdits",  # Auto-approve edits within allowed directories
            "allow": [
                # Allow all file operations within the project directory
                "Read(./**)",
                "Write(./**)",
                "Edit(./**)",
                "Glob(./**)",
                "Grep(./**)",
                # Bash permission granted here, but actual commands are validated
                # by the bash_security_hook (see security.py for allowed commands)
                "Bash(*)",
                # Allow Chrome DevTools MCP tools for browser automation
                *DEVTOOLS_TOOLS,
            ],
        },
    }

    # Write settings to a file in the project directory
    settings_file = project_dir / ".claude_settings.json"
    with open(settings_file, "w") as f:
        json.dump(security_settings, f, indent=2)

    print(f"Created security settings at {settings_file}")
    print("   - Sandbox enabled (OS-level bash isolation)")
    print(f"   - Filesystem restricted to: {project_dir.resolve()}")
    print("   - Bash commands restricted to allowlist (see security.py)")
    print("   - MCP servers: chrome-devtools (browser automation)")
    print()

    return ClaudeSDKClient(
        options=ClaudeAgentOptions(
            model=model,
            # Use Claude Code's preset system prompt with project-specific additions
            system_prompt={
                "type": "preset",
                "preset": "claude_code",
                "append": PROJECT_DESCRIPTION,
            },
            # Load project settings (for CLAUDE.md, .claude/settings.json)
            setting_sources=["project"],
            allowed_tools=[
                *BUILTIN_TOOLS,
                *DEVTOOLS_TOOLS,
            ],
            mcp_servers={
                "chrome-devtools": {
                    "command": "npx",
                    "args": ["-y", "chrome-devtools-mcp@latest"],
                }
            },
            hooks={
                "PreToolUse": [
                    HookMatcher(matcher="Bash", hooks=[bash_security_hook]),
                ],
            },
            max_turns=1000,
            cwd=str(project_dir.resolve()),
            settings=str(settings_file.resolve()),  # Use absolute path
        )
    )
