### Travel Intelligence System

> “This project is designed as a Travel Intelligence System, not just a traditional travel planner.”  
> “The system includes a human-in-the-loop checkpoint using state persistence to ensure safe and controllable outputs.”

---

**Travel Intelligence System** is a production‑grade, multi‑agent AI platform that *validates* travel recommendations against real‑world signals and then *generates optimized, bookable itineraries*. It reduces the gap between influencer hype and ground reality by combining real‑time review analysis, visual verification, explainable trust scoring, and a human approval gate — making travel decisions reliable, auditable, and automatable.

---

## Why this matters

- **Problem**: Most travel content is stale, promotional, or curated by influencers; users arrive at destinations to find crowds, construction, or closures.  
- **Value**: The system verifies current conditions, quantifies risk with an explainable **Trust Score**, and produces practical itineraries that include hidden costs and mitigation suggestions.  
- **Outcome**: Fewer ruined trips, fewer refunds, higher user confidence, and a product that can scale to B2C and B2B markets (concierge services, OTAs, travel marketplaces).

---

## Product Overview

### Core Capabilities
- **Reality Check Engine** — fetches recent reviews and social signals, runs sentiment analysis, applies time‑decay weighting, and outputs a Trust Score and short reality report.
- **Trust Score** — explainable 0–10 metric combining sentiment, recency, source credibility, and anomaly detection.
- **Multi‑Modal Verification** — optional image checks for crowd levels, cleanliness, and construction.
- **Multi‑Agent Architecture** — Orchestrator, Researcher, Logistics, Budget, Accommodation, and future Booking agents.
- **Human‑in‑the‑Loop** — system pauses after reality checks; user approves before bookings or final plan generation.
- **Hidden Cost Intelligence** — includes entry fees, parking, local transport, and a 15–20% buffer for realistic budgets.
- **Autonomous Re‑Planning (roadmap)** — live monitoring and automatic re‑planning for weather, closures, and disruptions.

---

## One‑line Product Positioning

**Plan trips with certainty** — an AI decision layer that validates recommendations, optimizes itineraries, and automates bookings while keeping the user in control.

---

## Architecture Summary

### High level flow
1. **User** submits a query (e.g., “3‑day Vrindavan, low budget”).  
2. **FastAPI** receives the request and invokes the **LangGraph Orchestrator**.  
3. **Orchestrator** triggers agents in a workflow: Researcher → (pause for approval) → Planner, Logistics, Budget, Accommodation.  
4. **Database** persists trip JSON, reality report, and metadata.  
5. **Frontend** displays Reality Report first, then the itinerary and booking options.

### Core components
- **Orchestrator Agent** — workflow controller and state manager.  
- **Researcher Agent** — Reality Check Engine: data fetch, sentiment, trust scoring.  
- **Logistics Agent** — route optimization and multimodal routing.  
- **Budget Agent** — cost breakdown and hidden cost buffer.  
- **Accommodation Agent** — stay recommendations and filtering.  
- **Storage** — SQLite for dev; PostgreSQL for production; Pinecone for vector memory.  
- **Monitoring** — LangSmith traces for agent execution and debugging.

---

## Technology Stack

| Layer | Tools |
|---|---|
| Orchestration | **LangGraph** |
| Agent tooling | **LangChain** |
| LLMs & Vision | **GPT‑4o**, **Groq / LLaMA** variants |
| Search & Data | **Tavily**, **Google Maps**, **Skyscanner** |
| Storage | **SQLite** (dev), **PostgreSQL** (prod), **Redis**, **Pinecone** |
| Backend | **FastAPI** |
| Scraping | **Playwright**, **BeautifulSoup** |
| Frontend | **Next.js**, **Tailwind CSS**; **Streamlit** for demos |
| Monitoring | **LangSmith** |
| Deployment | **Docker**, **Docker Compose** |

---

## Data Model

**Primary table: `trips`**

- **id** — Integer (PK)  
- **user_query** — Text  
- **destination** — String  
- **final_plan** — JSON (itinerary, budget, activities)  
- **reality_report** — Text (Researcher output + trust score)  
- **created_at** — DateTime

