from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.integration.repository import rows
router=APIRouter(prefix='/api/dashboard',tags=['Dashboard'])
@router.get('/summary')
def summary(db:Session=Depends(get_db)):
    total=rows(db,"SELECT COUNT(*) n FROM v_unified_block_request WHERE request_status NOT IN ('CANCELLED','COMPLETED')")[0]['n']
    critical=rows(db,"SELECT COUNT(*) n FROM v_unified_block_request WHERE request_status NOT IN ('CANCELLED','COMPLETED') AND (safety_critical_flag=1 OR dept_priority_rank=1)")[0]['n']
    overdue=rows(db,"SELECT COUNT(*) n FROM v_unified_block_request WHERE request_status NOT IN ('CANCELLED','COMPLETED') AND days_overdue>0")[0]['n']
    conflicts=rows(db,"SELECT COUNT(*) n FROM conflicts WHERE status='OPEN'")[0]['n']
    return {'total_open_requests':total,'critical_requests':critical,'overdue_requests':overdue,'open_conflicts':conflicts}
@router.get('/today')
def today(db:Session=Depends(get_db)):
    return rows(db,"SELECT * FROM v_unified_block_request WHERE request_status NOT IN ('CANCELLED','COMPLETED') ORDER BY safety_critical_flag DESC,dept_priority_rank ASC,days_overdue DESC LIMIT 25")
