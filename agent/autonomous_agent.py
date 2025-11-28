#!/usr/bin/env python3
"""
Project Emergence
=================

An experiment in autonomous agent creativity.

Agents decide what to build, then build it — no fixed specification.

Example Usage:
    python autonomous_agent.py ~/Dev/emergence/project
    python autonomous_agent.py ~/Dev/emergence/project --max-iterations 5
"""

import argparse
import asyncio
from pathlib import Path

from agent import run_autonomous_agent


# Configuration
DEFAULT_MODEL = "claude-opus-4-5-20251101"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Project Emergence: Autonomous Agent Creativity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start a new project (seed agent decides what to build)
  python autonomous_agent.py ~/Dev/emergence/project

  # Continue an existing project (contributor agents add features)
  python autonomous_agent.py ~/Dev/emergence/project

  # Use a different model
  python autonomous_agent.py ~/Dev/emergence/project --model claude-sonnet-4-5-20250929

  # Limit iterations for testing
  python autonomous_agent.py ~/Dev/emergence/project --max-iterations 5

Authentication:
  Uses existing Claude CLI authentication (no API key needed)
        """,
    )

    parser.add_argument(
        "project_dir",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Project directory (default: current directory)",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of agent iterations (default: unlimited)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Ensure project directory exists
    project_dir = args.project_dir.resolve()
    project_dir.mkdir(parents=True, exist_ok=True)

    # Run the agent (uses existing Claude CLI authentication)
    try:
        asyncio.run(
            run_autonomous_agent(
                project_dir=project_dir,
                model=args.model,
                max_iterations=args.max_iterations,
            )
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        print("To resume, run the same command again")
    except Exception as e:
        print(f"\nFatal error: {e}")
        raise


if __name__ == "__main__":
    main()
