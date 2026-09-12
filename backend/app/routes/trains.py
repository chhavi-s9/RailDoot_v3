from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.integration.repository import rows
router=APIRouter(prefix='/api/trains',tags=['Trains'])
@router.get('/passenger')
def passenger(db:Session=Depends(get_db)): return rows(db,'SELECT * FROM passenger_timetable')
@router.get('/goods')
def goods(start:str,end:str,db:Session=Depends(get_db)): return rows(db,'SELECT * FROM goods_train_forecast WHERE forecast_date BETWEEN :s AND :e',{'s':start,'e':end})
