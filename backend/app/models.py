from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    owner = Column(String, nullable=True)

class Commit(Base):
    __tablename__ = "commits"
    id = Column(Integer, primary_key=True)
    sha = Column(String, unique=True, nullable=False)
    message = Column(String)
    author = Column(String)
    files_changed = Column(JSON, default=list)
    timestamp = Column(DateTime, default=datetime.utcnow)
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship('Service')

class Deployment(Base):
    __tablename__ = "deployments"
    id = Column(Integer, primary_key=True)
    commit_sha = Column(String, nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship('Service')
    deployed_at = Column(DateTime, default=datetime.utcnow)
    env = Column(String, default='production')

class Runbook(Base):
    __tablename__ = "runbooks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    tags = Column(JSON, default=list)
    content = Column(Text)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True)
    alert_payload = Column(JSON)
    status = Column(String, default='open')
    severity = Column(String, default='medium')
    created_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    suspected_cause = Column(Text)
    resolved = Column(Boolean, default=False)

class IncidentEvent(Base):
    __tablename__ = "incident_events"
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey('incidents.id'))
    incident = relationship('Incident')
    type = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
