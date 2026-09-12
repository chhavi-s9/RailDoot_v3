"""
Single source of truth for the feature schema used by both the offline
training script (scripts/train_models.py) and the online predictor
(app/ml/predictor.py).

Previously these lists were duplicated in both files. If they ever drifted
apart, a model trained with one column order/set could silently receive a
mismatched feature row at inference time (wrong columns, missing columns,
or columns in a different order fed into the pipeline's ColumnTransformer).
Importing from here instead makes that class of bug impossible: change a
feature once, and both training and inference pick it up automatically.
"""

CATEGORICAL = [
    "source_system",
    "dept",
    "activity_code",
    "activity_group",
    "route_class",
    "line_config",
    "block_kind",
    "dept_priority_code",
    "resource_required",
    "day_of_week",
]

NUMERIC = [
    "traffic_density_gmt",
    "notice_days",
    "requested_duration_min",
    "min_viable_duration_min",
    "is_splittable",
    "dept_priority_rank",
    "asset_criticality_score",
    "asset_health_index",
    "days_overdue",
    "safety_critical_flag",
    "sr_in_force_kmph",
    "failures_last_90d",
    "material_readiness_pct",
    "resource_confirmed_flag",
    "joint_dept_flag",
    "window_start_hour",
    "is_night_block",
    "month_num",
    "monsoon_flag",
    "event_embargo_flag",
    "passenger_trains_in_window",
    "goods_trains_in_window",
    "section_utilisation_pct",
    "competing_requests_same_window",
    "corridor_notified_flag",
]

FEATURES = CATEGORICAL + NUMERIC

# Prediction targets trained in scripts/train_models.py. Kept here too so
# any future script (evaluation, drift checks, etc.) has one place to look
# up what the historical_block_grant table is expected to contain, beyond
# just the input features.
LABELS = [
    "granted_flag",
    "granted_duration_min",
    "actual_start_delay_min",
    "actual_duration_min",
    "block_utilisation_pct",
    "overrun_min",
    "work_completion_status",
    "trains_detained",
    "total_detention_min",
    "asset_downtime_avoided_min",
    "post_block_defect_cleared",
]
