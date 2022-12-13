from abc import ABC, abstractmethod
from datetime import datetime


class StarWarsDataAdapter(ABC):

    @abstractmethod
    def data_adapter(self, **kwargs):
        pass


class StarWarsPeopleAdapter(StarWarsDataAdapter):

    def data_adapter(self, people_data: list[dict], planets_data: list[dict]) -> list[dict]:
        required_people_data = []
        planets = self.get_dict_with_planets(planets_data=planets_data)
        for person in people_data:
            self.add_date_column(person=person)
            self.change_homeworld_column(person=person, planets=planets)
            required_person_columns = self.drop_columns(person)
            required_people_data.append(required_person_columns)
        return required_people_data

    def get_dict_with_planets(self, planets_data: list[dict]) -> dict:
        planets = {}
        for planet in planets_data:
            planets[planet['url']] = planet['name']
        return planets

    def add_date_column(self, person: dict):
        edited_column = person['edited']
        datetime_object = datetime.strptime(edited_column, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_column_format = datetime_object.strftime('%Y-%m-%d')
        person['date'] = date_column_format

    def change_homeworld_column(self, person: dict, planets: dict):
        person['homeworld'] = planets[person['homeworld']]

    def drop_columns(self, person: dict) -> dict:
        required_columns = ['name', 'height', 'mass', 'hair_color', 'skin_color',
                            'eye_color', 'birth_year', 'gender', 'homeworld', 'date']
        return {key: value for key, value in person.items() if key in required_columns}
