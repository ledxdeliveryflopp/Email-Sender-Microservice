import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.broker.service import get_user_email_from_broker
from jinja2 import Template
from src.settings.settings import settings


def create_template(sender_email: str, user_email: str):
    """Создание шаблона"""
    with open("src/smtp/templates/user_register.html", "r") as file:
        template_str = file.read()
    jinja_template = Template(template_str)
    data = {"subject": "Успешная регистрация", "greeting": "Текст заглушка",
            "message": f"Успешная завершенна регистрация аккауннта - {user_email}",
            "sender_email": f"Почта для связи с техподдержкой - {sender_email}"}
    email_content = jinja_template.render(data)
    msg = MIMEMultipart()
    msg.attach(MIMEText(email_content, "html"))
    return msg


async def send_message():
    """Отправка сообщения"""
    smtp_email = settings.smtp_settings.smtp_email_sender

    conf = smtplib.SMTP(settings.smtp_settings.smtp_service, settings.smtp_settings.smtp_port)
    conf.ehlo()
    conf.starttls()
    conf.login(smtp_email, settings.smtp_settings.smtp_email_secret)
    broker_data = await get_user_email_from_broker()
    if broker_data is None:
        return None
    user_email = str(broker_data, encoding="utf-8")
    user_email.replace('b', '')
    template = create_template(sender_email=smtp_email, user_email=user_email)
    conf.sendmail(smtp_email, user_email, template.as_string())
    conf.quit()
