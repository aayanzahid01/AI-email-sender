from groq import Groq
import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

# ============================================================
#   SETTINGS — only thing you change per client
# ============================================================
YOUR_EMAIL        = ""
YOUR_APP_PASSWORD = ""
GROQ_API_KEY      = ""
SHEET_NAME        = "Email List"
YOUR_SERVICE      = "social media management"
# ============================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet_data():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet.get_all_records()

def generate_email(name, service):
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""Write a short, friendly, professional cold outreach email.

The sender offers: {service}
The recipient's name is: {name}

Rules:
- 3 short paragraphs maximum
- Sound human, not robotic
- End with a soft call to action (reply to learn more)
- No subject line, just the body
- Sign off as 'The Team'"""
            }
        ]
    )
    return response.choices[0].message.content

def send_emails():
    print("Running email automation...")
    rows = get_sheet_data()

    for row in rows:
        name  = row["Name"]
        email = row["Email"]

        body    = generate_email(name, YOUR_SERVICE)
        subject = f"Quick question for you, {name}"

        msg = MIMEMultipart()
        msg["From"]    = YOUR_EMAIL
        msg["To"]      = email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(YOUR_EMAIL, YOUR_APP_PASSWORD)
            server.sendmail(YOUR_EMAIL, email, msg.as_string())

        print(f"Sent to {name} at {email}")
        print(f"Email preview:\n{body}\n{'-'*40}")

    print("All done!")

# Runs once immediately, then every day at 09:00
send_emails()
schedule.every().day.at("09:00").do(send_emails)

while True:
    schedule.run_pending()
    time.sleep(60)