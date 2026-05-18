'use client'

import { useState } from 'react'

const providers = [
  { name: 'Anthropic', color: 'text-orange-400', url: 'https://api.anthropic.com/v1/messages', headers: ['x-api-key: YOUR_ANTHROPIC_KEY','anthropic-version: 2023-06-01','content-type: application/json'] },
  { name: 'OpenAI', color: 'text-emerald-400', url: 'https://api.openai.com/v1/chat/completions', headers: ['Authorization: Bearer YOUR_OPENAI_KEY','content-type: application/json'] },
  { name: 'Groq', color: 'text-purple-400', url: 'https://api.groq.com/openai/v1/chat/completions', headers: ['Authorization: Bearer YOUR_GROQ_KEY','content-type: application/json'] },
]

export default function AIConfigPanel() {
  const [active, setActive] = useState(0)
  return (
    <div className="rounded-xl border border-indigo-800 bg-indigo-950/40 p-6 my-8">
      <div className="flex items-start gap-3 mb-4">
        <span className="text-2xl">🔑</span>
        <div>
          <h3 className="text-indigo-300 font-semibold text-base">AI Provider Configuration</h3>
          <p className="text-gray-400 text-sm mt-1">This template requires an LLM API key. Your key is configured inside n8n&apos;s Credentials system — it never touches this website.</p>
        </div>
      </div>
      <div className="flex gap-2 mb-4">
        {providers.map((p, i) => (
          <button key={p.name} onClick={() => setActive(i)} className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${active === i ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}>{p.name}</button>
        ))}
      </div>
      <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm space-y-1.5">
        <div><span className="text-gray-500">URL: </span><span className={providers[active].color}>{providers[active].url}</span></div>
        {providers[active].headers.map((h, i) => (<div key={i}><span className="text-gray-500">Header: </span><span className="text-gray-300">{h}</span></div>))}
      </div>
      <p className="text-gray-500 text-xs mt-3">Store your API key in n8n: <span className="text-gray-400">Settings → Credentials → New → Header Auth</span></p>
      <a href="/docs/" className="inline-flex items-center gap-1 text-indigo-400 hover:text-indigo-300 text-sm mt-3">See full configuration guide →</a>
    </div>
  )
}
