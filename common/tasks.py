from core import celery_app as celery
from celery.utils.log import get_task_logger
from .emails import send_registration_email

logger = get_task_logger(__name__)


@celery.task(name="send_registration_email_task")
def send_registration_email_task(email, message):
    logger.info("Registration email sent.")
    return send_registration_email(email, message)
