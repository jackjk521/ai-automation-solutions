import Link from 'next/link'

const TEMPLATE_LINKS = [
  { href: '/templates/lead-capture-to-crm/', label: 'Lead Capture to CRM' },
  { href: '/templates/ai-email-triage/', label: 'AI Email Triage' },
  { href: '/templates/web-scraping-business-analysis/', label: 'Web Scraping & Outreach' },
  { href: '/templates/weekly-report-generator/', label: 'Weekly Report Generator' },
  { href: '/templates/support-ticket-classifier/', label: 'Support Ticket Classifier' },
  { href: '/templates/b2b-lead-gen-pipeline/', label: 'B2B Lead Gen Pipeline' },
]

const RESOURCE_LINKS = [
  { href: '/docs/', label: 'Documentation' },
  { href: '/docs/#import', label: 'How to Import' },
  { href: '/docs/#credentials', label: 'Configuring Credentials' },
  { href: '/docs/#ai-nodes', label: 'AI Node Setup' },
  { href: 'https://github.com/jackjk521/ai-automation-solutions', label: 'GitHub Repository', external: true },
]

export default function Footer() {
  return (
    <footer className="bg-gray-950 border-t border-gray-800/80 mt-0">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-10">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-14">
          {/* Brand */}
          <div className="lg:col-span-1 space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-indigo-500/20">
                n8
              </div>
              <span className="font-semibold text-white text-base">n8n Templates</span>
            </div>
            <p className="text-gray-500 text-sm leading-relaxed">
              Production-ready n8n automation workflows. Free, open source, and ready to import in 60 seconds.
            </p>
            <div className="flex items-center gap-3 pt-1">
              <a
                href="https://github.com/jackjk521/ai-automation-solutions"
                target="_blank"
                rel="noopener noreferrer"
                className="w-8 h-8 rounded-lg bg-gray-800 border border-gray-700 flex items-center justify-center text-gray-400 hover:text-white hover:border-gray-500 transition-all"
                aria-label="GitHub"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
                </svg>
              </a>
            </div>
          </div>

          {/* Templates */}
          <div className="space-y-4">
            <h3 className="text-white font-semibold text-sm">Popular Templates</h3>
            <ul className="space-y-2.5">
              {TEMPLATE_LINKS.map(({ href, label }) => (
                <li key={href}>
                  <Link href={href} className="text-gray-500 hover:text-gray-300 text-sm transition-colors">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div className="space-y-4">
            <h3 className="text-white font-semibold text-sm">Resources</h3>
            <ul className="space-y-2.5">
              {RESOURCE_LINKS.map(({ href, label, external }) => (
                <li key={href}>
                  {external ? (
                    <a
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-500 hover:text-gray-300 text-sm transition-colors flex items-center gap-1"
                    >
                      {label}
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </a>
                  ) : (
                    <Link href={href} className="text-gray-500 hover:text-gray-300 text-sm transition-colors">
                      {label}
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Author */}
          <div className="space-y-4">
            <h3 className="text-white font-semibold text-sm">Author</h3>
            <div className="space-y-3">
              <div>
                <p className="text-gray-300 text-sm font-medium">Jed Abner Chu</p>
                <a
                  href="https://aceinternational.solutions"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-400 hover:text-indigo-300 text-sm transition-colors"
                >
                  aceinternational.solutions
                </a>
              </div>
              <div className="rounded-xl bg-gray-900 border border-gray-800 p-4">
                <p className="text-xs text-gray-600 mb-1">License</p>
                <p className="text-gray-400 text-xs">
                  MIT — free to use, modify, and distribute.{' '}
                  <a
                    href="https://opensource.org/licenses/MIT"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-500 hover:text-gray-300 underline"
                  >
                    View license
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-gray-800/80 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-gray-600 text-xs">
            &copy; {new Date().getFullYear()} Jed Abner Chu &middot; aceinternational.solutions
          </p>
          <div className="flex items-center gap-4">
            <span className="px-2.5 py-1 rounded-full bg-gray-900 border border-gray-800 text-xs text-gray-500">
              MIT License
            </span>
            <span className="px-2.5 py-1 rounded-full bg-emerald-950/50 border border-emerald-900/50 text-xs text-emerald-600">
              Open Source
            </span>
          </div>
        </div>
      </div>
    </footer>
  )
}
