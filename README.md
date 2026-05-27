# ai-email-sender

Python automation tool that reads a contact list from Google Sheets,
generates a unique personalised email per contact via the Groq API,
and delivers each one through Gmail SMTP — on a daily automated schedule.

Built for service businesses that send regular outreach but don't want
to pay for expensive email marketing platforms.

## how it works
Google Sheets → Python → Groq API (LLaMA 3.3) → Gmail SMTP → inbox
1. Authenticates with Google Sheets API via service account
2. Pulls contact list from configured sheet
3. Calls Groq API to generate unique content per contact
4. Delivers via Gmail SMTP over SSL (port 465)
5. Repeats daily at 09:00 via schedule library

## tech

| layer | tool |
|---|---|
| language | Python 3.12 |
| sheet integration | gspread + google-auth |
| content generation | Groq API — llama-3.3-70b-versatile |
| delivery | Gmail SMTP — SSL port 465 |
| scheduling | schedule library |

## configuration

```python
YOUR_EMAIL        = ""  # Gmail address
YOUR_APP_PASSWORD = ""  # Gmail App Password
GROQ_API_KEY      = ""  # Groq API key
SHEET_NAME        = ""  # Google Sheet name
YOUR_SERVICE      = ""  # Business context for content generation
```

## sheet format

| Name | Email |
|---|---|
| Sarah Johnson | sarah@example.com |

## setup

```bash
git clone https://github.com/aayanzahid01/ai-email-sender
pip install gspread google-auth groq schedule
```

Add `credentials.json` from Google Cloud Console, fill settings block, run:

```bash
python email_sender.py
```

## notes
- `credentials.json` not included — generate from Google Cloud Console
- Sheets + Drive APIs must be enabled on your Google Cloud project
- Sheet must be shared with service account email
