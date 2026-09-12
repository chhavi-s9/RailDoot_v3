from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
router=APIRouter(prefix='/api/blocks',tags=['Blocks'])
@router.get('/plan/{plan_id}')
def blocks(plan_id:str,db:Session=Depends(get_db)):
    return [dict(x) for x in db.execute(text('SELECT * FROM plan_assignments WHERE plan_id=:id ORDER BY calendar_date,start_time'),{'id':plan_id}).mappings().all()]
