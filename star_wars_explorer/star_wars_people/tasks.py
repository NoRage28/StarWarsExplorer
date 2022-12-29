from celery import shared_task
from .services import download_and_save_required_data_to_db


@shared_task()
def download_dataset_task():
    download_and_save_required_data_to_db()
