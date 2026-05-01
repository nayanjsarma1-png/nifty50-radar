import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
load_dotenv()
class Email:
    def __init__(self):

        self.MY_EMAIL = os.environ["MY_EMAIL"]
        self.PASSWORD = os.environ["PASSWORD"]
        self.RECIPIENT = os.environ["RECIPIENT"]


    def message(self,news_body):
        msg = MIMEMultipart()
        msg["From"] = self.MY_EMAIL
        msg["To"] = self.RECIPIENT
        msg["Subject"] = "Breakout Stocks "

        body = news_body

        msg.attach(MIMEText(body, "plain"))
        return msg

    def send_mail(self,news_body):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
            connection.login(user=self.MY_EMAIL, password=self.PASSWORD)
            connection.sendmail(
                from_addr=self.MY_EMAIL,
                to_addrs=self.RECIPIENT,
                msg=self.message(news_body).as_string()
            )

