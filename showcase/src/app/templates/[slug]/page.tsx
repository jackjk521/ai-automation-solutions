import { templates } from '@/data/templates'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import FlowDiagram from '@/components/FlowDiagram'
import AIConfigPanel from '@/components/AIConfigPanel'

const GITHUB_RAW = 'https://raw.githubusercontent.com/jackjk521/ai-automation-solutions/main/'

export async function generateStaticParams() {
  return templates.map((t) => ({ slug: t.slug }))
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const t = templates.find((t) => t.slug === params.slug)
  return t ? { title: `${t.name} — n8n Template`, description: t.description } : {}
}

export default function TemplatePage({ params }: { params: { slug: string } }) {
  const template = templates.find((t) => t.slug === params.slug)
  if (!template) notFound()
  const triggerBadge: Record<string, { label: string; color: string }> = {
    webhook: { label: 'Webhook', color: 'bg-cyan-900/50 text-cyan-300 border-cyan-800' },
    schedule: { label: 'Schedule', color: 'bg-yellow-900/50 text-yellow-300 border-yellow-800' },
    manual: { label: 'Manual', color: 'bg-gray-700 text-gray-300 border-gray-600' },
    gmail: { label: 'Gmail', color: 'bg-red-900/50 text-red-300 border-red-800' },
  }
  const trigger = triggerBadge[template.trigger]
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <nav className="flex items-center gap-2 text-sm text-gray-500 mb-8">
        <Link href="/" className="hover:text-gray-300">Home</Link><span>/</span>
        <Link href="/#templates" className="hover:text-gray-300">Templates</Link><span>/</span>
        <span className="text-gray-300">{template.name}</span>
      </nav>
      <div className="mb-8">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <span className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-bold text-sm">{template.id}</span>
          {template.isAIPowered && <span className="px-3 py-1 rounded-full bg-emerald-900/50 text-emerald-300 text-xs font-semibold border border-emerald-700">AI-Powered</span>}
          <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${trigger.color}`}>{trigger.label}</span>
        </div>
        <h1 className="text-3xl font-bold text-white mb-3">{template.name}</h1>
        <p className="text-gray-400 text-lg leading-relaxed">{template.fullDescription}</p>
      </div>
      <div className="flex flex-wrap gap-3 mb-10">
        <a href={`${GITHUB_RAW}${template.githubPath}`} target="_blank" rel="noopener noreferrer" className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-all inline-flex items-center gap-2">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
          Download workflow.json
        </a>
        <Link href="/#templates" className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 font-semibold rounded-xl border border-gray-700">← Back</Link>
      </div>
      <div className="mb-10">
        <h2 className="text-xl font-semibold text-white mb-4">Workflow Flow</h2>
        <div className="rounded-xl bg-gray-900 border border-gray-800 overflow-x-auto p-4">
          <FlowDiagram nodes={template.nodes} trigger={template.trigger} />
        </div>
      </div>
      {template.isAIPowered && <AIConfigPanel />}
      {template.id === '09' && (
        <div className="rounded-xl border border-yellow-800 bg-yellow-950/30 p-6 my-8">
          <h3 className="text-yellow-300 font-semibold mb-3">📊 Lead Tracking Dashboard</h3>
          <p className="text-gray-300 text-sm mb-3">All prospects stored in Google Sheets with 20 columns for complete pipeline tracking:</p>
          <div className="flex flex-wrap gap-2">
            {['Date Added','Business Name','Website URL','Niche','Location','Has Website','Tech Stack','Site Score (0–10)','Priority','Has SSL','Phone','Address','Email Subject','Email Body','Outreach Status','Follow-up Date','Contract Value','Notes'].map((col) => (
              <span key={col} className="px-2 py-1 rounded bg-gray-800 text-gray-300 text-xs border border-gray-700">{col}</span>
            ))}
          </div>
        </div>
      )}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">Prerequisites</h2>
        <ul className="space-y-2">
          {template.prerequisites.map((p, i) => (
            <li key={i} className="flex items-start gap-3 text-gray-300 text-sm">
              <svg className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
              {p}
            </li>
          ))}
        </ul>
      </div>
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">Credentials to Configure</h2>
        <div className="rounded-xl overflow-hidden border border-gray-800">
          <table className="w-full text-sm">
            <thead><tr className="bg-gray-900"><th className="px-4 py-3 text-gray-400 font-medium text-left">Node</th><th className="px-4 py-3 text-gray-400 font-medium text-left">Credential Type</th><th className="px-4 py-3 text-gray-400 font-medium text-left">Notes</th></tr></thead>
            <tbody>
              {template.credentials.map((c, i) => (
                <tr key={i} className={i % 2 === 0 ? 'bg-gray-950' : 'bg-gray-900/50'}>
                  <td className="px-4 py-3 text-gray-300 font-mono text-xs">{c.node}</td>
                  <td className="px-4 py-3 text-indigo-300">{c.type}</td>
                  <td className="px-4 py-3 text-gray-400">{c.notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">Customization Tips</h2>
        <ul className="space-y-3">
          {template.customization.map((tip, i) => (
            <li key={i} className="flex items-start gap-3 text-gray-300 text-sm bg-gray-900 rounded-lg p-4 border border-gray-800">
              <span className="text-indigo-400 font-bold flex-shrink-0">{i + 1}.</span>{tip}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