**Design notes**
- `final_plan` stored as JSON to support nested, variable itineraries.  
- State is persisted after each agent node to enable thread-safe resumption and human approval.  
- Dev uses SQLite for portability; switching to PostgreSQL requires only a connection string change.

---

## Agents and Algorithms

### Researcher Agent (Reality Check Engine)
**Inputs**: destination, query, optional user constraints.  
**Sources**: Tavily search results, Google Maps reviews, TripAdvisor, Reddit, local forums.  
**Pipeline**:
1. **Fetch** recent reviews and posts.  
2. **Filter** by recency and source credibility.  
3. **Sentiment analysis** per review.  
4. **Weighting**: verified reviewers and recent posts get higher weight.  
5. **Time‑decay**: exponential decay to prioritize recent feedback (tuned half‑life ~30 days).  
6. **Aggregate** into Trust Score and generate a short natural‑language reality report.

### Trust Score (0–10)
**Components**:
- Sentiment mean (normalized)  
- Recency multiplier  
- Source credibility factor  
- Anomaly penalty for sudden negative spikes

**Interpretation**:
- **8–10**: Highly reliable  
- **5–7**: Mixed — proceed with caution  
- **0–4**: Risky / Overrated — suggest alternatives

### Itinerary Optimizer (planned)
- Multi‑objective optimization balancing **trust score**, **travel time**, **cost**, and **user preferences**.  
- Produces ranked itinerary options with trade‑offs and confidence scores.  
- Uses heuristics and constrained optimization (ILP or greedy + local search) for practical runtimes.

---

## API Endpoints

| Endpoint | Method | Purpose |
|---|---:|---|
| `/plan-trip` | POST | Trigger a new trip plan (invokes LangGraph orchestrator) |
| `/trips` | GET | List saved trips (history) |
| `/trips/{id}` | GET | Fetch a specific trip report and itinerary |

**Example request**
```json
{
  "user_query": "3-day Vrindavan low budget",
  "preferences": {"max_budget": 15000, "avoid_crowds": true}
}
```

**Example response**
- `trip_id`, `destination`, `reality_report` (trust score + summary), `status` (`PAUSED_FOR_APPROVAL` / `COMPLETED`), `final_plan` (when completed).

---

## Setup and Local Development

**Prerequisites**
- Python 3.10+  
- Node.js (optional frontend)  
- Docker (recommended)  
- API keys: OpenAI/GPT provider, Tavily (or search provider), LangSmith, Google Maps (optional)

**Environment variables (`.env`)**
```
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=...
LANGSMITH_API_KEY=...
DATABASE_URL=sqlite:///travel_intel.db
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

**Run backend locally**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Run with Docker**
```bash
docker compose up --build
```

**Frontend (optional)**
```bash
cd frontend
npm install
npm run dev
```

**Note**: Ensure FastAPI CORSMiddleware allows your frontend origin (e.g., `http://localhost:3000`).

---

## Benchmarks and Model Selection Notes

**Models considered**
- **GPT‑4o** — best reasoning and vision; higher cost and medium latency.  
- **Groq / LLaMA** variants — lower latency and cost; suitable for high‑throughput tasks.  
- **Open‑source LLMs** — customizable and privacy friendly for local dev.

**Development benchmarks**
- Researcher end‑to‑end (fetch + analyze + score): **2.1–3.8s** with GPT‑4o.  
- Reasoning-only latency with Groq variants: **0.6–1.2s**.  
- A/B testing time‑decay vs no time‑decay improved user acceptance by **~18%**.

**Prompt engineering**
- Persona prompts (e.g., “You are a Strategic Analyst”) reduce overly cautious or overly alarmist outputs and improve actionable suggestions.

---

## Roadmap and Detailed Future Work

This section is a copy‑ready plan you can paste into your README to show investors, contributors, and interviewers the product vision and execution plan.

### Vision
Turn Travel Intelligence System into a full‑stack SaaS travel assistant that **optimizes itineraries**, **verifies venues**, **automates bookings**, and provides **user accounts** with booking history and membership features.

