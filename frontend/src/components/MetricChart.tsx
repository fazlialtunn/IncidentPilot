import React from 'react'

type Props = {
  errorRate?: number
  latencyMs?: number
  estimatedUsers?: number
}

const axisLabels = [
  { label: 'Low', value: 0 },
  { label: 'Medium', value: 0.5 },
  { label: 'High', value: 1 }
]

export default function MetricChart({ errorRate = 0, latencyMs = 0, estimatedUsers = 0 }: Props){
  const normalizedError = Math.min(1, errorRate / 0.5)
  const normalizedLatency = Math.min(1, latencyMs / 1000)
  const normalizedUsers = Math.min(1, estimatedUsers / 2000)

  return (
    <div className="space-y-3">
      <div className="text-sm text-neutral-300">Key impact metrics</div>
      <div className="space-y-2">
        <MetricBar name="Error rate" value={normalizedError} display={`${(errorRate*100).toFixed(1)}%`} />
        <MetricBar name="Latency" value={normalizedLatency} display={`${latencyMs} ms`} />
        <MetricBar name="Users" value={normalizedUsers} display={`${estimatedUsers}`} />
      </div>
    </div>
  )
}

function MetricBar({ name, value, display }: { name:string, value:number, display:string }){
  return (
    <div>
      <div className="flex justify-between text-xs text-neutral-300 mb-1"><span>{name}</span><span>{display}</span></div>
      <div className="h-3 rounded-full bg-neutral-700 overflow-hidden">
        <div className="h-full rounded-full bg-gradient-to-r from-amber-500 to-rose-500" style={{ width: `${Math.round(value * 100)}%` }} />
      </div>
    </div>
  )
}
