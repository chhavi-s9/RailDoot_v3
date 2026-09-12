import json
from datetime import datetime
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session

def create_for_conflict(db:Session, conflict_id):
    c=db.execute(text("SELECT * FROM conflicts WHERE conflict_id=:id"),{'id':conflict_id}).mappings().first()
    if not c: return None
    assignments=db.execute(text("SELECT * FROM plan_assignments WHERE request_id=:rid ORDER BY calendar_date,start_time LIMIT 5"),{'rid':c['request_id']}).mappings().all()
    if not assignments: return None
    a=dict(assignments[0])
    # Recommendation is deliberately advisory. The optimizer should be rerun with the conflicting movement excluded for a final alternative.
    payload={"request_id":c['request_id'],"current_assignment":a,"suggested_action":"MOVE_BLOCK_TO_NEXT_FEASIBLE_WINDOW","requires_officer_approval":True}
    rid=f"REC-{uuid4().hex[:10].upper()}"
    db.execute(text("INSERT INTO recommendations(recommendation_id,conflict_id,request_id,action,reason,payload_json,status,created_at) VALUES(:id,:cid,:rid,:action,:reason,:payload,'PENDING',:at)"),{'id':rid,'cid':conflict_id,'rid':c['request_id'],'action':'MOVE_BLOCK_TO_NEXT_FEASIBLE_WINDOW','reason':'Current assignment conflicts with a protected passenger movement. Re-run the optimizer after excluding the conflicting window.','payload':json.dumps(payload,default=str),'at':datetime.utcnow().isoformat()}); db.commit()
    return {**payload,'recommendation_id':rid,'reason':payload.get('suggested_action')}
