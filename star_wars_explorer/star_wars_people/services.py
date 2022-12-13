import os
from abc import ABC, abstractmethod
from .models import Dataset
from django.core.files import File
import petl
from .clienst import StarWarsApiClient
from .adapters import StarWarsPeopleAdapter
from .utils import create_file_name


class DataWriterAndDBSaver(ABC):
    file_name = None
    client = StarWarsApiClient()

    def write_data_and_save_to_db(self):
        self.write_data_to_file()
        self.save_file_to_db_and_remove_from_disk()

    @abstractmethod
    def write_data_to_file(self):
        pass

    @abstractmethod
    def save_file_to_db_and_remove_from_disk(self):
        pass


class CSVDataWriterAndDBSaver(DataWriterAndDBSaver):

    def __init__(self):
        self.file_name = create_file_name()
        self.adapter = StarWarsPeopleAdapter()

    def write_data_and_save_to_db(self):
        self.write_data_to_file()
        self.save_file_to_db_and_remove_from_disk()

    def write_data_to_file(self):
        data_to_write = self.adapter.data_adapter(people_data=self.client.get_people(),
                                                  planets_data=self.client.get_planets())
        file_headers = data_to_write[0].keys()
        file = [file_headers]

        for row in data_to_write:
            row = [row[row_name] for row_name in file_headers]
            file.append(row)

        petl.tocsv(file, f'{self.file_name}.csv')

    def save_file_to_db_and_remove_from_disk(self):
        with open(f'{self.file_name}.csv', 'r') as csv_file:
            Dataset.objects.get_or_create(name=self.file_name, file=File(csv_file))

        os.remove(f'{self.file_name}.csv')
