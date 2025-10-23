import requests

from src.base_api import BaseAPI


class HH(BaseAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 10}
        self.vacancies = []

    def load_vacancies(self, keyword: str):
        self.params["text"] = keyword
        while self.params.get("page") != 2:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()["items"]
            self.vacancies.extend(vacancies)
            self.params["page"] += 1
        return self.vacancies
