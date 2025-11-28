# Project Emergence

An experiment in autonomous agent creativity.

## What Is This?

Project Emergence is an experiment to see what happens when you give AI agents creative freedom to build something — with no fixed specification. Instead of telling agents "build X," we ask them "what should we build?"

**The question we're exploring:** What emerges when autonomous agents decide what to create?

## How It Works

This harness implements an **emergent agent pattern**:

1. **Seed Agent** (first run):
   - Chooses what to build (within React constraints)
   - Creates `project_vision.md` describing the direction
   - Sets up project structure and implements starter features
   - Creates `feature_log.json` documenting what exists

2. **Contributor Agents** (subsequent runs):
   - Survey what exists via `feature_log.json` and progress notes
   - **Decide** what to add or extend
   - Implement 1-2 features
   - Document their decisions and reasoning
   - Leave breadcrumbs for the next agent

The project never "completes" — it just grows and evolves.

## The Constraints

Agents have creative freedom within these bounds:
- **Frontend**: Must use React (agents choose tooling: Vite, CRA, Next.js, etc.)
- **Backend**: Optional thin backend allowed (Express, Fastify, etc.)
- **What to build**: Completely open

## Quick Start

### 1. Set Up Environment

```bash
cd ~/Dev/ada-claude-agent-labs/agent
source venv/bin/activate  # or: python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

### 2. Create a Project Directory

```bash
mkdir ~/Dev/ada-claude-agent-labs/project
```

### 3. Run the Agent

```bash
./venv/bin/python autonomous_agent.py ~/Dev/ada-claude-agent-labs/project
```

The first run is the seed agent — it decides what to build. Subsequent runs add features.

### 4. Monitor Progress

```bash
# See what's been built
cat ~/Dev/ada-claude-agent-labs/project/feature_log.json

# Read session decisions
cat ~/Dev/ada-claude-agent-labs/project/session_log.json

# Check agent notes
cat ~/Dev/ada-claude-agent-labs/project/claude-progress.txt
```

## Project Structure

After running, the project directory contains:

```
project/
├── project_vision.md     # What we're building and why
├── feature_log.json      # Record of all features
├── session_log.json      # Timeline of agent sessions
├── claude-progress.txt   # Agent notes
├── init.sh               # Setup script
└── [generated code]      # The actual application
```

## Key Files

| File | Purpose |
|------|---------|
| `project_vision.md` | Agent-created document describing what we're building |
| `feature_log.json` | Structured log of all features (not a checklist!) |
| `session_log.json` | Hybrid log: harness tracks timing, agents report decisions |
| `claude-progress.txt` | Unstructured notes from agents to agents |

## Options

### Model Selection

Default is `claude-opus-4-5-20251101`. Change with:

```bash
./venv/bin/python autonomous_agent.py --model claude-sonnet-4-5-20250929
```

### Iteration Limits

For testing, limit sessions:

```bash
./venv/bin/python autonomous_agent.py --max-iterations 5
```

## Security

The harness uses multi-layered security:

1. **Sandbox** - OS-level bash isolation
2. **Permissions** - File operations restricted to project directory
3. **Command Allowlist** - Only approved bash commands can run (see `security.py`)

## The Experiment

This is based on [Anthropic's long-running agent pattern](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), but flipped:

| Original Pattern | Project Emergence |
|------------------|-------------------|
| Fixed app specification | Open creative freedom |
| `feature_list.json` (tests to pass) | `feature_log.json` (record of what exists) |
| Initializer creates checklist | Seed agent picks direction |
| Coding agent implements next test | Contributor decides what to add |
| "Done" when all tests pass | Never "done" — always growing |

## Requirements

- Python 3.10+
- Claude Code CLI (authenticated)
- Node.js 18+ (for Chrome DevTools MCP)
- Chrome browser (for UI testing)

## Blog Post

This experiment is documented at [link coming soon].

---

*What will your agents build?*
