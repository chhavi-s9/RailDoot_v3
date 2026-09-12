def candidate_score(pred, slot, task):
    detention=float(slot.get('estimated_detention_min') or 0)
    weather=float(slot.get('weather_risk_score') or 0)
    duration_penalty=max(0, float(pred['predicted_actual_duration_min']+pred['predicted_overrun_min'])-float(task.get('requested_duration_min') or 0))
    joint_bonus=250 if task.get('joint_dept_required') else 0
    return int(1000*pred['priority_score'] + 20*pred['predicted_downtime_avoided_min'] + joint_bonus - 25*detention - 5*weather - 8*duration_penalty)
