import os
from abc import ABC, abstractmethod
from rest_framework.exceptions import APIException
from .models import Dataset
from django.core.files import File
import csv
from .clienst import StarWarsApiClient
from .adapters import StarWarsPeopleAdapter
from .utils import create_file_name
from django.conf import settings
from datetime import datetime

people_data = StarWarsApiClient().get_people()
planets_data = StarWarsApiClient().get_planets()


class DataWriterAndDBSaver(ABC):
    file_name = None

    def write_data_and_save_to_db(self, data):
        self._write_data_to_file(data=data)
        self._save_file_to_db_and_remove_from_disk()

    @abstractmethod
    def _write_data_to_file(self, data):
        pass

    @abstractmethod
    def _save_file_to_db_and_remove_from_disk(self):
        pass


class CSVDataWriterAndDBSaver(DataWriterAndDBSaver):

    def __init__(self):
        self.file_name = create_file_name()

    def write_data_and_save_to_db(self, data: list[dict]):
        self._write_data_to_file(data=data)
        self._save_file_to_db_and_remove_from_disk()

    def _write_data_to_file(self, data: list[dict]):
        to_csv = data
        keys = to_csv[0].keys()

        with open(f'{self.file_name}.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(to_csv)

    def _save_file_to_db_and_remove_from_disk(self):
        with open(f'{self.file_name}.csv', 'r') as csv_file:
            Dataset.objects.create(name=self.file_name, file=File(csv_file))

        os.remove(f'{self.file_name}.csv')


def get_required_data_to_write():
    required_data = StarWarsPeopleAdapter().data_adapter(people_data=people_data, planets_data=planets_data)
    return required_data


def read_data_from_csv(file_name: str) -> list[str]:
    file_url = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, f'datasets/{file_name}.csv')
    with open(f'{file_url}', 'r') as csv_file:
        file = csv_file.readlines()
    return file


def start_download_dataset_task():
    from .tasks import download_dataset_task
    try:
        cache_task_key = str(datetime.utcnow().timestamp())
        download_dataset_task.delay(cache_task_key)

    except Exception as exc:
        raise APIException(
            {"Import task error": exc.args},
        ) from exc
    return cache_task_key
