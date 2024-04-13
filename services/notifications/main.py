from fastapi import FastAPI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from schemas import CreateEmail
import smtplib
from fastapi.responses import Response

app = FastAPI()

sender_email = "kharelgyanoo@gmail.com"
password = "bokn aptt mlbm ogvt"


@app.post("/notifications/email")
async def send_email(request: CreateEmail):

    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = request.to
        message["Subject"] = request.subject
        body = request.body
        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            text = message.as_string()
            server.sendmail(sender_email, request.to, text)
            return Response(status_code=200)

    except:
        return Response(status_code=400)