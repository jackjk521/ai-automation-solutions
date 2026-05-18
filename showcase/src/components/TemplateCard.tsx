import Link from 'next/link'
import { Template } from '@/data/templates'

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/jackjk521/ai-automation-solutions/main/'

const integrationColors: Record<string, string> = {
  Gmail: 'bg-red-950/70 text-red-300 border-red-800/60',
  Slack: 'bg-purple-950/70 text-purple-300 border-purple-800/60',
  Notion: 'bg-gray-800/70 text-gray-300 border-gray-600/60',
  'Google Sheets': 'bg-green-950/70 text-green-300 border-green-800/60',
  Airtable: 'bg-blue-950/70 text-blue-300 border-blue-800/60',
  SerpAPI: 'bg-orange-950/70 text-orange-300 border-orange-800/60',
  Anthropic: 'bg-amber-950/70 text-amber-300 border-amber-800/60',
  BuiltWith: 'bg-yellow-950/70 text-yellow-300 border-yellow-800/60',
}

const triggerConfig: Record<string, { label: string; pill: string; glow: string; bar: string }> = {
  webhook: {
    label: 'Webhook',
    pill: 'bg-cyan-950/60 text-cyan-300 border-cyan-800/50',
    glow: 'hover:shadow-cyan-500/5',
    bar: 'bg-gradient-to-r from-cyan-500/60 to-transparent',
  },
  schedule: {
    label: 'Scheduled',
    pill: 'bg-amber-950/60 text-amber-300 border-amber-800/50',
    glow: 'hover:shadow-amber-500/5',
    bar: 'bg-gradient-to-r from-amber-500/60 to-transparent',
  },
  manual: {
    label: 'Manual',
    pill: 'bg-violet-950/60 text-violet-300 border-violet-800/50',
    glow: 'hover:shadow-violet-500/5',
    bar: 'bg-gradient-to-r from-violet-500/60 to-transparent',
  },
  gmail: {
    label: 'Gmail Trigger',
    pill: 'bg-rose-950/60 text-rose-300 border-rose-800/50',
    glow: 'hover:shadow-rose-500/5',
    bar: 'bg-gradient-to-r from-rose-500/60 to-transparent',
  },
}

function getComplexity(count: number): { label: string; color: string } {
  if (count <= 6) return { label: 'Starter', color: 'text-emerald-400 bg-emerald-950/50 border-emerald-800/40' }
  if (count <= 9) return { label: 'Intermediate', color: 'text-sky-400 bg-sky-950/50 border-sky-800/40' }
  if (count <= 12) return { label: 'Advanced', color: 'text-amber-400 bg-amber-950/50 border-amber-800/40' }
  return { label: 'Expert', color: 'text-rose-400 bg-rose-950/50 border-rose-800/40' }
}

export default function TemplateCard({ template }: { template: Template }) {
  const tc = triggerConfig[template.trigger] ?? triggerConfig.manual
  const nodeCount = template.nodes.length
  const complexity = getComplexity(nodeCount)

  return (
    <div className={`card-shine group relative flex flex-col rounded-2xl border border-gray-800 bg-gray-900/70 overflow-hidden transition-all duration-300 hover:border-gray-700 hover:-translate-y-1 hover:shadow-2xl ${tc.glow}`}>
      {/* Trigger-coloured top accent */}
      <div className={`h-px w-full ${tc.bar} opacity-60 group-hover:opacity-100 transition-opacity duration-300`} />

      <div className="p-5 flex flex-col flex-1 gap-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-3">
          <span className="inline-flex items-center justify-center w-9 h-9 rounded-xl bg-indigo-600/15 border border-indigo-500/20 text-indigo-400 text-sm font-bold flex-shrink-0 group-hover:bg-indigo-600/25 transition-colors">
            {template.id}
          </span>
          <div className="flex items-center gap-1.5 flex-wrap justify-end">
            {template.isAIPowered && (
              <span className="px-2 py-0.5 rounded-full bg-emerald-950/60 border border-emerald-700/40 text-emerald-400 text-xs font-medium flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                AI
              </span>
            )}
            <span className={`px-2.5 py-0.5 rounded-full border text-xs font-medium ${tc.pill}`}>
              {tc.label}
            </span>
          </div>
        </div>

        {/* Title + description */}
        <div className="flex-1">
          <h3 className="text-white font-semibold text-base leading-snug mb-1.5 group-hover:text-indigo-200 transition-colors">
            {template.name}
          </h3>
          <p className="text-gray-400 text-sm leading-relaxed line-clamp-2">
            {template.description}
          </p>
        </div>

        {/* Meta row: node count + complexity */}
        <div className="flex items-center gap-2.5">
          <span className="flex items-center gap-1.5 text-gray-500 text-xs">
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
            {nodeCount} nodes
          </span>
          <span className={`px-2 py-0.5 rounded-md border text-xs font-medium ${complexity.color}`}>
            {complexity.label}
          </span>
        </div>

        {/* Integrations */}
        <div className="flex flex-wrap gap-1.5">
          {template.integrations.map((i) => (
            <span
              key={i}
              className={`px-2 py-0.5 rounded-md border text-xs ${integrationColors[i] ?? 'bg-gray-800/60 text-gray-400 border-gray-700/60'}`}
            >
              {i}
            </span>
          ))}
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2">
          {template.tags.slice(0, 4).map((tag) => (
            <span key={tag} className="text-xs text-gray-600">
              #{tag}
            </span>
          ))}
        </div>

        {/* Actions */}
        <div className="flex gap-2 pt-1">
          <Link
            href={`/templates/${template.slug}/`}
            className="flex-1 text-center px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold transition-all hover:shadow-lg hover:shadow-indigo-500/25"
          >
            View Details
          </Link>
          <a
            href={`${GITHUB_RAW_BASE}${template.githubPath}`}
            target="_blank"
            rel="noopener noreferrer"
            title="Download workflow.json"
            className="px-4 py-2.5 rounded-xl bg-gray-800/80 hover:bg-gray-700 text-gray-400 hover:text-white text-sm font-medium border border-gray-700 hover:border-gray-500 transition-all flex items-center gap-1.5"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            JSON
          </a>
        </div>
      </div>
    </div>
  )
}
