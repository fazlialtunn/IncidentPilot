from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from . import db, services, seed, models
from .schemas import AlertPayload
import uvicorn
import os

app = FastAPI(title='IncidentPilot')


@app.on_event('startup')
def startup():
    db.init_db()
    # seed if empty
    from .db import SessionLocal
    s = SessionLocal()
    cnt = s.query(db.Base.metadata.tables['services']).count() if 'services' in db.Base.metadata.tables else 0
    s.close()
    try:
        seed.seed()
    except Exception:
        pass


@app.get('/health')
def health():
    return {'status':'ok'}


@app.post('/webhook/alert')
async def webhook_alert(payload: dict, background_tasks: BackgroundTasks):
    try:
        inc = services.create_incident_from_alert(payload)
        return JSONResponse({'incident_id': inc.id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/incidents')
def list_incidents():
    items = services.list_incidents()
    out = []
    for i in items:
        out.append({'id':i.id,'status':i.status,'severity':i.severity,'summary':i.summary,'created_at':i.created_at.isoformat()})
    return out


@app.get('/incidents/{incident_id}')
def get_incident(incident_id: int):
    inc = services.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail='not found')
    from .db import SessionLocal
    s = SessionLocal()
    evs = s.query(models.IncidentEvent).filter(models.IncidentEvent.incident_id==incident_id).order_by(models.IncidentEvent.created_at).all()
    timeline = [{"id": e.id, "type": e.type, "payload": e.payload, "created_at": e.created_at.isoformat()} for e in evs]
    s.close()
    return {'id':inc.id,'status':inc.status,'severity':inc.severity,'summary':inc.summary,'suspected_cause':inc.suspected_cause,'timeline': timeline}


@app.post('/incidents/{incident_id}/action')
def incident_action(incident_id: int, payload: dict):
    # payload: { action: str, user: str, note?: str }
    action = payload.get('action')
    user = payload.get('user','demo-user')
    note = payload.get('note')
    if not action:
        raise HTTPException(status_code=400, detail='action required')
    ev = services.perform_action(incident_id, action, user, note)
    return {'event_id': ev.id}


@app.get('/services/{service_name}/suspects')
def suspects(service_name: str):
    ranked = services.rank_commits_for_service(service_name)
    return {'service': service_name, 'suspects': ranked}


@app.get('/runbooks')
def runbooks(query: str = ''):
    items = services.search_runbooks(query)
    return {'query': query, 'runbooks': items}


@app.get('/incidents/{incident_id}/analysis')
def incident_analysis(incident_id: int):
    analysis = services.get_incident_analysis(incident_id)
    return {'incident_id': incident_id, 'analysis': analysis}


@app.post('/simulate/slack')
def simulate_slack(payload: dict):
    # payload: { incident_id: int, message: str, user?: str }
    incident_id = payload.get('incident_id')
    message = payload.get('message')
    user = payload.get('user','simulator')
    if not incident_id or not message:
        raise HTTPException(status_code=400, detail='incident_id and message required')
    ev = services.post_slack_message(incident_id, message, user)
    return {'event_id': ev.id}


@app.post('/simulate/demo')
def run_demo(background_tasks: BackgroundTasks):
    # Simulate a progressive scenario via events
    from .db import SessionLocal
    s = SessionLocal()
    # create alert for checkout-service
    alert = {'service':'checkout-service','severity':'critical','summary':'Payment failure spike','meta':{'error_rate':0.22,'latency_ms':850,'endpoints':['/checkout/charge']}}
    inc_id = services.create_incident_from_alert(alert).id
    return {'incident_id': inc_id}

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=int(os.getenv('PORT',9000)), reload=True)
