from datetime import date, datetime
from typing import Any
from sqlalchemy import text
from sqlalchemy.orm import Session


def rows(db: Session, sql: str, params: dict[str, Any] | None = None):
    return [dict(r) for r in db.execute(text(sql), params or {}).mappings().all()]


def one(db: Session, sql: str, params=None):
    r = db.execute(text(sql), params or {}).mappings().first()
    return dict(r) if r else None
