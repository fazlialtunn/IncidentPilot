import React, {useState} from 'react'

export default function CommitCard({commit}:{commit:any}){
  const [open, setOpen] = useState(false)
  return (
    <div className="p-2 bg-neutral-700 rounded">
      <div className="flex justify-between items-center">
        <div>
          <div className="font-medium">{commit.sha}</div>
          <div className="text-xs text-neutral-400">{commit.message}</div>
        </div>
        <div className="text-right">
          <div className="text-sm">score: {commit.score.toFixed(1)}</div>
          <button onClick={()=>setOpen(!open)} className="text-xs text-blue-400 mt-1">{open? 'Hide':'Details'}</button>
        </div>
      </div>
      {open && (
        <div className="mt-2 text-sm bg-neutral-800 p-2 rounded">
          <div className="font-semibold">Files changed</div>
          <ul className="list-disc list-inside text-xs mt-1">
            {(commit.files_changed||[]).map((f:string)=> <li key={f}>{f}</li>)}
          </ul>
          <div className="mt-2 text-xs text-neutral-300">Author: {commit.author}</div>
        </div>
      )}
    </div>
  )
}
