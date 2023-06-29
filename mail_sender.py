import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(receiver_email:str, code: str):
    _from = "aaa@mail.ru"
    _from_pass = "STRONGpassword"
    message = f"""\
    # Subject: Hi from our the best service ever

    # Type this code to verify your email: {code}"""
    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login(_from,_from_pass)
    smtpObj.sendmail(_from, receiver_email, message)