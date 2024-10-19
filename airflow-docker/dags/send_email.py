import os
from email.message import EmailMessage
import ssl
import smtplib

email_sender = 'pruebasdevdata@gmail.com'   
email_password = os.environ.get("EMAIL_PASSWORD")
email_receiver = 'pruebasdevdata@gmail.com'

title = "ALERTA ! Items con demasiadas ventas"
body="""Hemos detectado nuevos items con demasiadas ventas {}""".format(data)

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = title
em.set_content(body)

context=ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())