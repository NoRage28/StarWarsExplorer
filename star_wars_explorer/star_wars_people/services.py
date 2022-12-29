import os
from abc import ABC, abstractmethod
from .models import Dataset
from django.core.files import File
import csv
from .clienst import StarWarsApiClient
from .adapters import StarWarsPeopleAdapter
from .utils import create_file_name
from django.conf import settings


class DataWriter(ABC):
    @abstractmethod
    def write_data_to_file(self, file_name, data):
        pass


class FileSaverToDatabase(ABC):
    @abstractmethod
    def save_file_to_db_and_remove_from_disk(self, file_name):
        pass


class CSVDataWriter(DataWriter):

    def write_data_to_file(self, file_name: str, data: list[dict]):
        to_csv = data
        keys = to_csv[0].keys()

        with open(f'{file_name}.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(to_csv)


class CSVFileSaverToDatabase(FileSaverToDatabase):

    def save_file_to_db_and_remove_from_disk(self, file_name: str):
        with open(f'{file_name}.csv', 'r') as csv_file:
            Dataset.objects.create(name=file_name, file=File(csv_file))

        os.remove(f'{file_name}.csv')


def download_and_save_required_data_to_db():
    people_data = StarWarsApiClient().get_people()
    planets_data = StarWarsApiClient().get_planets()
    required_data = StarWarsPeopleAdapter().data_adapter(people_data=people_data, planets_data=planets_data)
    file_name = create_file_name()
    CSVDataWriter().write_data_to_file(file_name=file_name, data=required_data)
    CSVFileSaverToDatabase().save_file_to_db_and_remove_from_disk(file_name=file_name)


def read_data_from_csv(file_name: str):
    file_url = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, f'datasets/{file_name}.csv')
    with open(f'{file_url}', 'r') as csv_file:
        file = csv_file.readlines()
    return file
