from collections import defaultdict
from app.optimizer.candidates import build_candidates
from app.integration import data
from app.integration.unified_requests import get_requests
from app.core.config import settings

def solve(db, start_date, end_date, time_limit=None):
    from ortools.sat.python import cp_model
    requests=get_requests(db,start_date,end_date,limit=5000)
    slots=data.slots(db,start_date,end_date); assets=data.assets(db); sections=data.sections(db); resources=data.resources(db)
    rav=data.resource_availability(db,start_date,end_date); trains=data.passenger_trains(db,start_date,end_date); policies=data.policies(db)
    if not requests: return {'status':'NO_DATA','assignments':[],'unscheduled':0,'candidate_count':0}
    candidates=build_candidates(requests,slots,resources,rav,assets,sections,trains,policies,settings.max_candidates_per_task)
    if not candidates: return {'status':'INFEASIBLE','assignments':[],'unscheduled':len(requests),'candidate_count':0}
    model=cp_model.CpModel(); x=[model.NewBoolVar(f'x_{i}') for i in range(len(candidates))]
    by_task=defaultdict(list); by_slot=defaultdict(list); by_resource_day=defaultdict(list); by_section=defaultdict(list)
    for i,c in enumerate(candidates):
        by_task[c['task_index']].append(i); by_slot[c['slot_index']].append(i)
        day=str(slots[c['slot_index']]['calendar_date']); rid=resources[c['resource_index']]['resource_id']; by_resource_day[(str(rid),day)].append(i)
        by_section.setdefault((requests[c['task_index']]['section_id'],day),[]).append(i)
    for ks in by_task.values(): model.Add(sum(x[k] for k in ks)<=1)
    for si,ks in by_slot.items():
        s=slots[si]; model.Add(sum(x[k]*candidates[k]['duration'] for k in ks)<=int(s['net_available_min'] or 0)); model.Add(sum(x[k] for k in ks)<=int(s.get('remaining_capacity_dept_slots') or 1))
    rav_map={(str(r['resource_id']),str(r['calendar_date'])):r for r in rav}
    for key,ks in by_resource_day.items(): model.Add(sum(x[k]*candidates[k]['duration'] for k in ks)<=int(float(rav_map.get(key,{}).get('available_hours') or 0)*60))
    # Pairwise hard mutual exclusion for tasks in the same section/day when their compatibility says so.
    compat=data.compatibility(db)
    for a in range(len(candidates)):
        for b in range(a+1,len(candidates)):
            ca,cb=candidates[a],candidates[b]
            if ca['slot_index']!=cb['slot_index']: continue
            ta,tb=requests[ca['task_index']],requests[cb['task_index']]
            if ta['section_id']!=tb['section_id']: continue
            rules=[r for r in compat if ((r['dept_a']==ta['dept'] and r['activity_code_a'] in (ta['activity_code'],'ANY') and r['dept_b']==tb['dept'] and r['activity_code_b'] in (tb['activity_code'],'ANY')) or (r['dept_b']==ta['dept'] and r['activity_code_b'] in (ta['activity_code'],'ANY') and r['dept_a']==tb['dept'] and r['activity_code_a'] in (tb['activity_code'],'ANY')))]
            if rules and rules[0]['compatibility']=='MUTUALLY_EXCLUSIVE': model.Add(x[a]+x[b]<=1)
    # Same-section minimum gap between blocks on the same day.
    for a in range(len(candidates)):
        for b in range(a+1,len(candidates)):
            ca,cb=candidates[a],candidates[b]; ta,tb=requests[ca['task_index']],requests[cb['task_index']]
            if ta['section_id']!=tb['section_id'] or ca['slot_index']==cb['slot_index']: continue
            if ca['start'] < cb['end'] and cb['start'] < ca['end']: model.Add(x[a]+x[b]<=1)
    model.Maximize(sum(x[i]*c['score'] for i,c in enumerate(candidates)))
    solver=cp_model.CpSolver(); solver.parameters.max_time_in_seconds=float(time_limit or settings.optimizer_time_limit); solver.parameters.num_search_workers=8
    status=solver.Solve(model)
    assignments=[]; used=set()
    for i,c in enumerate(candidates):
        if not solver.Value(x[i]): continue
        t=requests[c['task_index']]; s=slots[c['slot_index']]; r=resources[c['resource_index']]; used.add(c['task_index'])
        pred=c['prediction']; assignments.append({'request_id':t['req_uid'],'department':t['dept'],'activity_code':t['activity_code'],'asset_id':t['asset_id'],'block_section_id':t['block_section_id'],'section_id':t['section_id'],'date':str(s['calendar_date']),'start_time':c['start'].strftime('%H:%M'),'end_time':c['end'].strftime('%H:%M'),'planned_duration_min':c['duration'],'resource_id':r['resource_id'],'priority_score':pred['priority_score'],'risk_score':pred['risk_score'],'grant_probability':pred['grant_probability'],'predicted_overrun_min':pred['predicted_overrun_min'],'predicted_downtime_avoided_min':pred['predicted_downtime_avoided_min'],'estimated_detention_min':int(s.get('estimated_detention_min') or 0),'corridor_id':s['corridor_id']})
    return {'status':solver.StatusName(status),'objective':solver.ObjectiveValue(),'wall_time_sec':solver.WallTime(),'candidate_count':len(candidates),'scheduled':len(assignments),'unscheduled':len(requests)-len(used),'assignments':assignments}
