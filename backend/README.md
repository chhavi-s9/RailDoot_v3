# RailDoot Complete Backend

Integrated FastAPI + Random Forest ML + OR-Tools CP-SAT backend using `data/abp_integrated.db`.

## Run

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open `/docs` for Swagger.

## Generate a plan

```http
POST /api/planning/generate?start_date=2026-09-15&end_date=2026-09-21
```

The optimizer reads unified requests, block availability, resources, asset data, passenger timetable, compatibility rules and hard policy rules. ML predicts grant probability, actual duration, overrun and downtime avoided. CP-SAT selects a globally feasible schedule.

## Retrain

```bash
python scripts/train_models.py
```

Models are trained from `historical_block_grant` with a temporal split before/after 2026-04-01. Do not use outcome/label columns as model features.

## Architecture

Source systems -> integrated DB -> unified requests -> ML predictions -> candidate generation -> CP-SAT -> conflict detection -> recommendation -> officer approval -> final plan.

The data is synthetic and intended for demonstration, not live railway operations.
