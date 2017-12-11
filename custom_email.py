import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class customEmail:
    def __init__(self):
        self.username = 'USERNAME'
        self.password = 'PASSWORD'
        self.msg = MIMEMultipart('mixed')
        self.sender = 'sender@example.com'
        self.mailServer = smtplib.SMTP('mail.smtp2go.com', 2525)  # 8025, 587 and 25 can also be used.
        self.mailServer.login(self.username, self.password)


    def sendEmail(self, recipient, template):
        msg['Subject'] = template.subject
        msg['From'] = self.sender
        msg['To'] = recipient

        text_message = MIMEText(template.body, 'plain')
        msg.attach(text_message)
        self.mailServer.sendmail(sender, recipient, msg.as_string())

    def close(self):
        self.mailServer.close()
