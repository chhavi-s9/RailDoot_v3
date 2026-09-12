import json
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.optimizer.block_optimizer import solve
from app.services.conflict_service import detect, save

def generate(db:Session,start_date,end_date,time_limit=None):
    result=solve(db,start_date,end_date,time_limit)
    plan_id=f"PLAN-{uuid4().hex[:10].upper()}"
    now=datetime.utcnow().isoformat()
    db.execute(text("INSERT INTO generated_plans(plan_id,start_date,end_date,status,solver_status,objective_value,created_at) VALUES(:id,:s,:e,:st,:ss,:obj,:at)"),{'id':plan_id,'s':start_date,'e':end_date,'st':'GENERATED','ss':result.get('status'),'obj':result.get('objective'),'at':now})
    for a in result.get('assignments',[]):
        db.execute(text("INSERT INTO plan_assignments(assignment_id,plan_id,request_id,department,activity_code,asset_id,block_section_id,section_id,corridor_id,calendar_date,start_time,end_time,planned_duration_min,resource_id,priority_score,risk_score,grant_probability,predicted_overrun_min,predicted_downtime_avoided_min,estimated_detention_min) VALUES(:id,:plan_id,:request_id,:department,:activity_code,:asset_id,:block_section_id,:section_id,:corridor_id,:date,:start_time,:end_time,:duration,:resource_id,:priority,:risk,:grant,:overrun,:downtime,:detention)"),{'id':str(uuid4()),'plan_id':plan_id,**a,'date':a['date'],'duration':a['planned_duration_min'],'priority':a['priority_score'],'risk':a['risk_score'],'grant':a['grant_probability'],'overrun':a['predicted_overrun_min'],'downtime':a['predicted_downtime_avoided_min'],'detention':a['estimated_detention_min']})
    conflicts=detect(db,result.get('assignments',[])); save(db,conflicts,plan_id); db.commit()
    return {'plan_id':plan_id,**result,'conflicts':conflicts}
