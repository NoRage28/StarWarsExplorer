from celery import shared_task, Celery
from .services import CSVDataWriterAndDBSaver


@shared_task()
def download_dataset_task():
    CSVDataWriterAndDBSaver().write_data_and_save_to_db()


# celery -A star_wars_explorer worker --loglevel=INFO

