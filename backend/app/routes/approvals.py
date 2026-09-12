import json
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
router=APIRouter(prefix='/api/approvals',tags=['Approvals'])
@router.post('/{recommendation_id}/apply')
def apply(recommendation_id:str,db:Session=Depends(get_db)):
    rec=db.execute(text('SELECT * FROM recommendations WHERE recommendation_id=:id'),{'id':recommendation_id}).mappings().first()
    if not rec: raise HTTPException(404,'Recommendation not found')
    db.execute(text("UPDATE recommendations SET status='APPLIED' WHERE recommendation_id=:id"),{'id':recommendation_id})
    db.execute(text("UPDATE conflicts SET status='RESOLVED' WHERE conflict_id=:id"),{'id':rec['conflict_id']})
    aid=str(uuid4()); db.execute(text("INSERT INTO approval_actions(approval_id,recommendation_id,action,created_at) VALUES(:id,:rid,'APPLY',:at)"),{'id':aid,'rid':recommendation_id,'at':datetime.utcnow().isoformat()}); db.commit()
    return {'approval_id':aid,'recommendation_id':recommendation_id,'status':'APPLIED','message':'Recommendation approved. Replanning should be run to produce the final conflict-free schedule.'}
@router.post('/{recommendation_id}/reject')
def reject(recommendation_id:str,db:Session=Depends(get_db)):
    rec=db.execute(text('SELECT * FROM recommendations WHERE recommendation_id=:id'),{'id':recommendation_id}).mappings().first()
    if not rec: raise HTTPException(404,'Recommendation not found')
    db.execute(text("UPDATE recommendations SET status='REJECTED' WHERE recommendation_id=:id"),{'id':recommendation_id}); aid=str(uuid4()); db.execute(text("INSERT INTO approval_actions(approval_id,recommendation_id,action,created_at) VALUES(:id,:rid,'REJECT',:at)"),{'id':aid,'rid':recommendation_id,'at':datetime.utcnow().isoformat()}); db.commit()
    return {'approval_id':aid,'recommendation_id':recommendation_id,'status':'REJECTED'}
