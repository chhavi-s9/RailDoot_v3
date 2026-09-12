from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.optimizer.constraints import parse_dt, overlap
from app.integration import data

def detect(db:Session, assignments):
    conflicts=[]; trains=data.passenger_trains(db,'','')
    for a in assignments:
        day=a['date']; st=parse_dt(day,a['start_time']); en=parse_dt(day,a['end_time'])
        for t in trains:
            if t.get('section_id')!=a['section_id'] or t.get('block_section_id')!=a['block_section_id']: continue
            try: ts=parse_dt(day,t['entry_time']); te=parse_dt(day,t['exit_time'])
            except Exception: continue
            if overlap(st,en,ts,te) and int(t.get('is_reschedulable',0))==0:
                conflicts.append({'conflict_id':str(uuid4()),'request_id':a['request_id'],'conflict_type':'TRAIN_CONFLICT','severity':'HIGH','message':f"Non-reschedulable passenger train {t['train_no']} overlaps the proposed block.",'related_id':t['train_no'],'status':'OPEN','created_at':datetime.utcnow().isoformat()})
    return conflicts

def save(db, conflicts, plan_id=None):
    for c in conflicts:
        db.execute(text("INSERT INTO conflicts(conflict_id,plan_id,request_id,conflict_type,severity,message,related_id,status,created_at) VALUES(:conflict_id,:plan_id,:request_id,:conflict_type,:severity,:message,:related_id,:status,:created_at)"),{**c,'plan_id':plan_id})
    db.commit()
