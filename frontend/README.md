# RailDoot Frontend v2

New React + TypeScript + Vite frontend for the integrated RailDoot backend.

## What changed from the previous frontend

The previous repository already had a React/TypeScript/Vite application with pages for Dashboard, Block Planning, Network, Assets, Analytics, Conflicts, Reports, Alerts, Settings and Weather Replanning, plus reusable corridor and operations components. The new frontend intentionally replaces that larger navigation surface with a focused government-operations workflow:

1. Today's Operations
2. AI Block Planner
3. Corridor View
4. Conflict Management
5. Maintenance Requests
6. Asset Availability
7. Performance

The main workflow is:

Maintenance requests -> AI/ML priority -> candidate windows -> CP-SAT block plan -> conflicts -> officer review -> final plan.

## Visual direction

- White base
- Railway/government blue: #123B67 / #1F5F9B
- Orange accent: rgb(251, 121, 43)
- Thin borders
- Dense but readable tables
- No gradients
- No glassmorphism
- No consumer-app styling
- Human-operated control-room feel

## Run

```bash
npm install
npm run dev
```

The Vite dev server proxies `/api/*` to `http://localhost:8000`.

Start the backend separately:

```bash
uvicorn app.main:app --reload --port 8000
```

If the backend is unavailable, key pages show sensible demo data so the UI can still be developed.

## Important

The corridor labels are currently presented as the requested demo corridor, Jaipur <-> Delhi. Replace the display values with backend data once the final corridor endpoint is wired.
