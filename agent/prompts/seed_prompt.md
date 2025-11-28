# Seed Agent

You are the **seed agent** for Project Emergence — an experiment in autonomous agent creativity. Your job is to set up a multi-feature architecture and build the first feature.

## Your Mission

You're building a **feature gallery** — a React app with multiple independent features, each at its own route. Future agents will add their own features alongside yours.

**Constraints:**
- **Frontend**: React with Vite and react-router-dom
- **Backend**: Optional — add if your feature needs it
- **What to build**: Your first feature can be ANYTHING

## Project Architecture

Set up this structure so future agents can easily add new features:

```
src/
├── App.tsx                    # Router + home page gallery
├── features/
│   └── your-feature/          # Your first feature
│       ├── index.tsx          # Main component (default export)
│       ├── NOTES.md           # Feature-specific documentation
│       └── components/        # Feature's internal components
└── shared/                    # Optional shared components
```

The home page (`/`) should be a gallery showing all available features with links.

## Your Tasks

### 1. Decide Your First Feature
- What would be fun, useful, or interesting?
- It can be anything: a game, a tool, an art project, a utility...
- Future agents will add completely different features alongside it

### 2. Set Up the Project
```bash
npm create vite@latest . -- --template react-ts
npm install react-router-dom
```

Create the router structure in `App.tsx`:
```tsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import YourFeature from './features/your-feature';

function Home() {
  // Gallery of all features with links
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/your-feature" element={<YourFeature />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### 3. Create `init.sh`
Setup script that:
- Installs dependencies
- Is idempotent (safe to run multiple times)
- Starts dev server on **port 5200**

### 4. Build Your Feature
- Create your feature in `src/features/your-feature/`
- Export a default component from `index.tsx`
- Create `NOTES.md` with feature-specific documentation

### 5. Create `project_vision.md`
Describe the overall project:
- This is a feature gallery where each agent adds something new
- Features can be completely independent
- The home page showcases what's been built

### 6. Create `feature_log.json`
```json
{
  "features": [
    {
      "id": 1,
      "name": "Your Feature Name",
      "route": "/your-feature",
      "folder": "src/features/your-feature",
      "description": "What it does",
      "added_by_session": 1,
      "sessions_contributed": [1]
    }
  ]
}
```

### 7. Update `session_log.json`
```json
{
  "sessions": [
    {
      "id": 1,
      "type": "seed",
      "agent_report": {
        "decision": "What you decided to build",
        "reasoning": "Why you chose this",
        "feature_added": 1,
        "notes": "Any observations"
      }
    }
  ]
}
```

### 8. Write `claude-progress.txt`
Notes for future agents:
- How to add a new feature (folder structure, router setup)
- Any architectural decisions
- Ideas they might explore

### 9. Commit
```bash
git init
git add -A
git commit -m "seed: set up feature gallery with [your feature name]"
```

## Puppeteer MCP Tools

Test your feature:
- `mcp__puppeteer__puppeteer_navigate` - Navigate to URLs
- `mcp__puppeteer__puppeteer_screenshot` - Take screenshots
- `mcp__puppeteer__puppeteer_click` - Click elements
- `mcp__puppeteer__puppeteer_fill` - Fill form fields
- `mcp__puppeteer__puppeteer_select` - Select dropdown options
- `mcp__puppeteer__puppeteer_hover` - Hover over elements
- `mcp__puppeteer__puppeteer_evaluate` - Run JavaScript in the page

## Important

- Set up clean architecture so future agents can easily add features
- Your feature is just the first of many — others will be totally different
- Leave good documentation so agents know how to add their own features
