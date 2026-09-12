from datetime import datetime, timedelta

def parse_dt(day, tm): return datetime.strptime(f"{day} {tm}", "%Y-%m-%d %H:%M")

def overlap(a_start,a_end,b_start,b_end): return a_start < b_end and b_start < a_end

def passenger_conflict(task, slot, trains):
    day=str(slot['calendar_date']); start=parse_dt(day,slot['available_from']); end=parse_dt(day,slot['available_to'])
    bs=task.get('block_section_id'); sec=task.get('section_id')
    for t in trains:
        if t.get('block_section_id') not in (bs,None): continue
        if t.get('section_id') != sec: continue
        try: ts=parse_dt(day,t['entry_time']); te=parse_dt(day,t['exit_time'])
        except Exception: continue
        if overlap(start,end,ts,te):
            if int(t.get('is_reschedulable',0))==0 or int(t.get('max_permissible_detention_min') or 0)==0:
                return True, t
    return False, None
