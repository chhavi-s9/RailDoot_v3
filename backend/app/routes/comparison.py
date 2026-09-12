from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.comparison_service import compare
router=APIRouter(prefix='/api/comparison',tags=['Comparison'])
@router.get('/{plan_id}')
def comparison(plan_id:str,db:Session=Depends(get_db)): return compare(db,plan_id)
