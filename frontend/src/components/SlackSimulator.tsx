import React, {useEffect, useState} from 'react'
import axios from 'axios'

export default function SlackSimulator({ incidentId, onPosted }:{ incidentId:number, onPosted?:()=>void }){
  const [message, setMessage] = useState('')
  const [sending, setSending] = useState(false)

  async function post(){
    if(!message) return
    setSending(true)
    try{
      await axios.post('/api/simulate/slack', { incident_id: incidentId, message, user: 'demo-user' })
      setMessage('')
      if(onPosted) onPosted()
    }catch(e){console.error(e)}
    setSending(false)
  }

  return (
    <div className="mt-2">
      <textarea value={message} onChange={e=>setMessage(e.target.value)} className="w-full p-2 bg-neutral-700 rounded" rows={3} />
      <div className="flex gap-2 mt-2">
        <button onClick={post} disabled={sending} className="bg-blue-600 px-3 py-1 rounded">Post to Slack</button>
        <button onClick={()=>{setMessage('')}} className="bg-neutral-600 px-3 py-1 rounded">Clear</button>
      </div>
    </div>
  )
}
