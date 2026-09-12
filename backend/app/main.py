from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.routes import dashboard,requests,assets,planning,conflicts,approvals,blocks,trains,comparison,ml

init_db()

app=FastAPI(title=settings.app_name,version=settings.app_version,description='AI-powered integrated railway maintenance block planning backend')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

@app.on_event('startup')
def startup(): init_db()

@app.get('/')
def root(): return {'app':'RailDoot','version':settings.app_version,'status':'running','data_source':'abp_integrated.db','optimizer':'OR-Tools CP-SAT','ml':'Random Forest'}
@app.get('/health')
def health(): return {'status':'ok'}

for r in [dashboard.router,requests.router,assets.router,planning.router,conflicts.router,approvals.router,blocks.router,trains.router,comparison.router,ml.router]: app.include_router(r)