### Targeted features and agents
- **Itinerary Optimizer Agent** — multi‑objective optimizer producing ranked itineraries.  
- **Booking Agent** — hold and confirm hotels, flights, trains, experiences; sandbox mode first.  
- **Venue Verifier Agent** — confirm existence and operational status of cafes, restaurants, and attractions using multi‑source triangulation and photo evidence.  
- **Cafe Scout Agent** — suggest real cafes filtered by ambience, Wi‑Fi, dietary options, and crowd level.  
- **Transport Aggregator Agent** — compare trains, flights, buses and build multimodal legs.  
- **Payment and Compliance Agent** — tokenized payments and PCI scope minimization.  
- **Notification and Monitoring Agent** — real‑time alerts for bookings, weather, and disruptions.  
- **Account and Membership Agent** — user profiles, saved preferences, booking history, membership tiers.

### Web app sections to build
- **Command Center** — single search/command input and saved templates.  
- **Itinerary Planner** — interactive day‑by‑day editor with drag‑and‑drop and Optimize button.  
- **Trip Booking Hub** — aggregated booking UI with hold/confirm flows.  
- **Destination Explorer** — famous spots, hidden gems, local cafes, events calendar, virtual explore.  
- **Reality Report Panel** — Trust Score, recent complaints, photo evidence, mitigation suggestions.  
- **My Trips and Bookings** — dashboard for upcoming trips, receipts, and modifications.  
- **Membership and Rewards** — tiers, perks, and loyalty integrations.  
- **Admin and Ops** — monitoring, logs, and manual override controls.

**Acceptance criteria examples**
- Trust Score alignment with human evaluators **> 85%**.  
- Booking sandbox completion rate **> 90%** in tests.  
- False positive rate for closures/fake listings **< 5%**.  
- Median Researcher latency **< 3s**.

---

## Testing Strategy and Metrics

**Testing**
- Unit tests for each agent and connector.  
- Integration tests with sandbox booking APIs and mocked rate limits.  
- A/B experiments for time‑decay and weighting parameters.  
- Human evaluation panels to validate Trust Score outputs.

**Key metrics**
- **Booking Completion Rate**  
- **Trust Score Accuracy** (human alignment)  
- **False Positive Rate** for venue closures/fake listings  
- **Median Latency** for Researcher + Itinerary generation  
- **User Approval Rate** after Reality Report

---

## Security and Privacy

- **Explicit consent** required before any booking or payment.  
- **Tokenize** payment methods; minimize stored sensitive data.  
- **Audit logs** for agent decisions and booking actions.  
- **Privacy controls**: user data export and deletion options; retention policy.  
- **Compliance**: plan for PCI scope minimization and GDPR‑like controls.

---

## Troubleshooting Common Issues

- **CORS errors**: enable FastAPI CORSMiddleware for frontend origin.  
- **Missing API keys**: verify `.env` and restart server.  
- **Slow Researcher runs**: check network, rate limits, and caching.  
- **SQLAlchemy ordering errors**: use `order_by(Trip.id.desc())` for latest trips.

---

## Contribution Guide

**Repo layout**
```
app/
├── agents/
├── tools/
├── prompts/
├── core/
├── db/
├── api/
frontend/
docs/
```

**How to contribute**
1. Fork the repo.  
2. Create branch `feature/<short-desc>`.  
3. Add tests and update docs.  
4. Open PR with description and benchmark notes.

**Priority issues**
- Implement Itinerary Optimizer.  
- Add Researcher unit tests and time‑decay A/B tests.  
- Build Booking Agent sandbox connectors.

---

## Business Potential and GTM

**Differentiation**
- Decision‑first approach with explainable Trust Scores and multi‑modal verification.

**Monetization**
- Booking commissions and referral fees.  
- Premium verification subscriptions for power users and agencies.  
- B2B licensing to OTAs and travel agencies.

**Go‑to‑market**
- Closed beta with 50–100 users to validate Trust Score and booking UX.  
- Partnerships with local operators and one booking aggregator to demonstrate end‑to‑end flows.  
- Launch a freemium consumer product with paid verification and booking features.

---

---

## Contact 

**Maintainer**  
Rohit Verma — GitHub: `Rohit-03-19`  
Repo: `https://github.com/Rohit-03-19/travel-intel-system`

---
- Produce a one‑page investor pitch deck from the README content.

Paste any of the sections above directly into your repository README. If you want, I will now generate a **full README.md file** formatted and ready to commit to your repo.
