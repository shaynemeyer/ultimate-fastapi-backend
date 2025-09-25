from asgiref.sync import async_to_sync
from celery import Celery
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import db_settings, notification_settings
from app.utils import TEMPLATE_DIR

fast_mail = FastMail(
    ConnectionConfig(
        **notification_settings.model_dump(),
        TEMPLATE_FOLDER=TEMPLATE_DIR,
    )
)


send_message = async_to_sync(fast_mail.send_message)

app = Celery("api_tasks", broker=db_settings.REDIS_URL(9))


@app.task
def send_mail(recipients: list[str], subject: str, body: str):
    send_message(
        MessageSchema(
            recipients=recipients, subject=subject, body=body, subtype=MessageType.plain
        )
    )

    return "Message Sent!"


@app.task
def send_email_with_template(
    recipients: list[str],
    subject: str,
    context: dict,
    template_name: str,
):
    send_message(
        message=MessageSchema(
            recipients=recipients,
            subject=subject,
            template_body=context,
            subtype=MessageType.html,
        ),
        template_name=template_name,
    )
