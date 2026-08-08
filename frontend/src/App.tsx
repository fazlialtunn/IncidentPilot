import React, {useEffect, useState} from 'react'
import axios from 'axios'

type Incident = { id:number; status:string; severity:string; summary?:string }

export default function App(){
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)

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
      await axios.post('/api/simulate/demo')
      await fetchIncidents()
    }catch(e){console.error(e)}
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-neutral-900 text-white p-6 font-sans">
      <header className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">IncidentPilot</h1>
        <div>
          <button onClick={runDemo} className="bg-red-600 px-4 py-2 rounded">Run demo</button>
        </div>
      </header>
      <section>
        <h2 className="text-xl mb-2">Active incidents</h2>
        {loading && <div>Loading…</div>}
        <div className="grid gap-3">
          {incidents.length===0 && !loading && <div className="text-neutral-400">No incidents</div>}
          {incidents.map(i=> (
            <div key={i.id} className="p-4 rounded bg-neutral-800">
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
    </div>
  )
}
