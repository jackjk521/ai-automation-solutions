# Invoice Automation

## What it does
Runs on the 1st of every month at 9 AM, pulls all active clients from a Google Sheet, generates a fully styled HTML invoice for each one, emails it directly from your billing address, and updates the sheet with the sent date, invoice number, and amount.

## Use case
Freelancers, agencies, and small businesses that bill clients on a recurring monthly basis and want to eliminate manual invoice creation and status tracking.

## Prerequisites
- n8n instance (self-hosted or cloud)
- Google account with Google Sheets and Gmail API access
- A Google Sheet set up with the client schema below

## How to import
1. Download `workflow.json`
2. Open n8n → **Workflows** → **Import from file**
3. Upload `workflow.json`
4. Configure credentials
5. Set `INVOICE_SHEET_ID` in **Settings → Variables**
6. Activate — fires on the 1st of next month at 9 AM

## Credentials to configure
| Node | Credential Type | Notes |
|---|---|---|
| Get Active Clients | Google Sheets OAuth2 | Authorize the Google account that owns the sheet |
| Update Invoice Status | Google Sheets OAuth2 | Same credential |
| Send Invoice Email | Gmail OAuth2 | Use the billing address you want clients to reply to |

## Google Sheets Schema
Create a sheet named **Clients** with these column headers:

| Column | Example |
|---|---|
| ClientName | Acme Corp |
| ClientEmail | accounts@acme.com |
| BillingAddress | 456 Oak St, New York, NY |
| MonthlyRate | 2500 |
| TaxRate | 0.1 |
| ServiceDescription | Monthly SEO Retainer |
| PaymentMethod | Bank Transfer |
| Active | TRUE |
| LastInvoiceDate | auto-filled |
| LastInvoiceNumber | auto-filled |
| InvoiceStatus | auto-filled |

## Customization
- **Change schedule:** Edit cron `0 9 1 * *` — e.g., `0 9 */2 * *` for every 2 months
- **Add line items:** Extend the HTML `<table>` in the Code node with extra `<tr>` rows mapped to sheet columns
- **PDF attachment:** Add an HTTP Request node calling Gotenberg or html2pdf.app after invoice generation

## Notes
- Set the server timezone correctly in n8n — or adjust the cron for UTC offset
- If `ClientEmail` is empty for any row, the loop errors; add an IF node to skip empty emails
- Google Sheets API allows ~300 read/write requests/minute — add a Wait node for 100+ clients
