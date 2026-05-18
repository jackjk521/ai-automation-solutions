import Link from 'next/link'
import { templates } from '@/data/templates'
import TemplateGrid from '@/components/TemplateGrid'

const STATS = [
  { icon: '📋', value: '9', label: 'Templates', sub: 'Ready to import' },
  { icon: '🤖', value: '4', label: 'AI-Powered', sub: 'Claude · GPT · Groq' },
  { icon: '🔗', value: '8+', label: 'Integrations', sub: 'Gmail, Slack, Sheets…' },
  { icon: '⚡', value: '60s', label: 'Setup time', sub: 'Import & configure' },
]

const INTEGRATIONS = [
  { name: 'Gmail', color: 'text-red-400' },
  { name: 'Slack', color: 'text-purple-400' },
  { name: 'Google Sheets', color: 'text-green-400' },
  { name: 'Airtable', color: 'text-blue-400' },
  { name: 'Notion', color: 'text-gray-300' },
  { name: 'Anthropic', color: 'text-amber-400' },
  { name: 'SerpAPI', color: 'text-orange-400' },
  { name: 'BuiltWith', color: 'text-yellow-400' },
]

export default function HomePage() {
  const aiTemplates = templates.filter((t) => t.isAIPowered)

  return (
    <>
      {/* ── Hero ── */}
      <section className="relative overflow-hidden pt-24 pb-20 px-4">
        <div className="absolute inset-0 dot-grid" />
        <div className="absolute inset-0 bg-gradient-to-b from-indigo-950/40 via-gray-950/70 to-gray-950 pointer-events-none" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[600px] bg-indigo-600/8 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-gray-900/80 border border-gray-700 text-gray-400 text-sm font-medium mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Open Source · MIT License · Free Forever
          </div>

          <h1 className="text-5xl md:text-7xl font-bold text-white leading-[1.06] tracking-tight mb-6">
            Production-Ready{' '}
            <span className="gradient-text">n8n Automation</span>{' '}
            Templates
          </h1>

          <p className="text-lg md:text-xl text-gray-400 leading-relaxed mb-10 max-w-2xl mx-auto">
            {templates.length} open-source workflow templates for lead generation, AI email triage,
            invoice automation, web scraping, and more.{' '}
            <span className="text-gray-200 font-medium">Import in 60 seconds.</span>
          </p>

          <div className="flex flex-wrap justify-center gap-4 mb-14">
            <a
              href="#templates"
              className="px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-all hover:shadow-xl hover:shadow-indigo-500/30 hover:-translate-y-0.5"
            >
              Browse Templates
            </a>
            <a
              href="https://github.com/jackjk521/ai-automation-solutions"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-3.5 bg-gray-900/80 hover:bg-gray-800 text-gray-300 hover:text-white font-semibold rounded-xl transition-all border border-gray-700 hover:border-gray-500 flex items-center gap-2 backdrop-blur-sm"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
              </svg>
              Star on GitHub
            </a>
          </div>

          {/* Integration chips */}
          <div className="flex flex-wrap justify-center gap-2">
            {INTEGRATIONS.map((i) => (
              <span
                key={i.name}
                className={`px-3 py-1 rounded-full bg-gray-900/80 border border-gray-800 text-xs font-medium backdrop-blur-sm ${i.color}`}
              >
                {i.name}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ── Stats ── */}
      <section className="max-w-5xl mx-auto px-4 mb-24">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {STATS.map((s) => (
            <div
              key={s.label}
              className="card-shine bg-gray-900/60 border border-gray-800 rounded-2xl p-6 text-center hover:border-gray-700 transition-colors"
            >
              <div className="text-3xl mb-3">{s.icon}</div>
              <div className="text-4xl font-bold text-white mb-1">{s.value}</div>
              <div className="text-sm font-semibold text-gray-300 mb-0.5">{s.label}</div>
              <div className="text-xs text-gray-600">{s.sub}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Template grid with live search + filters ── */}
      <section id="templates" className="max-w-7xl mx-auto px-4 pb-24">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">All Templates</h2>
          <p className="text-gray-400 max-w-xl mx-auto">
            Each template is a complete n8n workflow — download the JSON, configure credentials, and you&apos;re live.
          </p>
        </div>
        <TemplateGrid />
      </section>

      {/* ── AI callout ── */}
      <section className="max-w-5xl mx-auto px-4 pb-28">
        <div className="relative rounded-2xl overflow-hidden border border-indigo-800/40 bg-gradient-to-br from-indigo-950/80 via-purple-950/60 to-gray-950">
          <div className="absolute inset-0 dot-grid opacity-20" />
          <div className="relative p-10">
            <div className="flex flex-wrap items-center gap-3 mb-5">
              <span className="px-3 py-1 rounded-full bg-emerald-500/15 text-emerald-400 text-xs font-semibold border border-emerald-500/25 uppercase tracking-wider">
                AI-Powered
              </span>
              <span className="text-gray-600 text-sm">
                {aiTemplates.length} of {templates.length} templates use AI
              </span>
            </div>

            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Swap AI providers in 30 seconds
            </h2>
            <p className="text-gray-400 leading-relaxed mb-8 max-w-2xl text-sm">
              Every AI template uses a generic{' '}
              <strong className="text-gray-200">HTTP Request node</strong> — change one URL and one
              header to switch between Anthropic Claude, OpenAI GPT, or Groq Llama. Your API key stays
              inside n8n&apos;s built-in Credentials vault and never leaves your instance.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-8">
              {[
                { name: 'Anthropic Claude', color: 'text-amber-400', border: 'border-amber-800/30', models: 'claude-haiku-4-5 · claude-sonnet-4-6' },
                { name: 'OpenAI GPT', color: 'text-emerald-400', border: 'border-emerald-800/30', models: 'gpt-4o-mini · gpt-4o' },
                { name: 'Groq Llama', color: 'text-purple-400', border: 'border-purple-800/30', models: 'llama-3.1-8b · mixtral-8x7b' },
              ].map((p) => (
                <div key={p.name} className={`bg-gray-900/70 border ${p.border} rounded-xl px-4 py-4`}>
                  <div className={`text-sm font-semibold mb-1 ${p.color}`}>{p.name}</div>
                  <div className="text-xs text-gray-600 font-mono">{p.models}</div>
                </div>
              ))}
            </div>

            <Link
              href="/docs/"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold transition-all hover:shadow-lg hover:shadow-indigo-500/25"
            >
              Read the configuration guide
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </section>
    </>
  )
}
