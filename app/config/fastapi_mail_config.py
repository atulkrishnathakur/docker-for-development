from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import BaseModel, EmailStr
from app.validation.email import EmailSchema
import os

# https://sabuhish.github.io/fastapi-mail/example/
# https://sabuhish.github.io/fastapi-mail/getting-started/

mailconf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS = True    
)

def send_email(
    background_tasks,
    emaiSubject,
    emailTo,
    emailBody,
    ccemail=[],
    bccemail=[],
    attachmentsList=[]
    ):
    fm = FastMail(mailconf)
    mailData = MessageSchema(
        subject=emaiSubject,
        recipients=emailTo,
        cc=ccemail,
        bcc=bccemail,
        body=emailBody,
        subtype=MessageType.html,
        attachments=attachmentsList
        )
   
    background_tasks.add_task(fm.send_message, mailData)