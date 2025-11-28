"""
Agent Session Logic
===================

Core agent interaction functions for Project Emergence.
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from claude_agent_sdk import ClaudeSDKClient

from client import create_client
from progress import print_session_header, print_progress_summary
from prompts import get_seed_prompt, get_contributor_prompt


# Configuration
AUTO_CONTINUE_DELAY_SECONDS = 3


def get_next_session_id(project_dir: Path) -> int:
    """Get the next session ID from session_log.json."""
    session_log_path = project_dir / "session_log.json"
    if session_log_path.exists():
        data = json.loads(session_log_path.read_text())
        if data.get("sessions"):
            return max(s["id"] for s in data["sessions"]) + 1
    return 1


def log_session_start(project_dir: Path, session_id: int, session_type: str) -> datetime:
    """Log the start of a session. Returns the start time."""
    start_time = datetime.now(timezone.utc)

    session_log_path = project_dir / "session_log.json"
    if session_log_path.exists():
        data = json.loads(session_log_path.read_text())
    else:
        data = {"sessions": []}

    # Add session entry (agent will fill in agent_report)
    data["sessions"].append({
        "id": session_id,
        "started_at": start_time.isoformat(),
        "ended_at": None,
        "type": session_type,
        "duration_seconds": None,
        "agent_report": None  # Agent fills this in
    })

    session_log_path.write_text(json.dumps(data, indent=2))
    return start_time


def log_session_end(project_dir: Path, session_id: int, start_time: datetime) -> None:
    """Log the end of a session with duration."""
    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()

    session_log_path = project_dir / "session_log.json"
    if session_log_path.exists():
        data = json.loads(session_log_path.read_text())
        for session in data["sessions"]:
            if session["id"] == session_id:
                session["ended_at"] = end_time.isoformat()
                session["duration_seconds"] = int(duration)
                break
        session_log_path.write_text(json.dumps(data, indent=2))


async def run_agent_session(
    client: ClaudeSDKClient,
    message: str,
    project_dir: Path,
) -> tuple[str, str]:
    """
    Run a single agent session using Claude Agent SDK.

    Args:
        client: Claude SDK client
        message: The prompt to send
        project_dir: Project directory path

    Returns:
        (status, response_text) where status is:
        - "continue" if agent should continue working
        - "error" if an error occurred
    """
    print("Sending prompt to Claude Agent SDK...\n")

    try:
        # Send the query
        await client.query(message)

        # Collect response text and show tool use
        response_text = ""
        async for msg in client.receive_response():
            msg_type = type(msg).__name__

            # Handle AssistantMessage (text and tool use)
            if msg_type == "AssistantMessage" and hasattr(msg, "content"):
                for block in msg.content:
                    block_type = type(block).__name__

                    if block_type == "TextBlock" and hasattr(block, "text"):
                        response_text += block.text
                        print(block.text, end="", flush=True)
                    elif block_type == "ToolUseBlock" and hasattr(block, "name"):
                        print(f"\n[Tool: {block.name}]", flush=True)
                        if hasattr(block, "input"):
                            input_str = str(block.input)
                            if len(input_str) > 200:
                                print(f"   Input: {input_str[:200]}...", flush=True)
                            else:
                                print(f"   Input: {input_str}", flush=True)

            # Handle UserMessage (tool results)
            elif msg_type == "UserMessage" and hasattr(msg, "content"):
                for block in msg.content:
                    block_type = type(block).__name__

                    if block_type == "ToolResultBlock":
                        result_content = getattr(block, "content", "")
                        is_error = getattr(block, "is_error", False)

                        # Check if command was blocked by security hook
                        if "blocked" in str(result_content).lower():
                            print(f"   [BLOCKED] {result_content}", flush=True)
                        elif is_error:
                            # Show errors (truncated)
                            error_str = str(result_content)[:500]
                            print(f"   [Error] {error_str}", flush=True)
                        else:
                            # Tool succeeded - just show brief confirmation
                            print("   [Done]", flush=True)

        print("\n" + "-" * 70 + "\n")
        return "continue", response_text

    except Exception as e:
        print(f"Error during agent session: {e}")
        return "error", str(e)


async def run_autonomous_agent(
    project_dir: Path,
    model: str,
    max_iterations: Optional[int] = None,
) -> None:
    """
    Run the autonomous agent loop.

    Args:
        project_dir: Directory for the project
        model: Claude model to use
        max_iterations: Maximum number of iterations (None for unlimited)
    """
    print("\n" + "=" * 70)
    print("  PROJECT EMERGENCE")
    print("  An experiment in autonomous agent creativity")
    print("=" * 70)
    print(f"\nProject directory: {project_dir}")
    print(f"Model: {model}")
    if max_iterations:
        print(f"Max iterations: {max_iterations}")
    else:
        print("Max iterations: Unlimited (will run until stopped)")
    print()

    # Check if this is a fresh start or continuation
    feature_log = project_dir / "feature_log.json"
    is_first_run = not feature_log.exists()

    if is_first_run:
        print("Fresh start - seed agent will choose what to build")
        print()
        print("=" * 70)
        print("  NOTE: First session takes 10-20+ minutes!")
        print("  The seed agent is deciding what to build and setting up.")
        print("  This may appear to hang - it's working. Watch for [Tool: ...] output.")
        print("=" * 70)
        print()
    else:
        print("Continuing existing project")
        print_progress_summary(project_dir)

    # Main loop
    iteration = 0

    while True:
        iteration += 1

        # Check max iterations
        if max_iterations and iteration > max_iterations:
            print(f"\nReached max iterations ({max_iterations})")
            print("To continue, run the script again without --max-iterations")
            break

        # Determine session type and get next session ID
        session_type = "seed" if is_first_run else "contributor"
        session_id = get_next_session_id(project_dir)

        # Print session header
        print_session_header(iteration, is_first_run)

        # Log session start (harness tracking)
        start_time = log_session_start(project_dir, session_id, session_type)

        # Create client (fresh context)
        client = create_client(project_dir, model)

        # Choose prompt based on session type
        if is_first_run:
            prompt = get_seed_prompt()
            is_first_run = False  # Only use seed prompt once
        else:
            prompt = get_contributor_prompt()

        # Run session with async context manager
        async with client:
            status, response = await run_agent_session(client, prompt, project_dir)

        # Log session end (harness tracking)
        log_session_end(project_dir, session_id, start_time)

        # Handle status
        if status == "continue":
            print(f"\nAgent will auto-continue in {AUTO_CONTINUE_DELAY_SECONDS}s...")
            print_progress_summary(project_dir)
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        elif status == "error":
            print("\nSession encountered an error")
            print("Will retry with a fresh session...")
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        # Small delay between sessions
        if max_iterations is None or iteration < max_iterations:
            print("\nPreparing next session...\n")
            await asyncio.sleep(1)

    # Final summary
    print("\n" + "=" * 70)
    print("  SESSION COMPLETE")
    print("=" * 70)
    print(f"\nProject directory: {project_dir}")
    print_progress_summary(project_dir)

    # Print instructions for running the generated application
    print("\n" + "-" * 70)
    print("  TO RUN THE GENERATED APPLICATION:")
    print("-" * 70)
    print(f"\n  cd {project_dir.resolve()}")
    print("  ./init.sh           # Run the setup script")
    print("-" * 70)

    print("\nDone!")
