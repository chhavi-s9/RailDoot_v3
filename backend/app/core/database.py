from contextlib import contextmanager
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

RUNTIME_SCHEMA = """
CREATE TABLE IF NOT EXISTS generated_plans (
    plan_id TEXT PRIMARY KEY,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    status TEXT NOT NULL,
    solver_status TEXT,
    objective_value REAL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS plan_assignments (
    assignment_id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL,
    request_id TEXT NOT NULL,
    department TEXT,
    activity_code TEXT,
    asset_id TEXT,
    block_section_id TEXT,
    section_id TEXT,
    corridor_id TEXT,
    calendar_date TEXT,
    start_time TEXT,
    end_time TEXT,
    planned_duration_min INTEGER,
    resource_id TEXT,
    priority_score REAL,
    risk_score REAL,
    grant_probability REAL,
    predicted_overrun_min REAL,
    predicted_downtime_avoided_min REAL,
    estimated_detention_min INTEGER
);
CREATE TABLE IF NOT EXISTS conflicts (
    conflict_id TEXT PRIMARY KEY,
    plan_id TEXT,
    request_id TEXT,
    conflict_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    related_id TEXT,
    status TEXT NOT NULL DEFAULT 'OPEN',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id TEXT PRIMARY KEY,
    conflict_id TEXT,
    request_id TEXT,
    action TEXT NOT NULL,
    reason TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS approval_actions (
    approval_id TEXT PRIMARY KEY,
    recommendation_id TEXT NOT NULL,
    action TEXT NOT NULL,
    edited_payload_json TEXT,
    created_at TEXT NOT NULL
);
"""

def init_db():
    with engine.begin() as conn:
        for statement in RUNTIME_SCHEMA.strip().split(";\n"):
            if statement.strip():
                conn.execute(text(statement))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
