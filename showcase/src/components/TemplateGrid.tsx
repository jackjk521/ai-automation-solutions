'use client'

import { useState, useMemo } from 'react'
import { templates } from '@/data/templates'
import TemplateCard from './TemplateCard'

const TRIGGER_FILTERS = [
  { key: 'all', label: 'All Templates' },
  { key: 'webhook', label: 'Webhook' },
  { key: 'schedule', label: 'Scheduled' },
  { key: 'manual', label: 'Manual' },
  { key: 'gmail', label: 'Gmail' },
] as const

export default function TemplateGrid() {
  const [query, setQuery] = useState('')
  const [trigger, setTrigger] = useState('all')
  const [aiOnly, setAiOnly] = useState(false)

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim()
    return templates.filter((t) => {
      if (trigger !== 'all' && t.trigger !== trigger) return false
      if (aiOnly && !t.isAIPowered) return false
      if (!q) return true
      return (
        t.name.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q) ||
        t.tags.some((tag) => tag.toLowerCase().includes(q)) ||
        t.integrations.some((i) => i.toLowerCase().includes(q))
      )
    })
  }, [query, trigger, aiOnly])

  return (
    <div>
      {/* Search + Filters */}
      <div className="flex flex-col gap-5 mb-10">
        <div className="relative max-w-xl mx-auto w-full">
          <svg
            className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search templates, integrations, or tags…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full pl-10 pr-10 py-3 bg-gray-900 border border-gray-700 rounded-xl text-gray-200 placeholder-gray-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 text-sm transition-all"
          />
          {query && (
            <button
              onClick={() => setQuery('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        <div className="flex flex-wrap items-center justify-center gap-2">
          {TRIGGER_FILTERS.map((f) => (
            <button
              key={f.key}
              onClick={() => setTrigger(f.key)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all duration-150 ${
                trigger === f.key
                  ? 'bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-500/20'
                  : 'bg-gray-900 border-gray-700 text-gray-400 hover:border-gray-500 hover:text-gray-200'
              }`}
            >
              {f.label}
            </button>
          ))}

          <div className="w-px h-5 bg-gray-700 mx-1 hidden sm:block" />

          <button
            onClick={() => setAiOnly(!aiOnly)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all duration-150 flex items-center gap-1.5 ${
              aiOnly
                ? 'bg-emerald-950/60 border-emerald-500/60 text-emerald-300 shadow-lg shadow-emerald-500/10'
                : 'bg-gray-900 border-gray-700 text-gray-400 hover:border-gray-500 hover:text-gray-200'
            }`}
          >
            <span className={`w-1.5 h-1.5 rounded-full transition-colors ${aiOnly ? 'bg-emerald-400 animate-pulse' : 'bg-gray-600'}`} />
            AI-Powered
          </button>
        </div>
      </div>

      {/* Result count */}
      <p className="text-center text-gray-600 text-xs mb-8 tracking-wide uppercase">
        {filtered.length === templates.length
          ? `All ${templates.length} templates`
          : `${filtered.length} of ${templates.length} templates`}
      </p>

      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((t) => (
            <TemplateCard key={t.id} template={t} />
          ))}
        </div>
      ) : (
        <div className="text-center py-24">
          <div className="text-5xl mb-5">🔍</div>
          <p className="text-gray-300 text-lg font-semibold mb-2">No templates found</p>
          <p className="text-gray-600 text-sm mb-6">Try different keywords, or clear the active filters</p>
          <button
            onClick={() => { setQuery(''); setTrigger('all'); setAiOnly(false) }}
            className="px-5 py-2 rounded-xl bg-gray-800 text-gray-300 hover:text-white text-sm font-medium border border-gray-700 hover:border-gray-500 transition-colors"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  )
}
