# Software Development Plan — TOC Navigator AI Backend Prototype

## 1. Foundation Setup
- Docker Compose brings up FastAPI API, PostgreSQL, Qdrant, Redis.
- Base project structure with linting, tests, and CI.

## 2. Order Management Core
- SQLAlchemy models and Alembic migrations for orders and operators.
- CRUD endpoints for `/orders` and `/operators`.
- Excel import endpoint with column validation.
- Unit and integration tests.

## 3. Event Logging & Vector Store
- Event model and endpoints to log text updates on orders.
- Background task generates embeddings and stores them in Qdrant.
- Search endpoint for similar events.

## 4. AI Assistance Layer
- Retrieval-augmented generation service querying Qdrant.
- Endpoint `POST /ai/advise` returning contextual recommendations from Gemini.

## 5. KPI & Document Services
- KPI calculation module and `GET /kpi` endpoint.
- PDF upload/download endpoints with metadata storage.

## Milestones
1. **Week 2** – Development environment and CI running.
2. **Week 8** – Stable CRUD and import interfaces.
3. **Week 12** – Event logging and semantic search.
4. **Week 16** – AI recommendations functional.
5. **Week 20** – KPI dashboard and document management ready.
