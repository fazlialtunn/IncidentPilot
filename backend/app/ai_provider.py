import os
from typing import Any, Dict
import json
import random

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class BaseProvider:
    def explain_incident(self, evidence: Dict[str,Any]) -> Dict[str,Any]:
        raise NotImplementedError()

class OpenAIProvider(BaseProvider):
    def __init__(self):
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.openai = openai

    def explain_incident(self, evidence: Dict[str,Any]) -> Dict[str,Any]:
        # Call openai.chat.completions with a structured JSON output request
        prompt = f"Analyze the following incident evidence and produce a JSON with keys: summary, suspected_cause, runbook_id (nullable), impact_estimate(dict with keys error_rate, latency, affected_endpoints, users), confidence (0-1), evidence (list of citations). Evidence: {json.dumps(evidence)}"
        resp = self.openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{"role":"user","content":prompt}], max_tokens=400)
        text = resp['choices'][0]['message']['content']
        # best-effort JSON parse
        try:
            return json.loads(text)
        except Exception:
            return {"summary":text, "suspected_cause":"unable to parse", "runbook_id":None, "impact_estimate":{}, "confidence":0.0, "evidence":[]}

class DeterministicProvider(BaseProvider):
    def explain_incident(self, evidence: Dict[str,Any]) -> Dict[str,Any]:
        # Simple deterministic reasoning to work without API keys
        summary = evidence.get('alert', {}).get('summary', 'Alert received')
        service = evidence.get('alert', {}).get('service')
        recent_deploy = evidence.get('deployments', [])[-1] if evidence.get('deployments') else None
        suspected = "Unknown"
        runbook_id = None
        confidence = 0.3
        if recent_deploy and recent_deploy.get('service') == service:
            suspected = f"Recent deployment {recent_deploy.get('commit_sha')} to {service}"
            confidence = 0.7
        impact = {
            "error_rate": evidence.get('metrics', {}).get('error_rate', 0.0),
            "latency_ms": evidence.get('metrics', {}).get('latency', 0.0),
            "affected_endpoints": evidence.get('metrics', {}).get('endpoints', []),
            "estimated_users": int(evidence.get('metrics', {}).get('error_rate',0)*1000)
        }
        evidence_list = []
        if recent_deploy:
            evidence_list.append({"type":"deployment","commit":recent_deploy.get('commit_sha')})
        return {
            "summary": summary,
            "suspected_cause": suspected,
            "runbook_id": runbook_id,
            "impact_estimate": impact,
            "confidence": confidence,
            "evidence": evidence_list
        }

def get_provider():
    if OPENAI_API_KEY:
        try:
            return OpenAIProvider()
        except Exception:
            return DeterministicProvider()
    return DeterministicProvider()
