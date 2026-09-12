from app.optimizer.constraints import parse_dt, passenger_conflict
from app.optimizer.objective import candidate_score
from app.ml.predictor import predict

def build_candidates(requests, slots, resources, resource_availability, assets, sections, trains, policies, max_per_task=12):
    asset_map={a['asset_id']:a for a in assets}; section_map={s['section_id']:s for s in sections}
    rav={(str(r['resource_id']),str(r['calendar_date'])):r for r in resource_availability}
    policy_by_route={}; notice_rules={}; max_duration={}
    for p in policies:
        if int(p.get('is_hard_constraint') or 0)!=1: continue
        if p['parameter_name']=='max_block_duration_min': max_duration[p['scope_value']]=int(float(p['parameter_value']))
        if p['parameter_name']=='min_notice_days': notice_rules[p['scope_value']]=int(float(p['parameter_value']))
    out=[]
    for ti,t in enumerate(requests):
        feasible=[]
        for si,s in enumerate(slots):
            if str(s['block_section_id']) != str(t['block_section_id']): continue
            d=str(s['calendar_date'])
            if d < str(t.get('earliest_start_date') or '0000-01-01') or d > str(t.get('latest_finish_date') or '9999-12-31'): continue
            if int(s.get('event_embargo_flag') or 0): continue
            sec=section_map.get(t['section_id'],{})
            maxdur=max_duration.get(sec.get('route_class'))
            pred=predict(t,asset_map.get(t['asset_id'],{}),sec,s)
            duration=max(int(t.get('min_viable_duration_min') or 1), int(round(pred['predicted_actual_duration_min']+pred['predicted_overrun_min'])))
            if maxdur and duration>maxdur: continue
            if duration>int(s.get('net_available_min') or 0): continue
            req_date=t.get('request_date')
            block_kind=t.get('block_kind')
            if req_date and block_kind in notice_rules:
                try:
                    if (parse_dt(d,'00:00')-parse_dt(str(req_date),'00:00')).days < notice_rules[block_kind]: continue
                except Exception: pass
            bad,_=passenger_conflict(t,s,trains)
            if bad: continue
            for ri,r in enumerate(resources):
                rid=str(t.get('primary_resource_id') or '')
                rclass=str(t.get('resource_class_required') or '')
                if rid and str(r['resource_id'])!=rid: continue
                if not rid and rclass not in ('','NONE') and str(r.get('resource_class'))!=rclass: continue
                av=rav.get((str(r['resource_id']),d))
                if not av or float(av.get('available_hours') or 0)<=0: continue
                start=parse_dt(d,s['available_from']); end=start+__import__('datetime').timedelta(minutes=duration)
                if end>parse_dt(d,s['available_to']): continue
                if duration>float(av.get('available_hours') or 0)*60: continue
                feasible.append({'task_index':ti,'slot_index':si,'resource_index':ri,'duration':duration,'score':candidate_score(pred,s,t),'prediction':pred,'start':start,'end':end})
        feasible.sort(key=lambda x:x['score'],reverse=True)
        out.extend(feasible[:max_per_task])
    return out
