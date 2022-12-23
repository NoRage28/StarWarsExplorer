import os
from abc import ABC, abstractmethod
from .models import Dataset
from django.core.files import File
import petl
from .clienst import StarWarsApiClient
from .adapters import StarWarsPeopleAdapter
from .utils import create_file_name
from django.conf import settings


class DataWriterAndDBSaver(ABC):
    file_name = None
    data_to_write = None

    def write_data_and_save_to_db(self):
        self._write_data_to_file()
        self._save_file_to_db_and_remove_from_disk()

    @abstractmethod
    def _write_data_to_file(self):
        pass

    @abstractmethod
    def _save_file_to_db_and_remove_from_disk(self):
        pass


class CSVDataWriterAndDBSaver(DataWriterAndDBSaver):

    def __init__(self):
        self.file_name = create_file_name()
        self.data_to_write = StarWarsPeopleDataExtractor().get_data_to_write()

    def write_data_and_save_to_db(self):
        self._write_data_to_file()
        self._save_file_to_db_and_remove_from_disk()

    def _write_data_to_file(self):
        data_to_write = self.data_to_write
        file_headers = data_to_write[0].keys()
        file = [file_headers]

        for row in data_to_write:
            row = [row[row_name] for row_name in file_headers]
            file.append(row)

        petl.tocsv(file, f'{self.file_name}.csv')

    def _save_file_to_db_and_remove_from_disk(self):
        with open(f'{self.file_name}.csv', 'r') as csv_file:
            Dataset.objects.get_or_create(name=self.file_name, file=File(csv_file))

        os.remove(f'{self.file_name}.csv')


class DataExtractor(ABC):
    client = None
    adapter = None

    @abstractmethod
    def get_data_to_write(self):
        pass


class StarWarsPeopleDataExtractor(DataExtractor):

    def __init__(self):
        self.client = StarWarsApiClient()
        self.adapter = StarWarsPeopleAdapter()

    def get_data_to_write(self) -> list[dict]:
        people_data = self.client.get_people()
        planets_data = self.client.get_planets()
        data = self.adapter.data_adapter(people_data=people_data, planets_data=planets_data)
        return data


def read_data_from_csv(file_name: str):
    file_url = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, f'datasets/{file_name}.csv')
    with open(f'{file_url}', 'r') as csv_file:
        file = csv_file.readlines()
    return file
