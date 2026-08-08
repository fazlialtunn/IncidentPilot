from .db import SessionLocal
from . import models, db
from datetime import datetime, timedelta

def seed():
    db.init_db()
    session = SessionLocal()
    # create services
    s1 = models.Service(name='checkout-service', owner='payments-team')
    s2 = models.Service(name='user-service', owner='accounts')
    s3 = models.Service(name='search-service', owner='search')
    session.add_all([s1,s2,s3])
    session.commit()
    session.refresh(s1)
    # commits and deployments
    c1 = models.Commit(sha='a1b2c3', message='Fix payment retry', author='alice', files_changed=['checkout/payment.py'], service_id=s1.id, timestamp=datetime.utcnow()-timedelta(hours=2))
    c2 = models.Commit(sha='d4e5f6', message='Add metrics', author='bob', files_changed=['checkout/metrics.py'], service_id=s1.id, timestamp=datetime.utcnow()-timedelta(days=1))
    session.add_all([c1,c2])
    session.commit()
    dep = models.Deployment(commit_sha=c1.sha, service_id=s1.id, deployed_at=datetime.utcnow()-timedelta(hours=1))
    session.add(dep)
    # runbooks
    rb1 = models.Runbook(title='Checkout payment failures', tags=['checkout','payments'], content='Steps: check payment provider, restart workers, rollback last deployment. Citation: runbook:checkout')
    rb2 = models.Runbook(title='User auth errors', tags=['user','auth'], content='Steps: check auth DB, rotate keys, clear cache.')
    session.add_all([rb1, rb2])
    session.commit()
    session.close()
