import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import settings


def send_verification_email(
        email:str,
        first_name:str,
        code:str
):
    message = MIMEMultipart()

    message['From'] = f"Note App <{settings.SMTP_EMAIL}>"
    message['To'] = email
    message['Subject'] = "Verify your Email Address for Note App "

    body = f"""
<html>
<body>

<p>Hello <b>{first_name}</b>,</p>

<p>
Thank you for registering with Note App!

</p>

<h1>{code}</h1>

<p>
This code expires in 30 minutes.
</p>


</body>
</html>
"""

    message.attach(
        MIMEText(body, "html")
    )

    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            settings.SMTP_EMAIL,
            settings.SMTP_PASSWORD
        )

        print("the email is sending")

        server.send_message(message)

        print('the email is sent ')