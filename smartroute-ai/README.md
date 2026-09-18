# SmartRoute AI
**"Right Model. Right Cost."**

An AI gateway that analyzes the complexity of every incoming query and routes it
to the cheapest model that can still answer it well — TinyLlama (local, free) for
simple queries, Gemini 2.5 Flash for anything needing real reasoning — instead of
sending every request to an expensive top-tier model.

Built for: **Cost Optimisation using LLM Routing** (hackathon problem statement).

---

## How it works

```
User Query
   ↓
Complexity Analyzer   (analyzer.py)   → keyword + structure heuristics, no extra model call
   ↓
Difficulty Scoring    → 1–10 score, Easy / Medium / Hard, confidence %
   ↓
LLM Router            (router.py)     → score 1-3 → TinyLlama, 4-10 → Gemini
   ↓
Model Selection + Connectors  (ollama_client.py / gemini_client.py)
   ↓
Response Generator
   ↓
Transparency Dashboard  (frontend)    → cost, savings, reasoning, timing, live pipeline
```

Every query and its routing decision is logged to SQLite so the Admin Dashboard
can show totals, per-difficulty breakdowns, model usage split, and cumulative
savings.

## Folder structure

```
smartroute-ai/
├── backend/
│   ├── app.py             # Flask app, all API routes
│   ├── analyzer.py        # Module 2 - Complexity Analyzer
│   ├── router.py          # Module 3 - Routing Engine
│   ├── cost_engine.py      # Module 5 - Cost Estimation Engine
│   ├── ollama_client.py    # Module 4 - Connector A (TinyLlama)
│   ├── gemini_client.py    # Module 4 - Connector B (Gemini 2.5 Flash)
│   ├── models.py           # SQLite schema + persistence
│   ├── dashboard.py        # Module 7 - Admin dashboard aggregation
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html          # Full React + Tailwind + Framer Motion UI (CDN, no build step)
└── README.md
```

## Tech stack

- **Frontend:** React 18, Tailwind CSS, Framer Motion — all loaded via CDN inside
  a single `index.html`, so there is no `npm install` / build step. Fastest path
  for a hackathon; swap for a Vite project later if you want a "real" frontend repo.
- **Backend:** Python Flask, SQLite
- **Models:** TinyLlama via [Ollama](https://ollama.com) (local, free), Gemini 2.5
  Flash via Google's Generative Language API

## Installation & run

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then edit .env and add your GEMINI_API_KEY
python app.py                   # runs on http://localhost:5000
```

> **No Gemini key yet?** The app still works — `gemini_client.py` falls back to a
> clearly-labeled mock response so you can demo the full routing flow offline.

### 2. TinyLlama (optional but recommended)

```bash
# install Ollama: https://ollama.com/download
ollama pull tinyllama
ollama serve                    # runs on http://localhost:11434
```

> If Ollama isn't running, `ollama_client.py` also falls back to a mock response —
> the pipeline, scoring, and cost math still run end-to-end.

### 3. Frontend

No build step needed — just open the file:

```bash
cd frontend
open index.html                 # macOS
# or: start index.html          # Windows
# or serve it: python -m http.server 5500
```

The page talks to the backend at `http://localhost:5000/api`. Make sure the
Flask server (step 1) is running first.

## API routes

| Method | Route          | Description                                      |
|--------|----------------|---------------------------------------------------|
| POST   | `/api/chat`    | Send a query, get routed response + full metadata |
| GET    | `/api/history` | Recent query log                                  |
| GET    | `/api/stats`   | Admin dashboard aggregates                        |
| POST   | `/api/reset`   | Clear the query log (demo reset)                  |
| GET    | `/api/health`  | Health check                                       |

Example:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Design a scalable banking architecture", "override": "auto"}'
```

## Routing rules

| Score | Difficulty | Routed to | Why |
|-------|-----------|-----------|-----|
| 1–3   | Easy      | TinyLlama | Simple facts/definitions — a small local model is enough and it's free |
| 4–6   | Medium    | Gemini    | Summaries, comparisons — needs more reliable reasoning |
| 7–10  | Hard      | Gemini    | Coding, system design, multi-step reasoning — needs the stronger model |

Manual override is available in the chat header: **Auto Routing / Force
TinyLlama / Force Gemini** — useful for demoing the cost difference live.

## Demo script (suggested for judges)

1. Ask **"What is Java?"** → scored Easy, routed to TinyLlama, ₹0 cost.
2. Ask **"Summarize the pros and cons of microservices"** → Medium, routed to Gemini.
3. Ask **"Design a scalable banking architecture with fraud detection"** → Hard,
   routed to Gemini, show the reasoning explanation and the cost-savings meter
   jump on the dashboard.
4. Toggle **Force Gemini** on the first "What is Java?" question again to show
   the cost/behavior difference the router is preventing.
5. Point at the **Admin Dashboard** card to show cumulative savings across the
   session.

## Deployment notes

- **Backend:** deploy `backend/` to any Python host (Render, Railway, Fly.io,
  a VM). Set `GEMINI_API_KEY` as an environment variable there instead of a
  local `.env` file. SQLite is fine for a demo; swap for Postgres for
  multi-instance production use.
- **Ollama/TinyLlama:** needs to run on a machine with `ollama serve` reachable
  from the backend — either colocate it with the backend or point
  `OLLAMA_URL` in `ollama_client.py` at a remote Ollama host.
- **Frontend:** `frontend/index.html` is fully static — host it on Netlify,
  Vercel, GitHub Pages, or any static file host. Just update `API_BASE` in the
  `<script>` at the top of `App` to your deployed backend URL (it's currently
  hardcoded to `http://localhost:5000/api` for local dev).
- **CORS** is already enabled on the Flask app via `flask-cors` for local dev;
  tighten `CORS(app)` to your deployed frontend origin in production.

## Extending further

- Swap the heuristic `analyzer.py` for a tiny classifier model if you want
  learned (rather than rule-based) difficulty scoring.
- Add more model tiers (e.g., a mid-tier model) and extend `router.py`'s score
  bands to route across three tiers instead of two.
- Add authentication + per-user cost tracking for a multi-tenant version.
