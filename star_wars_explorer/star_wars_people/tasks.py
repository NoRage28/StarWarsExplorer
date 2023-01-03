from celery import shared_task
from .services import CSVDataWriterAndDBSaver, get_required_data_to_write
from django.core.cache import cache


@shared_task()
def download_dataset_task(cache_task_id: str):
    try:
        cache.set(cache_task_id, {'is_importing': False, 'errors': []}, timeout=300)
        data = get_required_data_to_write()
        CSVDataWriterAndDBSaver().write_data_and_save_to_db(data=data)
    except Exception as exc:
        cache.set(cache_task_id, {'is_importing': False, 'errors': [exc.args]}, timeout=120)
    else:
        cache.set(cache_task_id, {'is_importing': True, 'errors': []}, timeout=120)
