from app.ml.predictor import predict

def rank(requests, asset_map=None, section_map=None):
    asset_map=asset_map or {}; section_map=section_map or {}
    out=[]
    for r in requests:
        p=predict(r, asset_map.get(r.get('asset_id'),{}), section_map.get(r.get('section_id'),{}))
        out.append({**r, **p})
    out.sort(key=lambda x:(x['priority_score'],x['risk_score']), reverse=True)
    for i,r in enumerate(out,1): r['rank']=i
    return out
