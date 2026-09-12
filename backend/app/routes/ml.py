from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.integration.unified_requests import get_request
from app.integration.repository import rows
from app.ml.predictor import predict

router=APIRouter(prefix="/api/ml",tags=["AI / ML"])

@router.get("/predict")
def predict_request(req_uid: str, db: Session = Depends(get_db)):
    req=get_request(db,req_uid)
    if not req: raise HTTPException(404,"Request not found")
    asset=next(iter(rows(db,"SELECT * FROM asset_master WHERE asset_id=:id",{"id":req["asset_id"]})),{})
    section=next(iter(rows(db,"SELECT * FROM section_master WHERE section_id=:id",{"id":req["section_id"]})),{})
    return {"request_id":req_uid,"predictions":predict(req,asset,section)}
