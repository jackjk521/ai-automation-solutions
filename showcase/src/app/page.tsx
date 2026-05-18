import Link from 'next/link'
import { templates } from '@/data/templates'
import TemplateCard from '@/components/TemplateCard'

export default function HomePage() {
  const aiTemplates = templates.filter((t) => t.isAIPowered)
  return (
    <>
      <section className="relative overflow-hidden pt-20 pb-16 px-4">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-950/50 via-gray-950 to-gray-950 pointer-events-none" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-900/50 border border-indigo-700 text-indigo-300 text-sm font-medium mb-6">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Open Source · Free to Use
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight tracking-tight mb-6">
            Production-Ready{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">n8n Automation</span>{' '}Templates
          </h1>
          <p className="text-xl text-gray-400 leading-relaxed mb-10 max-w-2xl mx-auto">
            9 open-source workflow templates for lead generation, AI email triage, invoice automation, web scraping, and more. Import in 60 seconds.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <a href="#templates" className="px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-all">Browse Templates</a>
            <a href="https://github.com/jackjk521/ai-automation-solutions" target="_blank" rel="noopener noreferrer" className="px-8 py-3.5 bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white font-semibold rounded-xl transition-all border border-gray-700">View on GitHub</a>
          </div>
        </div>
      </section>
      <section className="border-y border-gray-800 bg-gray-900/50">
        <div className="max-w-5xl mx-auto px-4 py-6 grid grid-cols-2 md:grid-cols-4 divide-x divide-gray-800">
          {[{value:'9',label:'Templates'},{value:'4',label:'AI-Powered'},{value:'7+',label:'Integrations'},{value:'100%',label:'Open Source'}].map((s) => (
            <div key={s.label} className="text-center py-2 px-4">
              <div className="text-3xl font-bold text-white">{s.value}</div>
              <div className="text-gray-400 text-sm mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </section>
      <section id="templates" className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-white mb-4">All Templates</h2>
          <p className="text-gray-400 max-w-xl mx-auto">Each template is a complete n8n workflow — import the JSON, configure credentials, and you&apos;re live.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((t) => (<TemplateCard key={t.id} template={t} />))}
        </div>
      </section>
      <section className="max-w-5xl mx-auto px-4 pb-20">
        <div className="rounded-2xl bg-gradient-to-br from-indigo-950 to-purple-950 border border-indigo-800 p-10">
          <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-semibold border border-emerald-500/30 uppercase tracking-wide">AI-Powered</span>
          <h2 className="text-2xl font-bold text-white mt-4 mb-4">How AI Templates Work</h2>
          <p className="text-gray-300 leading-relaxed mb-6 max-w-2xl">
            Templates {aiTemplates.map((t) => t.id).join(', ')} use an <strong className="text-white">HTTP Request node</strong> to call any AI provider — Anthropic, OpenAI, or Groq. Your API key is stored securely inside n8n&apos;s built-in Credentials system.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {['Anthropic Claude','OpenAI GPT','Groq Llama'].map((p) => (<div key={p} className="bg-gray-900/60 rounded-lg px-4 py-3 text-sm text-gray-300 font-medium border border-gray-700 text-center">{p}</div>))}
          </div>
          <Link href="/docs/" className="inline-flex items-center gap-2 text-indigo-400 hover:text-indigo-300 font-medium transition-colors">Read the configuration guide →</Link>
        </div>
      </section>
    </>
  )
}
