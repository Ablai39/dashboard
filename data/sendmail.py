import smtplib
import quopri
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def QuoHead(String):
    s = quopri.encodestring(String.encode('UTF-8'), 1, 0)
    return "=?utf-8?Q?" + s.decode('UTF-8') + "?="

host = "mail.halykbank.nb"
port = 587
sender = "ccmon@halykbank.nb"
subject = "Monitoring Service Level"
toList = ["didark@halykbank.kz", "DARHANBU@halykbank.kz"]

msg = MIMEMultipart()
msg["From"] = ("Служба мониторинга Контакт-центра").replace('=\n', '')
msg["To"] = ("didark@halykbank.kz").replace('=\n', '')
msg["Subject"] = QuoHead("Внимание. Service Level равен 72 %").replace('=\n', '')
textEmail = """ Привет
        Тест"""
html = """\
    <html>
        <body>
            <p>Привет!<br> Как у Вас <strong>дела</strong></p>
        </body>
    </html>
    """

text = MIMEText(html.encode('utf-8'), 'html', _charset='UTF-8')
msg.attach(text)


smtpObj = smtplib.SMTP(host, 587)



smtpObj.starttls()
smtpObj.login(sender,'sVtVo9Bk105LgQg1')
smtpObj.sendmail(sender, toList, msg.as_string())
smtpObj.quit()