from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd
from joblib import load
from app.core.config import settings
from app.ml.features import CATEGORICAL, NUMERIC, FEATURES

MODELS = {}

def _get_model(name):
    if name not in MODELS:
        artifact = load(Path(settings.model_dir) / name)
        MODELS[name] = artifact["pipeline"] if isinstance(artifact, dict) and "pipeline" in artifact else artifact
    return MODELS[name]

def _hour(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return 0
    try: return int(str(v)[:2])
    except Exception: return 0

def build_features(request, asset=None, section=None, window=None):
    r, a, s, w = request or {}, asset or {}, section or {}, window or {}
    start = r.get("earliest_start_date") or r.get("schedule_due_date") or pd.Timestamp.today().strftime('%Y-%m-%d')
    d = pd.Timestamp(start)
    req_date = pd.Timestamp(r.get("request_date") or pd.Timestamp.today())
    notice = r.get("notice_days")
    if notice is None: notice = max(0, int((d - req_date).days))
    hour = _hour(w.get("available_from") or r.get("preferred_window_start"))
    row = {
      "source_system":r.get("source_system"),"dept":r.get("dept"),"activity_code":r.get("activity_code"),"activity_group":r.get("activity_group","SCHEDULED"),
      "route_class":r.get("route_class",s.get("route_class")),"line_config":r.get("line_config",s.get("line_config")),"block_kind":r.get("block_kind"),"dept_priority_code":r.get("dept_priority_code"),
      "resource_required":r.get("resource_required",r.get("resource_class_required")),"day_of_week":d.day_name()[:3],"traffic_density_gmt":r.get("traffic_density_gmt",s.get("traffic_density_gmt")),
      "notice_days":notice,"requested_duration_min":r.get("requested_duration_min",60),"min_viable_duration_min":r.get("min_viable_duration_min",30),"is_splittable":r.get("is_splittable",0),
      "dept_priority_rank":r.get("dept_priority_rank",4),"asset_criticality_score":r.get("asset_criticality_score",a.get("criticality_score",50)),"asset_health_index":r.get("asset_health_index",a.get("health_index",70)),
      "days_overdue":r.get("days_overdue",a.get("days_overdue",0)),"safety_critical_flag":r.get("safety_critical_flag",0),"sr_in_force_kmph":r.get("sr_in_force_kmph",r.get("restriction_speed_kmph",a.get("restriction_speed_kmph",0))),
      "failures_last_90d":r.get("failures_last_90d",a.get("failures_last_90d",0)),"material_readiness_pct":r.get("material_readiness_pct",100),"resource_confirmed_flag":r.get("resource_confirmed_flag",1),
      "joint_dept_flag":r.get("joint_dept_flag",1 if r.get("joint_dept_required") else 0),"window_start_hour":hour,"is_night_block":int(hour>=20 or hour<6),"month_num":int(d.month),
      "monsoon_flag":r.get("monsoon_flag",w.get("monsoon_flag",0)),"event_embargo_flag":r.get("event_embargo_flag",w.get("event_embargo_flag",0)),"passenger_trains_in_window":r.get("passenger_trains_in_window",w.get("passenger_trains_in_window",0)),
      "goods_trains_in_window":r.get("goods_trains_in_window",w.get("goods_trains_in_window",0)),"section_utilisation_pct":r.get("section_utilisation_pct",0),"competing_requests_same_window":r.get("competing_requests_same_window",0),"corridor_notified_flag":r.get("corridor_notified_flag",0)
    }
    return pd.DataFrame([row], columns=FEATURES)

def predict(request, asset=None, section=None, window=None):
    x = build_features(request, asset, section, window)
    grant=float(_get_model('grant_probability_rf.joblib').predict_proba(x)[0,1])
    duration=float(_get_model('actual_duration_rf.joblib').predict(x)[0])
    overrun=float(_get_model('overrun_rf.joblib').predict(x)[0])
    downtime=float(_get_model('downtime_avoided_rf.joblib').predict(x)[0])
    h=float(x['asset_health_index'].iloc[0] or 70); c=float(x['asset_criticality_score'].iloc[0] or 50); o=float(x['days_overdue'].iloc[0] or 0)
    risk=100*(.30*np.clip((100-h)/100,0,1)+.25*np.clip(c/100,0,1)+.20*np.clip(o/90,0,1)+.15*(1-grant)+.10*float(x['safety_critical_flag'].iloc[0] or 0))
    priority=.55*risk+.25*np.clip(downtime/5,0,100)+.20*c
    return {"grant_probability":round(grant,4),"predicted_actual_duration_min":round(max(1,duration),1),"predicted_overrun_min":round(max(0,overrun),1),"predicted_downtime_avoided_min":round(max(0,downtime),1),"risk_score":round(float(np.clip(risk,0,100)),2),"priority_score":round(float(np.clip(priority,0,100)),2)}
