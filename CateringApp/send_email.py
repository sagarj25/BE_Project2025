import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

def sendemail(receiver_email, subject, message):
    # SMTP server configuration
    smtp_server = settings.EMAIL_SMTP_SERVER
    smtp_port = settings.EMAIL_PORT

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_HOST
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add message body
    msg.attach(MIMEText(message, 'html'))

    try:
        # Create an SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS for security
            server.starttls()

            # Login to the email account
            server.login(settings.EMAIL_HOST, settings.EMAIL_HOST_PASSWORD)

            # Send email
            server.send_message(msg)

        print('Email sent successfully!')
        return True
    except smtplib.SMTPException as e:
        print('Error: Unable to send email.')
        print(str(e))
        return False

# # Usage example
# sender_email = 'your_email@example.com'
# sender_password = 'your_password'
# receiver_email = 'recipient@example.com'
# subject = 'Hello from Python!'
# message = 'This is a test email sent using Python.'
# send_email(receiver_email, subject, message)
