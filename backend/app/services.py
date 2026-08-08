from .db import SessionLocal
from . import models
from .ai_provider import get_provider
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from sqlalchemy import desc

provider = get_provider()

def create_incident_from_alert(alert: Dict[str,Any]) -> models.Incident:
    db: Session = SessionLocal()
    inc = models.Incident(alert_payload=alert, severity=alert.get('severity','medium'), summary=alert.get('summary'))
    db.add(inc)
    db.commit()
    db.refresh(inc)
    # append an event
    ev = models.IncidentEvent(incident_id=inc.id, type='alert', payload=alert)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    # gather evidence
    evidence = gather_evidence(db, inc, alert)
    ai = provider.explain_incident(evidence)
    # attach AI inference to incident event
    ev2 = models.IncidentEvent(incident_id=inc.id, type='analysis', payload=ai)
    db.add(ev2)
    inc.suspected_cause = ai.get('suspected_cause')
    inc.summary = ai.get('summary')
    db.add(inc)
    db.commit()
    db.refresh(inc)
    db.close()
    return inc

def gather_evidence(db: Session, incident: models.Incident, alert: Dict[str,Any]) -> Dict[str,Any]:
    # recent deployments and commits for the service
    service_name = alert.get('service')
    deps = db.query(models.Deployment).join(models.Service).filter(models.Service.name==service_name).order_by(desc(models.Deployment.deployed_at)).limit(5).all()
    deployments = [{"commit_sha":d.commit_sha, "service":d.service.name, "deployed_at":d.deployed_at.isoformat()} for d in deps]
    # simple metrics placeholder
    metrics = {"error_rate":alert.get('meta',{}).get('error_rate', 0.05), "latency": alert.get('meta',{}).get('latency_ms', 120), "endpoints": alert.get('meta',{}).get('endpoints', [])}
    return {"alert": alert, "deployments": deployments, "metrics": metrics}

def list_incidents(limit:int=50) -> List[models.Incident]:
    db = SessionLocal()
    items = db.query(models.Incident).order_by(desc(models.Incident.created_at)).limit(limit).all()
    db.close()
    return items

def get_incident(incident_id:int) -> models.Incident:
    db = SessionLocal()
    inc = db.query(models.Incident).filter(models.Incident.id==incident_id).first()
    db.close()
    return inc

def add_incident_event(incident_id:int, type:str, payload:Dict[str,Any]):
    db = SessionLocal()
    ev = models.IncidentEvent(incident_id=incident_id, type=type, payload=payload)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    db.close()
    return ev
