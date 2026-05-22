export interface Template {
  id: string;
  slug: string;
  name: string;
  description: string;
  fullDescription: string;
  trigger: "webhook" | "schedule" | "manual" | "gmail";
  isAIPowered: boolean;
  integrations: string[];
  tags: string[];
  nodes: string[];
  prerequisites: string[];
  credentials: {
    node: string;
    type: string;
    notes: string;
  }[];
  customization: string[];
  githubPath: string;
}

export const templates: Template[] = [
  {
    id: "01",
    slug: "lead-capture-to-crm",
    name: "Lead Capture to CRM",
    description:
      "Capture form submissions and sync leads to Airtable with Slack notifications.",
    fullDescription:
      "Receives form submissions via webhook, deduplicates leads against Airtable, creates new records or updates existing ones, sends a personalised welcome email, and pings your sales team on Slack — all in real time.",
    trigger: "webhook",
    isAIPowered: false,
    integrations: ["Airtable", "Gmail", "Slack"],
    tags: ["CRM", "Lead Generation", "Sales"],
    nodes: [
      "Webhook Trigger",
      "Normalize Fields",
      "Check Required Fields",
      "Search Airtable",
      "Is Duplicate?",
      "Create Lead",
      "Send Welcome Email",
      "Notify Slack",
    ],
    prerequisites: [
      "n8n instance (cloud or self-hosted)",
      "Airtable account with a Leads base",
      "Gmail account with API access",
      "Slack workspace with bot token",
    ],
    credentials: [
      {
        node: "Airtable",
        type: "Airtable API",
        notes:
          "Personal Access Token from airtable.com/create/tokens",
      },
      {
        node: "Gmail",
        type: "Google OAuth2",
        notes:
          "Authorize via Google OAuth in n8n credentials",
      },
      {
        node: "Slack",
        type: "Slack API",
        notes: "Bot token with chat:write scope",
      },
    ],
    customization: [
      "Update AIRTABLE_BASE_ID variable in n8n Settings → Variables",
      "Modify the welcome email HTML in the Gmail node",
      "Change the Slack channel from #sales-leads to your preferred channel",
    ],
    githubPath:
      "templates/01-lead-capture-to-crm/workflow.json",
  },
  {
    id: "02",
    slug: "invoice-automation",
    name: "Invoice Automation",
    description:
      "Auto-generate and send branded HTML invoices to all active clients on the 1st of each month.",
    fullDescription:
      "Runs on the 1st of every month at 9am, pulls all active clients from Google Sheets, generates a professional branded HTML invoice for each one, sends it via Gmail, and logs the sent status back to the spreadsheet.",
    trigger: "schedule",
    isAIPowered: false,
    integrations: ["Google Sheets", "Gmail"],
    tags: ["Invoicing", "Finance", "Scheduling"],
    nodes: [
      "Schedule Trigger",
      "Get Active Clients",
      "Loop Over Clients",
      "Generate Invoice HTML",
      "Send Invoice Email",
      "Update Invoice Status",
    ],
    prerequisites: [
      "n8n instance",
      "Google Sheets with client data (ClientName, ClientEmail, MonthlyRate, Active)",
      "Gmail / Google Workspace account",
    ],
    credentials: [
      {
        node: "Google Sheets",
        type: "Google Sheets OAuth2",
        notes: "OAuth2 with spreadsheets read/write scope",
      },
      {
        node: "Gmail",
        type: "Gmail OAuth2",
        notes: "OAuth2 with gmail.send scope",
      },
    ],
    customization: [
      "Update company name, address, and bank details in the Code node invoice template",
      "Adjust tax rate per client by adding a TaxRate column to your Google Sheet",
      "Change the schedule cron expression (currently 0 9 1 * *) for different billing dates",
    ],
    githubPath:
      "templates/02-invoice-automation/workflow.json",
  },
  {
    id: "03",
    slug: "slack-project-notifications",
    name: "Slack Project Notifications",
    description:
      "Route GitHub/Jira/Trello webhook events to the right Slack channel with formatted messages.",
    fullDescription:
      "Receives webhooks from GitHub, Jira, or Trello, detects the event type (PR opened/merged, issue created/closed, task completed), formats a clean Slack Block Kit message, posts to the relevant project channel, and logs every event to a Google Sheet audit trail.",
    trigger: "webhook",
    isAIPowered: false,
    integrations: ["Slack", "Google Sheets"],
    tags: ["DevOps", "Project Management", "Notifications"],
    nodes: [
      "Webhook Trigger",
      "Parse Payload",
      "Switch (event type)",
      "Format Message",
      "Post to Slack",
      "Google Sheets Log",
    ],
    prerequisites: [
      "n8n instance",
      "Slack workspace with bot token",
      "GitHub/Jira/Trello webhook configured to point at n8n URL",
      "Google Sheets for audit log",
    ],
    credentials: [
      {
        node: "Slack",
        type: "Slack API",
        notes:
          "Bot token with chat:write and channels:read scopes",
      },
      {
        node: "Google Sheets",
        type: "Google OAuth2",
        notes: "OAuth2 with spreadsheets.append scope",
      },
    ],
    customization: [
      "Add more event types to the Switch node for custom routing",
      "Edit Block Kit templates in Set nodes to match your brand style",
      "Map different event types to different Slack channels",
    ],
    githubPath:
      "templates/03-slack-project-notifications/workflow.json",
  },
  {
    id: "04",
    slug: "ai-email-triage",
    name: "AI Email Triage",
    description:
      "Classify every incoming email as Urgent/Follow-up/Information/Spam and auto-route with labels.",
    fullDescription:
      "Watches your Gmail inbox, passes each email to an AI provider (Anthropic Claude or OpenAI) for classification into four categories, then applies Gmail labels automatically. Urgent emails also create a Notion task and fire a Slack alert. Zero emails fall through the cracks.",
    trigger: "gmail",
    isAIPowered: true,
    integrations: ["Gmail", "Notion", "Slack", "Anthropic"],
    tags: ["AI", "Email", "Triage", "Productivity"],
    nodes: [
      "Gmail Trigger",
      "Extract Email Data",
      "HTTP Request (AI Classify)",
      "Switch (category)",
      "Apply Gmail Label",
      "Create Notion Task",
      "Slack Urgent Alert",
    ],
    prerequisites: [
      "Gmail API credentials",
      "Notion integration token",
      "Slack bot token",
      "Anthropic or OpenAI API key stored in n8n Header Auth credential",
    ],
    credentials: [
      {
        node: "Gmail Trigger",
        type: "Google OAuth2",
        notes: "gmail.readonly + gmail.labels scope",
      },
      {
        node: "HTTP Request (AI)",
        type: "Header Auth",
        notes:
          "x-api-key: YOUR_ANTHROPIC_KEY | anthropic-version: 2023-06-01",
      },
      {
        node: "Notion",
        type: "Notion API",
        notes:
          "Internal integration token with database write access",
      },
      {
        node: "Slack",
        type: "Slack API",
        notes: "Bot token with chat:write scope",
      },
    ],
    customization: [
      "Edit the classification prompt in the HTTP Request body to add custom categories",
      "Swap Anthropic for OpenAI by updating the URL and Authorization header",
      "Change Notion database ID in the Notion node to your task tracker",
    ],
    githubPath:
      "templates/04-ai-email-triage/workflow.json",
  },
  {
    id: "05",
    slug: "real-estate-lead-nurture",
    name: "Real Estate Lead Nurture",
    description:
      "Auto-nurture property inquiries with a personalised 3-day email follow-up sequence.",
    fullDescription:
      "Captures property inquiries via webhook, logs them to a Google Sheets CRM, sends a personalised intro email immediately, waits 3 days, checks if the lead replied, and sends a targeted follow-up if they haven't. All email templates are real-estate branded and customisable.",
    trigger: "webhook",
    isAIPowered: false,
    integrations: ["Google Sheets", "Gmail"],
    tags: [
      "Real Estate",
      "Lead Nurture",
      "Email Sequences",
    ],
    nodes: [
      "Webhook Trigger",
      "Enrich Lead Data",
      "Add to CRM Sheet",
      "Send Intro Email",
      "Wait 3 Days",
      "Check Reply Status",
      "Did They Reply?",
      "Send Follow-up Email",
      "Log Outcome",
    ],
    prerequisites: [
      "n8n instance",
      "Google Sheets with Leads table",
      "Gmail account for sending",
    ],
    credentials: [
      {
        node: "Google Sheets",
        type: "Google OAuth2",
        notes: "OAuth2 with spreadsheets read/write scope",
      },
      {
        node: "Gmail",
        type: "Gmail OAuth2",
        notes: "OAuth2 with gmail.send scope",
      },
    ],
    customization: [
      "Update agent name, phone, and Calendly links in both Gmail nodes",
      "Change Wait node from 3 days to match your sales process",
      "Add a Day 7 third touch-point email for high-value leads",
    ],
    githubPath:
      "templates/05-real-estate-lead-nurture/workflow.json",
  },
  {
    id: "06",
    slug: "support-ticket-classifier",
    name: "Support Ticket Classifier",
    description:
      "AI-classify incoming support tickets by category, priority, and sentiment — then route automatically.",
    fullDescription:
      "Receives support tickets via webhook, sends the content to an AI provider to extract Category (Billing/Technical/Feature/Bug), Priority (High/Medium/Low), and Sentiment, then routes the ticket to the right Slack channel, assigns a team member, and sends an auto-acknowledgement email to the customer.",
    trigger: "webhook",
    isAIPowered: true,
    integrations: ["Slack", "Gmail", "Anthropic"],
    tags: ["AI", "Support", "Classification", "Routing"],
    nodes: [
      "Webhook Trigger",
      "Extract Ticket Content",
      "HTTP Request (AI Classify)",
      "Parse AI Response",
      "Switch (category)",
      "Post to Slack Channel",
      "Assign Team Member",
      "Send Acknowledgement Email",
    ],
    prerequisites: [
      "n8n instance",
      "Slack workspace with category channels",
      "Gmail for auto-replies",
      "Anthropic or OpenAI API key",
    ],
    credentials: [
      {
        node: "HTTP Request (AI)",
        type: "Header Auth",
        notes:
          "x-api-key: YOUR_ANTHROPIC_KEY | anthropic-version: 2023-06-01",
      },
      {
        node: "Slack",
        type: "Slack API",
        notes: "Bot token with chat:write scope",
      },
      {
        node: "Gmail",
        type: "Gmail OAuth2",
        notes: "OAuth2 with gmail.send scope",
      },
    ],
    customization: [
      "Edit the AI classification prompt to add custom ticket categories",
      "Configure Slack channel IDs per category in the Switch node outputs",
      "Add a Notion/Jira node to auto-create tickets in your project management tool",
    ],
    githubPath:
      "templates/06-support-ticket-classifier/workflow.json",
  },
  {
    id: "07",
    slug: "weekly-report-generator",
    name: "Weekly Report Generator",
    description:
      "Pull weekly KPIs from Google Sheets, generate an AI narrative, and email a branded HTML report.",
    fullDescription:
      "Runs every Friday at 5pm, fetches this week's deals, leads, and revenue data from Google Sheets, calculates KPIs in a Code node, asks an AI to write an executive narrative summary, compiles a styled HTML email report, and sends it to your distribution list.",
    trigger: "schedule",
    isAIPowered: true,
    integrations: ["Google Sheets", "Gmail", "Anthropic"],
    tags: ["AI", "Reporting", "KPIs", "Scheduling"],
    nodes: [
      "Schedule Trigger (Friday 5pm)",
      "Fetch Weekly Data",
      "Calculate KPIs",
      "HTTP Request (AI Narrative)",
      "Compile HTML Report",
      "Send Report Email",
    ],
    prerequisites: [
      "n8n instance",
      "Google Sheets with weekly sales data",
      "Gmail for sending",
      "Anthropic or OpenAI API key",
    ],
    credentials: [
      {
        node: "Google Sheets",
        type: "Google OAuth2",
        notes: "OAuth2 with spreadsheets.readonly scope",
      },
      {
        node: "HTTP Request (AI)",
        type: "Header Auth",
        notes:
          "x-api-key: YOUR_ANTHROPIC_KEY | anthropic-version: 2023-06-01",
      },
      {
        node: "Gmail",
        type: "Gmail OAuth2",
        notes: "OAuth2 with gmail.send scope",
      },
    ],
    customization: [
      "Update the Google Sheets column names in the KPI calculation Code node",
      "Add custom KPI metrics to the AI prompt for deeper insights",
      "Modify the HTML email template colors to match your brand",
    ],
    githubPath:
      "templates/07-weekly-report-generator/workflow.json",
  },
  {
    id: "08",
    slug: "client-onboarding-sequence",
    name: "Client Onboarding Sequence",
    description:
      "Automated 7-day client onboarding: welcome email, Notion page, daily touchpoints, check-in.",
    fullDescription:
      "Triggers when a new client is marked active. Immediately sends a welcome email and creates a Notion onboarding workspace. Then across Days 1, 3, and 7 (using n8n Wait nodes), sends a Getting Started guide, notifies the account manager in Slack, and sends a check-in email — logging completion to Google Sheets.",
    trigger: "webhook",
    isAIPowered: false,
    integrations: [
      "Gmail",
      "Notion",
      "Slack",
      "Google Sheets",
    ],
    tags: [
      "Onboarding",
      "Client Success",
      "Email Sequences",
    ],
    nodes: [
      "Webhook Trigger",
      "Send Welcome Email",
      "Create Notion Page",
      "Wait 1 Day",
      "Send Getting Started Email",
      "Wait 2 Days",
      "Slack Account Manager Alert",
      "Wait 4 Days",
      "Send Check-in Email",
      "Log to Sheets",
    ],
    prerequisites: [
      "n8n instance",
      "Gmail account",
      "Notion integration with onboarding template database",
      "Slack workspace",
      "Google Sheets for completion log",
    ],
    credentials: [
      {
        node: "Gmail",
        type: "Gmail OAuth2",
        notes: "OAuth2 with gmail.send scope",
      },
      {
        node: "Notion",
        type: "Notion API",
        notes:
          "Internal integration token with database write access",
      },
      {
        node: "Slack",
        type: "Slack API",
        notes: "Bot token with chat:write scope",
      },
      {
        node: "Google Sheets",
        type: "Google OAuth2",
        notes: "OAuth2 with spreadsheets.append scope",
      },
    ],
    customization: [
      "Personalise each email template with your brand voice and product-specific onboarding steps",
      "Adjust Wait node durations to match your onboarding timeline",
      "Add a Calendly link in the Day 1 email for a kickoff call booking",
    ],
    githubPath:
      "templates/08-client-onboarding-sequence/workflow.json",
  },
  {
    id: "09",
    slug: "web-scraping-business-analysis",
    name: "Web Scraping Business Analysis & Outreach",
    description:
      "Scrape Google for prospects, analyse tech stacks with AI, and generate personalised outreach emails.",
    fullDescription:
      "A powerful manually-triggered workflow targeting 3 niches per week across global markets. Searches Google via SerpAPI for businesses with missing or outdated websites, enriches each prospect with BuiltWith tech analysis, feeds everything to Claude AI for scoring and personalised email copy, stores 10+ leads per niche in Google Sheets, and queues outreach emails for your review. Run weekly to build 30-40 qualified prospects per month.",
    trigger: "manual",
    isAIPowered: true,
    integrations: [
      "Google Sheets",
      "Gmail",
      "SerpAPI",
      "Anthropic",
      "BuiltWith",
    ],
    tags: [
      "AI",
      "Web Scraping",
      "Lead Generation",
      "Outreach",
      "Sales Intelligence",
    ],
    nodes: [
      "Manual Trigger",
      "Set Config (niche/region)",
      "SerpAPI Google Search",
      "Parse Search Results",
      "Loop Over Businesses",
      "BuiltWith Tech Analysis",
      "Score Website Quality",
      "Has Website?",
      "Compile Lead Profile",
      "Store in Google Sheets",
      "Generate Outreach Email (AI)",
      "Queue for Review",
    ],
    prerequisites: [
      "n8n instance (self-hosted recommended for volume)",
      "SerpAPI account and API key (serpapi.com)",
      "BuiltWith API key (builtwith.com)",
      "Anthropic API key stored in n8n Header Auth credential",
      "Google Sheets with 18-column lead tracker template",
      "Gmail account for outreach",
    ],
    credentials: [
      {
        node: "Google Sheets",
        type: "Google OAuth2",
        notes: "OAuth2 with spreadsheets read/write scope",
      },
      {
        node: "SerpAPI",
        type: "Header Auth",
        notes:
          "api_key: YOUR_SERPAPI_KEY as query parameter",
      },
      {
        node: "BuiltWith",
        type: "Header Auth",
        notes: "KEY: YOUR_BUILTWITH_KEY as query parameter",
      },
      {
        node: "HTTP Request (Claude)",
        type: "Header Auth",
        notes:
          "x-api-key: YOUR_ANTHROPIC_KEY | anthropic-version: 2023-06-01",
      },
      {
        node: "Gmail",
        type: "Gmail OAuth2",
        notes:
          "OAuth2 with gmail.compose scope for drafting outreach",
      },
    ],
    customization: [
      'Configure 3 niche keywords in the Set Config node (e.g. "dental clinic", "law firm", "restaurant")',
      "Set target_region to any country/city for global prospect targeting",
      "Edit the Claude prompt to adjust website scoring criteria and email tone",
      "Enable the Gmail node (disabled by default) only after reviewing AI-generated drafts",
      "Add a second workflow run on Thursdays with 3 different niches for 6 niches/week",
    ],
    githubPath:
      "templates/09-web-scraping-business-analysis/workflow.json",
  },
  {
    id: "10",
    slug: "b2b-lead-gen-pipeline",
    name: "B2B Lead Gen Pipeline",
    description:
      "Full-stack B2B pipeline: scrape Google Maps, score leads with AI, publish top prospects, and send outreach.",
    fullDescription:
      "An enterprise-grade, fully automated B2B lead generation engine. Pulls local businesses from Google Maps via Apify, enriches each with BuiltWith tech stack + PageSpeed score + Open PageRank authority, feeds all signals to a universal LLM router (DeepSeek, Anthropic, OpenAI, Groq — swap with 4 env vars), scores leads across 5 dimensions (tech, SEO, brand, sales readiness, expansion), filters local businesses, ranks by score, publishes top prospects to a Vercel-hosted HTML page, appends to Google Sheets, and sends personalised outreach emails — with a circuit breaker for error resilience.",
    trigger: "schedule",
    isAIPowered: true,
    integrations: [
      "Google Sheets",
      "Gmail",
      "Apify",
      "Anthropic",
      "BuiltWith",
      "Vercel",
      "PageSpeed",
    ],
    tags: [
      "AI",
      "B2B",
      "Lead Generation",
      "Web Scraping",
      "Sales Intelligence",
      "Automation",
    ],
    nodes: [
      "Schedule Trigger",
      "Load Config from Sheets",
      "Apify Google Maps Actor",
      "Poll Apify Dataset",
      "BuiltWith Tech Stack",
      "PageSpeed Insights",
      "Open PageRank",
      "LLM Router (Universal)",
      "Score Lead (5 Dimensions)",
      "Accumulate & Rank Top N",
      "Circuit Breaker",
      "Publish to Vercel",
      "Append to Google Sheets",
      "Send Outreach Email",
      "Log Errors",
    ],
    prerequisites: [
      "n8n instance (self-hosted with docker-compose.yml included)",
      "Apify account + token (apify.com)",
      "BuiltWith API key (builtwith.com)",
      "PageSpeed Insights API key (free, Google Cloud Console)",
      "Open PageRank API key (free, domcop.com/openpagerank)",
      "LLM API key: DeepSeek (recommended), Anthropic, OpenAI, Groq, or Moonshot",
      "Google Sheets with 3-tab schema (Config, Leads, Errors)",
      "Vercel account + token for HTML publishing (optional)",
    ],
    credentials: [
      {
        node: "Google Sheets",
        type: "Google OAuth2",
        notes: "OAuth2 with spreadsheets read/write scope",
      },
      {
        node: "Apify HTTP nodes",
        type: "Header Auth",
        notes: "Authorization: Bearer YOUR_APIFY_TOKEN",
      },
      {
        node: "LLM Router (Code node)",
        type: "n8n Variables",
        notes:
          "Set LLM_PROVIDER, LLM_BASE_URL, LLM_MODEL, LLM_API_KEY in .env / docker-compose",
      },
      {
        node: "Gmail",
        type: "Gmail OAuth2",
        notes: "OAuth2 with gmail.send scope",
      },
    ],
    customization: [
      "Swap LLM provider by changing 4 env vars: LLM_PROVIDER, LLM_BASE_URL, LLM_MODEL, LLM_API_KEY",
      "Tune MAX_LEADS_FETCHED (default 30) and TOP_LEADS_KEPT (default 10) in .env",
      "Edit the 5-dimension scoring prompt to weight criteria for your ideal customer profile",
      "Set SCORE_THRESHOLD to filter out low-quality leads before outreach",
      "Disable Vercel publishing node if you only need Sheets + email output",
    ],
    githubPath:
      "templates/10-b2b-lead-gen-pipeline/workflow.json",
  },
];
