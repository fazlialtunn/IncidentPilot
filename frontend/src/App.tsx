import React, {useEffect, useState} from 'react'
import axios from 'axios'

type Incident = { id:number; status:string; severity:string; summary?:string }
type IncidentDetail = { id:number; status:string; severity:string; summary?:string; suspected_cause?:string; timeline:any[] }

export default function App(){
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)
  const [selected, setSelected] = useState<number| null>(null)
  const [detail, setDetail] = useState<IncidentDetail| null>(null)
  const [suspects, setSuspects] = useState<any[]>([])

  useEffect(()=>{ fetchIncidents() },[])

  async function fetchIncidents(){
    setLoading(true)
    try{
      const r = await axios.get('/api/incidents')
      setIncidents(r.data)
    }catch(e){ console.error(e) }
    setLoading(false)
  }

  async function runDemo(){
    setLoading(true)
    try{
      const r = await axios.post('/api/simulate/demo')
      await fetchIncidents()
      if(r.data.incident_id){
        selectIncident(r.data.incident_id)
      }
    }catch(e){console.error(e)}
    setLoading(false)
  }

  async function selectIncident(id:number){
    setSelected(id)
    setDetail(null)
    try{
      const r = await axios.get(`/api/incidents/${id}`)
      setDetail(r.data)
      // fetch suspects for the service mentioned in first alert timeline if available
      const alertEvent = r.data.timeline?.find((t:any)=> t.type==='alert')
      const service = alertEvent?.payload?.service
      if(service){
        const s = await axios.get(`/api/services/${service}/suspects`)
        setSuspects(s.data.suspects || [])
      }
    }catch(e){console.error(e)}
  }

  async function approveAction(action:string){
    if(!selected) return
    try{
      await axios.post(`/api/incidents/${selected}/action`, { action, user: 'demo-user', note: 'Approved from UI' })
      // refresh
      await selectIncident(selected)
      await fetchIncidents()
    }catch(e){console.error(e)}
  }

  return (
    <div className="min-h-screen bg-neutral-900 text-white p-6 font-sans flex gap-6">
      <aside className="w-1/3">
        <header className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">IncidentPilot</h1>
          <button onClick={runDemo} className="bg-red-600 px-3 py-1 rounded">Run demo</button>
        </header>
        <section>
          <h2 className="text-lg mb-2">Active incidents</h2>
          {loading && <div>Loading…</div>}
          <div className="grid gap-3">
            {incidents.length===0 && !loading && <div className="text-neutral-400">No incidents</div>}
            {incidents.map(i=> (
              <div key={i.id} onClick={()=>selectIncident(i.id)} className={`p-4 rounded cursor-pointer ${selected===i.id? 'bg-neutral-700': 'bg-neutral-800'}`}>
                <div className="flex justify-between">
                  <div>
                    <div className="font-semibold">#{i.id} {i.summary}</div>
                    <div className="text-sm text-neutral-400">{i.status} • {i.severity}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </aside>

      <main className="flex-1">
        {!detail && <div className="text-neutral-400">Select an incident to view details</div>}
        {detail && (
          <div>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">#{detail.id} — {detail.summary}</h2>
                <div className="text-sm text-neutral-400">{detail.status} • {detail.severity}</div>
              </div>
              <div className="flex gap-2">
                <button onClick={()=>approveAction('rollback')} className="bg-yellow-600 px-3 py-1 rounded">Approve rollback</button>
                <button onClick={()=>approveAction('resolve')} className="bg-green-600 px-3 py-1 rounded">Mark resolved</button>
              </div>
            </div>

            <section className="mt-4 grid grid-cols-3 gap-4">
              <div className="col-span-2 p-4 bg-neutral-800 rounded">
                <h3 className="font-semibold mb-2">Timeline</h3>
                <div className="space-y-2">
                  {detail.timeline.map(t=> (
                    <div key={t.id} className="p-2 bg-neutral-700 rounded">
                      <div className="text-xs text-neutral-300">{t.type} • {t.created_at}</div>
                      <pre className="text-sm mt-1 whitespace-pre-wrap">{JSON.stringify(t.payload,null,2)}</pre>
                    </div>
                  ))}
                </div>
              </div>

              <div className="p-4 bg-neutral-800 rounded">
                <h3 className="font-semibold mb-2">AI Analysis & Slack Brief</h3>
                <div className="mb-3">
                  <div className="text-sm text-neutral-300">Suspected cause</div>
                  <div className="mt-1 text-white">{detail.suspected_cause || '—'}</div>
                </div>
                <div className="mb-3">
                  <div className="text-sm text-neutral-300">Slack-style brief</div>
                  <div className="mt-2 p-2 bg-neutral-700 rounded">{detail.summary}</div>
                </div>
                <h4 className="font-semibold">Top suspect commits</h4>
                <div className="space-y-2 mt-2">
                  {suspects.map(s=> (
                    <div key={s.sha} className="p-2 bg-neutral-700 rounded">
                      <div className="text-sm font-medium">{s.sha} — {s.message}</div>
                      <div className="text-xs text-neutral-400">score: {s.score.toFixed(1)}</div>
                    </div>
                  ))}
                  {suspects.length===0 && <div className="text-neutral-400">No suspects available</div>}
                </div>
              </div>
            </section>

          </div>
        )}
      </main>
    </div>
  )
}
