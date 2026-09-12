from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.integration.unified_requests import get_requests,get_request
from app.ml.priority import rank
from app.integration.repository import rows
router=APIRouter(prefix='/api/requests',tags=['Requests'])
@router.get('')
def list_requests(start: str|None=None,end: str|None=None,section: str|None=None,department: str|None=None,limit:int=100,db:Session=Depends(get_db)):
    return get_requests(db,start,end,section,department,min(limit,5000))
@router.get('/prioritized')
def prioritized(start: str|None=None,end: str|None=None,limit:int=50,db:Session=Depends(get_db)):
    req=get_requests(db,start,end,limit=min(limit,500))
    assets={r['asset_id']:r for r in rows(db,'SELECT * FROM asset_master')}; sections={r['section_id']:r for r in rows(db,'SELECT * FROM section_master')}
    return rank(req,assets,sections)
@router.get('/{req_uid}')
def request_detail(req_uid:str,db:Session=Depends(get_db)):
    r=get_request(db,req_uid)
    if not r: raise HTTPException(404,'Request not found')
    return r
