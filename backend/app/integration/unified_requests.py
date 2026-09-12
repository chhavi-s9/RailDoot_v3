from sqlalchemy.orm import Session
from app.integration.repository import rows, one

OPEN_STATUSES = "('CANCELLED','COMPLETED')"

def get_requests(db: Session, start=None, end=None, section=None, department=None, limit=1000):
    sql = f"SELECT * FROM v_unified_block_request WHERE request_status NOT IN {OPEN_STATUSES}"
    p = {}
    if start:
        sql += " AND latest_finish_date >= :start"; p['start'] = start
    if end:
        sql += " AND earliest_start_date <= :end"; p['end'] = end
    if section:
        sql += " AND section_id = :section"; p['section'] = section
    if department:
        sql += " AND dept = :department"; p['department'] = department
    sql += " ORDER BY safety_critical_flag DESC, dept_priority_rank ASC, days_overdue DESC LIMIT :limit"
    p['limit'] = limit
    return rows(db, sql, p)

def get_request(db, req_uid):
    return one(db, "SELECT * FROM v_unified_block_request WHERE req_uid=:id", {'id': req_uid})
