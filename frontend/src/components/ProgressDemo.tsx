import React, {useEffect, useState} from 'react'

const steps = [
  'Alert received for checkout-service',
  'Correlating deployment history',
  'Ranking suspect commits',
  'Searching relevant runbooks',
  'Estimating user impact',
  'Ready for human approval'
]

export default function ProgressDemo({ active }: { active: boolean }){
  const [index, setIndex] = useState(0)

  useEffect(()=>{
    if(!active){
      setIndex(0)
      return
    }
    const timer = window.setInterval(()=>{
      setIndex(prev => Math.min(prev + 1, steps.length - 1))
    }, 1100)
    return ()=> window.clearInterval(timer)
  }, [active])

  return (
    <div className="p-4 bg-neutral-800 rounded mt-4">
      <div className="font-semibold mb-2">Investigation progress</div>
      <div className="space-y-2">
        {steps.map((step, idx) => (
          <div key={step} className={`rounded px-3 py-2 ${idx <= index ? 'bg-green-600/20 text-white' : 'bg-neutral-700 text-neutral-300'}`}>
            <div className="text-sm">{step}</div>
            {idx === index && <div className="text-xs text-neutral-200 mt-1">In progress...</div>}
          </div>
        ))}
      </div>
    </div>
  )
}
