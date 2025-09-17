from abc import ABC, abstractmethod


class BaseStorage(ABC):

    @abstractmethod
    def get_vacancies(self, keyword):
        pass

    @abstractmethod
    def add_vacancies(self, vacancies):
        pass

    @abstractmethod
    def delete_vacancies(self, vacancies):
        pass
