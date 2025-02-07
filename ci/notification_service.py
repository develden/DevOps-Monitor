import smtplib
import requests
import logging
from email.mime.text import MIMEText
import os

logger = logging.getLogger(__name__)

def send_email_notification(email_to, subject, message, smtp_host='smtp.example.com', smtp_port=587, username='user@example.com', password='password'):
    """
    Отправка email уведомления через SMTP.
    Параметры SMTP берутся из переменных окружения, если они заданы.
    """
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = email_to
    try:
        smtp_host = os.getenv('SMTP_HOST', smtp_host)
        smtp_port = int(os.getenv('SMTP_PORT', smtp_port))
        username = os.getenv('SMTP_USERNAME', username)
        password = os.getenv('SMTP_PASSWORD', password)

        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        server.starttls()
        server.login(username, password)
        server.sendmail(username, [email_to], msg.as_string())
        server.quit()
        logger.info("Email notification sent successfully")
        return True
    except Exception as e:
        logger.error(f"Email notification failed: {e}")
        return False

def send_slack_notification(webhook_url, message):
    """
    Отправка уведомления в Slack через webhook.
    webhook_url берется из переменной окружения SLACK_WEBHOOK_URL, если задана.
    """
    payload = {"text": message}
    try:
        webhook_url = os.getenv('SLACK_WEBHOOK_URL', webhook_url)
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        logger.info("Slack notification sent successfully")
        return True
    except Exception as e:
        logger.error(f"Slack notification failed: {e}")
        return False

def send_telegram_notification(bot_token, chat_id, message):
    """
    Отправка уведомления в Telegram через Bot API.
    Параметры bot_token и chat_id берутся из переменных окружения TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID, если заданы.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN', bot_token)
        chat_id = os.getenv('TELEGRAM_CHAT_ID', chat_id)
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info("Telegram notification sent successfully")
        return True
    except Exception as e:
        logger.error(f"Telegram notification failed: {e}")
        return False

def send_notification(notification_obj):
    """
    Отправка уведомления на основе типа уведомления (email, slack, telegram).
    Объект notification_obj должен быть экземпляром модели Notification.
    После отправки обновляется флаг is_sent.
    """
    message = f"Уведомление по {notification_obj.pipeline.name}: {notification_obj.message}"
    success = False
    if notification_obj.notif_type == 'email':
        # Пример: указаны получатель и SMTP-настройки.
        success = send_email_notification(
            email_to="recipient@example.com",
            subject="DevOps Monitor Alert",
            message=message
        )
    elif notification_obj.notif_type == 'slack':
        # Пример: укажите свой Slack webhook URL.
        success = send_slack_notification(
            webhook_url="https://hooks.slack.com/services/SLACK/WEBHOOK/URL",
            message=message
        )
    elif notification_obj.notif_type == 'telegram':
        # Пример: укажите свой Telegram Bot Token и Chat ID.
        success = send_telegram_notification(
            bot_token="TELEGRAM_BOT_TOKEN",
            chat_id="TELEGRAM_CHAT_ID",
            message=message
        )
    # Обновление статуса уведомления в БД
    notification_obj.is_sent = success
    notification_obj.save()
    return success 