import smtplib, ssl
from email.message import EmailMessage

def Send_email(
    host = 'smtp.gmail.com',
    port = 587,
    user = 'example@gmail.com', # gmail account
    password = 'password', # google app pass
    use_ssl = True,
    
    to = 'martinezesau90@gmail.com', # your email
    subject = 'orion alert',
    text = 'face recognized',
    ):
        
    msg = EmailMessage()
    msg.set_content(text)
    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = user
    if use_ssl:
        context = ssl.create_default_context()
	
    with smtplib.SMTP(host, port=port) as smtp:
        if use_ssl:
            smtp.starttls(context=context)
        smtp.login(msg['From'], password)# user , google-app-pass
        smtp.send_message(msg)
        return True

if __name__ == '__main__':
    Send_email()
