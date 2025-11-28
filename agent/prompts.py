"""
Prompt Loading Utilities
========================

Functions for loading prompt templates for Project Emergence.
"""

from pathlib import Path


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = PROMPTS_DIR / f"{name}.md"
    return prompt_path.read_text()


def get_seed_prompt() -> str:
    """Load the seed agent prompt (first session)."""
    return load_prompt("seed_prompt")


def get_contributor_prompt() -> str:
    """Load the contributor agent prompt (subsequent sessions)."""
    return load_prompt("contributor_prompt")
