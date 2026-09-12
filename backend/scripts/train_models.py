from pathlib import Path
import sqlite3, json, sys
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, average_precision_score, r2_score, mean_absolute_error
from joblib import dump

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))  # so `app.ml.features` resolves when run as a script
from app.ml.features import CATEGORICAL as CAT, NUMERIC as NUM, FEATURES, LABELS

DB=ROOT/'data'/'abp_integrated.db'; OUT=ROOT/'ml_models'; OUT.mkdir(exist_ok=True)

def make_pipe(model):
 return Pipeline([('prep',ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore'),CAT),('num','passthrough',NUM)])),('model',model)])
def clean(df):
 for c in CAT: df[c]=df[c].fillna('UNKNOWN').astype(str)
 for c in NUM: df[c]=pd.to_numeric(df[c],errors='coerce').fillna(0)
 return df

def main():
 c=sqlite3.connect(DB); df=pd.read_sql_query('SELECT * FROM historical_block_grant ORDER BY request_date',c); c.close(); df=clean(df)
 cut=pd.Timestamp('2026-04-01'); dates=pd.to_datetime(df.request_date); tr=df[dates<cut]; te=df[dates>=cut]
 configs=[('grant_probability_rf.joblib','granted_flag',RandomForestClassifier(n_estimators=500,min_samples_leaf=3,class_weight='balanced',random_state=42,n_jobs=-1),'clf'),('actual_duration_rf.joblib','actual_duration_min',RandomForestRegressor(n_estimators=500,min_samples_leaf=2,random_state=42,n_jobs=-1),'reg'),('overrun_rf.joblib','overrun_min',RandomForestRegressor(n_estimators=500,min_samples_leaf=3,random_state=42,n_jobs=-1),'reg'),('downtime_avoided_rf.joblib','asset_downtime_avoided_min',RandomForestRegressor(n_estimators=500,min_samples_leaf=3,random_state=42,n_jobs=-1),'reg')]
 metrics={}
 for fn,label,model,kind in configs:
  p=make_pipe(model); p.fit(tr[FEATURES],tr[label]); pred=p.predict(te[FEATURES]); dump({'pipeline':p,'features':FEATURES},OUT/fn)
  if kind=='clf': metrics[label]={'roc_auc':roc_auc_score(te[label],p.predict_proba(te[FEATURES])[:,1]),'pr_auc':average_precision_score(te[label],p.predict_proba(te[FEATURES])[:,1])}
  else: metrics[label]={'r2':r2_score(te[label],pred),'mae':mean_absolute_error(te[label],pred)}
 (OUT/'metrics.json').write_text(json.dumps(metrics,indent=2)); print(json.dumps(metrics,indent=2))
if __name__=='__main__': main()
