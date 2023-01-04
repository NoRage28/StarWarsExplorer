from requests import request, Response


class StarWarsApiClient:
    people_url = 'https://swapi.py4e.com/api/people/'
    planets_url = 'https://swapi.py4e.com/api/planets/'

    @staticmethod
    def client(method: str, url: str, headers: dict, data: dict) -> Response:
        return request(method=method, url=url, headers=headers, data=data)

    def get_people(self):
        people_data = []
        url = self.people_url
        while True:
            response = self.client(method='get', url=url, headers={}, data={}).json()
            people_data.extend(response['results'])
            if response['next'] is None:
                break
            url = response['next']
        return people_data

    def get_planets(self):
        planets_data = []
        url = self.planets_url
        while True:
            response = self.client(method='get', url=url, headers={}, data={}).json()
            planets_data.extend(response['results'])
            if response['next'] is None:
                break
            url = response['next']
        return planets_data
