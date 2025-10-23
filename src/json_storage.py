import json
from typing import List

from src.base_storage import BaseStorage
from src.vacancy import Vacancy


class JsonStorage(BaseStorage):

    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_vacancies(self, keywords: str | List) -> List[dict]:
        """Получение вакансий из файла по ключу"""
        data = self._load()
        result = []
        if isinstance(keywords, str):
            keywords = [keywords]
        for item in data:
            for keyword in keywords:
                if keyword.lower() in item["name"].lower():
                    result.append(item)
                    break
        return result

    def add_vacancies(self, vacancies: List[Vacancy]):
        """Добавление вакансий в файл"""
        data = self._load()
        data_ids = {item["id"] for item in data}
        for vacancy in vacancies:
            if vacancy.id not in data_ids:
                data.append(vacancy.to_dict())
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def delete_vacancies(self, keywords: str | List):
        """Удаление вакансий из файла по ключу"""
        data = self._load()
        result = []
        if isinstance(keywords, str):
            keywords = [keywords]
        for item in data:
            for keyword in keywords:
                if keyword.lower() in item["name"].lower():
                    break
            else:
                result.append(item)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False)

    def _load(self) -> List[dict]:
        """Получение данных из файла"""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                result = json.load(f)
            return result
        except FileNotFoundError:
            print("Файл не найден")
            return []
        except json.decoder.JSONDecodeError:
            return []
