export const metadata = {
  title: 'Documentation — n8n Template Library',
  description: 'How to import templates, configure credentials, and set up AI nodes in n8n.',
}

export default function DocsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-white mb-3">Documentation</h1>
      <p className="text-gray-400 mb-12 text-lg">Everything you need to import, configure, and customise these n8n templates.</p>
      <nav className="rounded-xl bg-gray-900 border border-gray-800 p-6 mb-12">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">On This Page</h2>
        <ol className="space-y-2 text-indigo-400 text-sm">
          <li><a href="#import" className="hover:text-indigo-300">1. How to Import a Template</a></li>
          <li><a href="#credentials" className="hover:text-indigo-300">2. Configuring Credentials in n8n</a></li>
          <li><a href="#ai-nodes" className="hover:text-indigo-300">3. Configuring AI Nodes</a></li>
        </ol>
      </nav>
      <section id="import" className="mb-16 scroll-mt-20">
        <h2 className="text-2xl font-bold text-white mb-6 pb-3 border-b border-gray-800">1. How to Import a Template</h2>
        <ol className="space-y-6">
          {[
            {step:'Download the workflow.json',desc:'Navigate to the template detail page and click "Download workflow.json". This saves the n8n workflow export file to your machine.'},
            {step:'Open your n8n instance',desc:'Navigate to your n8n URL (e.g. http://localhost:5678) and log in.'},
            {step:'Import the file',desc:'Click Workflows → three-dot menu (⋮) → Import from File. In n8n v1.x+, you can drag and drop the file onto the canvas.'},
            {step:'Configure credentials',desc:'Nodes requiring credentials show a warning indicator. Click each node and set up the required credential.'},
            {step:'Test before enabling',desc:'Click Execute Workflow for a manual test run. Green nodes = success, red = error. Check Executions log for details.'},
            {step:'Enable the workflow',desc:'Toggle the Active switch to green. Click Save. Your workflow is now live.'},
          ].map((item,i) => (
            <li key={i} className="flex gap-5">
              <span className="w-8 h-8 rounded-full bg-indigo-600 flex-shrink-0 flex items-center justify-center text-white text-sm font-bold">{i+1}</span>
              <div><h3 className="text-white font-semibold mb-1">{item.step}</h3><p className="text-gray-400 text-sm leading-relaxed">{item.desc}</p></div>
            </li>
          ))}
        </ol>
      </section>
      <section id="credentials" className="mb-16 scroll-mt-20">
        <h2 className="text-2xl font-bold text-white mb-6 pb-3 border-b border-gray-800">2. Configuring Credentials in n8n</h2>
        <p className="text-gray-400 mb-6 text-sm">Go to <strong className="text-gray-300">Settings → Credentials → New Credential</strong> to create a reusable credential.</p>
        <div className="space-y-4">
          {[
            {service:'Gmail / Google Sheets',type:'Google OAuth2 API',steps:'Create a project in Google Cloud Console, enable Gmail/Sheets API, create OAuth2 credentials. In n8n, select Google OAuth2 API, paste Client ID and Secret, then click Connect my account.'},
            {service:'Slack',type:'Slack API (Bot Token)',steps:'Go to api.slack.com/apps → Create App → Add OAuth Scopes → Install to Workspace → Copy the Bot User OAuth Token (starts with xoxb-).'},
            {service:'Airtable',type:'Airtable Token',steps:'Go to airtable.com/create/tokens → Create Personal Access Token with data.records:read and data.records:write scopes.'},
            {service:'Notion',type:'Notion API',steps:'Go to notion.so/my-integrations → New Integration → Copy the Internal Integration Token. Share your database with the integration from Notion.'},
            {service:'SerpAPI / BuiltWith / AI Providers',type:'Header Auth',steps:'Settings → Credentials → New → Header Auth. Enter header name (e.g. x-api-key) and your API key as the value.'},
          ].map((c) => (
            <div key={c.service} className="rounded-xl bg-gray-900 border border-gray-800 p-5">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-white font-semibold text-sm">{c.service}</h3>
                <span className="text-xs text-indigo-400 bg-indigo-900/40 px-2 py-0.5 rounded border border-indigo-800">{c.type}</span>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed">{c.steps}</p>
            </div>
          ))}
        </div>
      </section>
      <section id="ai-nodes" className="mb-16 scroll-mt-20">
        <h2 className="text-2xl font-bold text-white mb-6 pb-3 border-b border-gray-800">3. Configuring AI Nodes</h2>
        <div className="rounded-xl border border-indigo-800 bg-indigo-950/30 p-5 mb-8">
          <p className="text-indigo-200 text-sm leading-relaxed"><strong>Why HTTP Request instead of a dedicated AI node?</strong> Swap providers by changing one URL and one header — no node changes needed. Works with Anthropic, OpenAI, Groq, and any other provider.</p>
        </div>
        <div className="space-y-6">
          {[
            {name:'Anthropic Claude',color:'text-orange-400',url:'https://api.anthropic.com/v1/messages',headers:['x-api-key: YOUR_ANTHROPIC_KEY','anthropic-version: 2023-06-01'],note:'Use claude-haiku-4-5-20251001 for speed/cost, claude-sonnet-4-6 for quality.'},
            {name:'OpenAI',color:'text-emerald-400',url:'https://api.openai.com/v1/chat/completions',headers:['Authorization: Bearer YOUR_OPENAI_KEY'],note:'gpt-4o-mini recommended for cost efficiency.'},
            {name:'Groq',color:'text-purple-400',url:'https://api.groq.com/openai/v1/chat/completions',headers:['Authorization: Bearer YOUR_GROQ_KEY'],note:'Generous free tier with very fast inference.'},
          ].map((p) => (
            <div key={p.name} className="rounded-xl bg-gray-900 border border-gray-800 overflow-hidden">
              <div className="px-5 py-4 border-b border-gray-800"><h3 className={`font-semibold ${p.color}`}>{p.name}</h3></div>
              <div className="p-5">
                <div className="font-mono text-xs bg-gray-950 rounded-lg p-4 mb-3 space-y-1.5">
                  <div><span className="text-gray-500">URL: </span><span className={p.color}>{p.url}</span></div>
                  {p.headers.map((h,i) => (<div key={i}><span className="text-gray-500">Header: </span><span className="text-gray-300">{h}</span></div>))}
                </div>
                <p className="text-gray-500 text-xs">{p.note}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
