from sqlalchemy.orm import Session
from app.integration.unified_requests import get_requests
from app.integration import data
from app.optimizer.candidates import build_candidates

def compare(db: Session, plan_id: str):
    from sqlalchemy import text
    p=db.execute(text("SELECT * FROM generated_plans WHERE plan_id=:id"),{'id':plan_id}).mappings().first()
    if not p: return {'error':'Plan not found'}
    assignments=[dict(x) for x in db.execute(text("SELECT * FROM plan_assignments WHERE plan_id=:id"),{'id':plan_id}).mappings().all()]
    rail={'tasks_scheduled':len(assignments),'estimated_detention_min':sum(x['estimated_detention_min'] or 0 for x in assignments),'predicted_downtime_avoided_min':sum(x['predicted_downtime_avoided_min'] or 0 for x in assignments)}
    requests=get_requests(db,p['start_date'],p['end_date'],limit=5000); slots=data.slots(db,p['start_date'],p['end_date']); assets=data.assets(db); sections=data.sections(db); resources=data.resources(db); rav=data.resource_availability(db,p['start_date'],p['end_date']); trains=data.passenger_trains(db,p['start_date'],p['end_date']); policies=data.policies(db)
    candidates=build_candidates(requests,slots,resources,rav,assets,sections,trains,policies,max_per_task=3)
    selected=[]; task=set(); slot_minutes={}; resource_minutes={}
    for c in sorted(candidates,key=lambda x:x['score'],reverse=True):
        if c['task_index'] in task: continue
        s=slots[c['slot_index']]; key=c['slot_index']; rkey=(str(resources[c['resource_index']]['resource_id']),str(s['calendar_date']))
        if slot_minutes.get(key,0)+c['duration']>int(s.get('net_available_min') or 0): continue
        cap=next((float(x['available_hours'])*60 for x in rav if str(x['resource_id'])==rkey[0] and str(x['calendar_date'])==rkey[1]),0)
        if resource_minutes.get(rkey,0)+c['duration']>cap: continue
        selected.append(c); task.add(c['task_index']); slot_minutes[key]=slot_minutes.get(key,0)+c['duration']; resource_minutes[rkey]=resource_minutes.get(rkey,0)+c['duration']
    baseline={'tasks_scheduled':len(selected),'estimated_detention_min':sum(int(slots[c['slot_index']].get('estimated_detention_min') or 0) for c in selected),'predicted_downtime_avoided_min':sum(float(c['prediction']['predicted_downtime_avoided_min']) for c in selected),'method':'priority-sorted greedy baseline'}
    return {'plan_id':plan_id,'raildoot':rail,'baseline':baseline,'delta':{'tasks_scheduled':rail['tasks_scheduled']-baseline['tasks_scheduled'],'estimated_detention_min':baseline['estimated_detention_min']-rail['estimated_detention_min'],'predicted_downtime_avoided_min':rail['predicted_downtime_avoided_min']-baseline['predicted_downtime_avoided_min']}}
