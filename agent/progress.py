"""
Progress Tracking Utilities
===========================

Functions for tracking and displaying progress in Project Emergence.
"""

import json
from pathlib import Path


def count_features(project_dir: Path) -> int:
    """
    Count features in feature_log.json.

    Args:
        project_dir: Directory containing feature_log.json

    Returns:
        Number of features
    """
    feature_log = project_dir / "feature_log.json"

    if not feature_log.exists():
        return 0

    try:
        with open(feature_log, "r") as f:
            data = json.load(f)

        features = data.get("features", [])
        return len(features)
    except (json.JSONDecodeError, IOError):
        return 0


def count_sessions(project_dir: Path) -> int:
    """
    Count sessions in session_log.json.

    Args:
        project_dir: Directory containing session_log.json

    Returns:
        Number of sessions
    """
    session_log = project_dir / "session_log.json"

    if not session_log.exists():
        return 0

    try:
        with open(session_log, "r") as f:
            data = json.load(f)

        sessions = data.get("sessions", [])
        return len(sessions)
    except (json.JSONDecodeError, IOError):
        return 0


def print_session_header(session_num: int, is_seed: bool) -> None:
    """Print a formatted header for the session."""
    session_type = "SEED AGENT" if is_seed else "CONTRIBUTOR AGENT"

    print("\n" + "=" * 70)
    print(f"  SESSION {session_num}: {session_type}")
    print("=" * 70)
    print()


def print_progress_summary(project_dir: Path) -> None:
    """Print a summary of current progress."""
    feature_count = count_features(project_dir)
    session_count = count_sessions(project_dir)

    if feature_count > 0:
        print(f"\nProject status: {feature_count} features across {session_count} sessions")

        # Show encouraging messages at milestones
        if feature_count >= 20:
            print("The project has grown significantly!")
        elif feature_count >= 10:
            print("Nice collection of features emerging.")
        elif feature_count >= 5:
            print("Project is taking shape.")
        else:
            print("Just getting started.")
    else:
        print("\nProject status: Not yet initialized (feature_log.json not created)")
