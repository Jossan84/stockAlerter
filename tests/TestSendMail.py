
import os
import smtplib
import imghdr
from email.message import EmailMessage

contact = 'sanchezmosquerajosemanuel@gmail.com'
subject = 'Stock list report'
htmlMessage = """\
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:SlateGray;">This is an HTML Email!</h1>
        </body>
    </html>
    """


def sendEmail(contact, subject, htmlMessage):
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contact

    msg.add_alternative(htmlMessage, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

sendEmail(contact, subject, htmlMessage)