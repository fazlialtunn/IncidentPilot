import React, {useEffect, useState} from 'react'
import axios from 'axios'

export default function RunbookView({ query }:{ query: string }){
  const [runbooks, setRunbooks] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(()=>{ if(query) fetchRunbooks(query) },[query])

  async function fetchRunbooks(q:string){
    setLoading(true)
    try{
      const r = await axios.get(`/api/runbooks?query=${encodeURIComponent(q)}`)
      setRunbooks(r.data.runbooks || [])
    }catch(e){console.error(e)}
    setLoading(false)
  }

  if(!query) return <div className="text-neutral-400">No runbook query</div>
  return (
    <div>
      {loading && <div>Searching runbooks…</div>}
      {runbooks.length===0 && !loading && <div className="text-neutral-400">No runbooks found</div>}
      {runbooks.map(r=> (
        <div key={r.id} className="p-2 bg-neutral-700 rounded mt-2">
          <div className="font-semibold">{r.title} <span className="text-xs text-neutral-400">(score {r.score})</span></div>
          <div className="text-sm mt-1">{r.content}</div>
        </div>
      ))}
    </div>
  )
}
