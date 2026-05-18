import Link from 'next/link'
import { Template } from '@/data/templates'

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/jackjk521/ai-automation-solutions/main/'

const integrationColors: Record<string, string> = {
  Gmail: 'bg-red-900/50 text-red-300 border-red-800',
  Slack: 'bg-purple-900/50 text-purple-300 border-purple-800',
  Notion: 'bg-gray-800 text-gray-300 border-gray-600',
  'Google Sheets': 'bg-green-900/50 text-green-300 border-green-800',
  Airtable: 'bg-blue-900/50 text-blue-300 border-blue-800',
  SerpAPI: 'bg-orange-900/50 text-orange-300 border-orange-800',
  Anthropic: 'bg-orange-900/50 text-orange-300 border-orange-800',
  BuiltWith: 'bg-yellow-900/50 text-yellow-300 border-yellow-800',
  Webhook: 'bg-cyan-900/50 text-cyan-300 border-cyan-800',
}

const triggerLabels: Record<string, { label: string; color: string }> = {
  webhook: { label: 'Webhook', color: 'bg-cyan-900/50 text-cyan-300 border-cyan-800' },
  schedule: { label: 'Scheduled', color: 'bg-yellow-900/50 text-yellow-300 border-yellow-800' },
  manual: { label: 'Manual', color: 'bg-gray-800 text-gray-300 border-gray-600' },
  gmail: { label: 'Gmail', color: 'bg-red-900/50 text-red-300 border-red-800' },
}

export default function TemplateCard({ template }: { template: Template }) {
  const triggerInfo = triggerLabels[template.trigger] ?? triggerLabels.manual
  return (
    <div className="group flex flex-col bg-gray-900 border border-gray-800 rounded-2xl p-6 hover:border-indigo-500/50 hover:scale-[1.02] transition-all duration-200 hover:shadow-lg hover:shadow-indigo-500/10">
      <div className="flex items-start justify-between gap-3 mb-4">
        <span className="inline-flex items-center justify-center w-9 h-9 rounded-lg bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 text-sm font-bold">{template.id}</span>
        <div className="flex items-center gap-2 flex-wrap justify-end">
          {template.isAIPowered && <span className="px-2 py-0.5 rounded-full bg-emerald-900/50 border border-emerald-700/50 text-emerald-400 text-xs font-medium">⚡ AI-Powered</span>}
          <span className={`px-2 py-0.5 rounded-full border text-xs font-medium ${triggerInfo.color}`}>{triggerInfo.label}</span>
        </div>
      </div>
      <h3 className="text-white font-semibold text-lg mb-2 leading-snug group-hover:text-indigo-300 transition-colors">{template.name}</h3>
      <p className="text-gray-400 text-sm leading-relaxed mb-4 flex-1">{template.description}</p>
      <div className="flex flex-wrap gap-1.5 mb-5">
        {template.integrations.map((i) => (
          <span key={i} className={`px-2 py-0.5 rounded-md border text-xs font-medium ${integrationColors[i] ?? 'bg-gray-800 text-gray-300 border-gray-600'}`}>{i}</span>
        ))}
      </div>
      <div className="flex gap-3 mt-auto">
        <Link href={`/templates/${template.slug}/`} className="flex-1 text-center px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-colors">View Details</Link>
        <a href={`${GITHUB_RAW_BASE}${template.githubPath}`} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white text-sm font-medium border border-gray-700">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
          JSON
        </a>
      </div>
    </div>
  )
}
