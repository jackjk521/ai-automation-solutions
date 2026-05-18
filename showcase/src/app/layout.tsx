import type { Metadata } from 'next'
import './globals.css'
import Navigation from '@/components/Navigation'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'n8n Template Library | Free Production-Ready Automation Workflows',
  description: '9 open-source n8n workflow templates for lead generation, AI triage, invoice automation, web scraping, and more. Free to import and use.',
  keywords: 'n8n, automation, workflow templates, no-code, AI automation, lead generation',
  authors: [{ name: 'Jed Abner Chu', url: 'https://aceinternational.solutions' }],
  openGraph: {
    title: 'n8n Template Library',
    description: 'Production-ready n8n automation templates. Free to import.',
    type: 'website',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-gray-950 text-gray-100 antialiased">
        <Navigation />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  )
}
