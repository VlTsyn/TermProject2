from abc import ABC, abstractmethod


class BaseAPI(ABC):

    @abstractmethod
    def load_vacancies(self, keyword):
        pass
