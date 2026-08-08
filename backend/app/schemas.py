from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class AlertPayload(BaseModel):
    service: str
    severity: str
    summary: str
    details: Optional[str] = None

class CommitIn(BaseModel):
    sha: str
    message: str
    author: str
    files_changed: List[str] = []
    service: Optional[str]

class DeploymentIn(BaseModel):
    commit_sha: str
    service: str
    env: Optional[str] = 'production'

class IncidentOut(BaseModel):
    id: int
    status: str
    severity: str
    summary: Optional[str]
    created_at: datetime

class AIResult(BaseModel):
    summary: str
    suspected_cause: str
    runbook_id: Optional[int]
    impact_estimate: dict
    confidence: float
    evidence: List[Any] = []
