from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.services.planning_service import generate
router=APIRouter(prefix='/api/planning',tags=['Planning'])
@router.post('/generate')
def generate_plan(start_date:str,end_date:str,time_limit:int|None=None,db:Session=Depends(get_db)):
    if end_date<start_date: raise HTTPException(400,'end_date must be >= start_date')
    return generate(db,start_date,end_date,time_limit)
@router.get('/{plan_id}')
def get_plan(plan_id:str,db:Session=Depends(get_db)):
    p=db.execute(text('SELECT * FROM generated_plans WHERE plan_id=:id'),{'id':plan_id}).mappings().first()
    if not p: raise HTTPException(404,'Plan not found')
    a=db.execute(text('SELECT * FROM plan_assignments WHERE plan_id=:id ORDER BY calendar_date,start_time'),{'id':plan_id}).mappings().all()
    c=db.execute(text('SELECT * FROM conflicts WHERE plan_id=:id ORDER BY severity'),{'id':plan_id}).mappings().all()
    return {'plan':dict(p),'assignments':[dict(x) for x in a],'conflicts':[dict(x) for x in c]}
