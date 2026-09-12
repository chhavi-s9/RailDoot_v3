from sqlalchemy.orm import Session
from app.integration.repository import rows

def assets(db, ids=None):
    if ids:
        return rows(db, "SELECT * FROM asset_master WHERE asset_id IN :ids", {'ids': tuple(ids)})
    return rows(db, "SELECT * FROM asset_master")

def asset_status(db, asset_ids=None):
    if asset_ids:
        return rows(db, "SELECT * FROM asset_availability_status WHERE asset_id IN :ids", {'ids': tuple(asset_ids)})
    return rows(db, "SELECT * FROM asset_availability_status")

def sections(db): return rows(db, "SELECT * FROM section_master")
def slots(db, start, end):
    return rows(db, "SELECT * FROM block_availability_calendar WHERE calendar_date BETWEEN :start AND :end AND status='AVAILABLE' ORDER BY calendar_date, available_from", {'start':start,'end':end})
def resources(db): return rows(db, "SELECT * FROM resource_master WHERE current_status NOT IN ('UNAVAILABLE','RETIRED')")
def resource_availability(db, start, end): return rows(db, "SELECT * FROM resource_availability WHERE calendar_date BETWEEN :start AND :end AND status='AVAILABLE'", {'start':start,'end':end})
def passenger_trains(db, start, end): return rows(db, "SELECT * FROM passenger_timetable")
def goods_trains(db, start, end): return rows(db, "SELECT * FROM goods_train_forecast WHERE forecast_date BETWEEN :start AND :end", {'start':start,'end':end})
def compatibility(db): return rows(db, "SELECT * FROM dept_activity_compatibility")
def policies(db): return rows(db, "SELECT * FROM policy_constraint_master")
