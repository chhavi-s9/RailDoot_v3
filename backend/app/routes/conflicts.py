from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.services.recommendation_service import create_for_conflict
router=APIRouter(prefix='/api/conflicts',tags=['Conflicts'])
@router.get('')
def conflicts(status:str='OPEN',db:Session=Depends(get_db)):
    return [dict(x) for x in db.execute(text('SELECT * FROM conflicts WHERE status=:s ORDER BY CASE severity WHEN \'HIGH\' THEN 1 WHEN \'MEDIUM\' THEN 2 ELSE 3 END,created_at DESC'),{'s':status}).mappings().all()]
@router.post('/{conflict_id}/recommend')
def recommend(conflict_id:str,db:Session=Depends(get_db)):
    x=create_for_conflict(db,conflict_id)
    if not x: raise HTTPException(404,'Conflict or assignment not found')
    return x
