from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.integration.repository import rows
router=APIRouter(prefix='/api/assets',tags=['Assets'])
@router.get('')
def assets(db:Session=Depends(get_db)): return rows(db,'SELECT a.*, s.health_index,s.operational_status,s.predicted_failure_prob_30d,s.availability_pct_30d FROM asset_master a LEFT JOIN asset_availability_status s ON s.asset_id=a.asset_id')
@router.get('/risk')
def risk(db:Session=Depends(get_db)): return rows(db,"SELECT a.asset_id,a.asset_type,a.section_id,s.health_index,s.predicted_failure_prob_30d,s.availability_pct_30d,s.days_overdue,s.failures_last_90d FROM asset_master a JOIN asset_availability_status s ON s.asset_id=a.asset_id ORDER BY s.predicted_failure_prob_30d DESC LIMIT 100")
