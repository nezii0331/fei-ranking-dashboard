# fei-ranking-dashboard
Educational dashboard for FEI World Rankings. Built with Python, BeautifulSoup, PostgreSQL, and future AI insights (RAG, trend analysis).

## Quickstart

1) Install deps
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Fetch + save CSV
```bash
python -m crawler.fetch
```

3) Run pipeline (CSV + optional DB load)
```bash
python -m crawler.piplind  # saves data/world50.csv
# To load into Postgres as well, set env vars and edit run_pipeline(load_db=True)
```

### Environment variables (PostgreSQL)
- `PG_HOST`, `PG_PORT`, `PG_DB`, `PG_USER`, `PG_PASSWORD` (or use a `.env` file)

### SQL schema
See `sql/schema.sql`.
