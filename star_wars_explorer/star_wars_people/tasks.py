from celery import shared_task
from .services import ImportStarwarsDataSet, CSVDataWriterAndDBSaver
from django.core.cache import cache
from .adapters import StarWarsPeopleAdapter
from .clienst import StarWarsApiClient


@shared_task()
def download_dataset_task(cache_task_id: str):
    try:
        cache.set(cache_task_id, {'is_importing': False, 'errors': []}, timeout=300)
        ImportStarwarsDataSet(client=StarWarsApiClient(), adapter=StarWarsPeopleAdapter(),
                              data_writer_service=CSVDataWriterAndDBSaver()).import_data()
    except Exception as exc:
        cache.set(cache_task_id, {'is_importing': False, 'errors': [exc.args]}, timeout=120)
    else:
        cache.set(cache_task_id, {'is_importing': True, 'errors': []}, timeout=120)
