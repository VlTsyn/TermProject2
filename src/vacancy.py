class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, id, name, url, salary_from, salary_to, currency, requirement, responsibility):
        self.id = id
        self.name = name
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.avg_salary = self._calculate_avg_salary()
        self.currency = currency
        self.requirement = requirement
        self.responsibility = responsibility

    def __str__(self):
        return f"Вакансия: {self.name} | Зарплата: {self.get_salary_info()}"

    def _calculate_avg_salary(self):
        """Вычисление среднего значения зарплаты"""
        if self.salary_from is not None and self.salary_to is not None:
            return (self.salary_from + self.salary_to) / 2
        elif self.salary_from is not None:
            return self.salary_from
        elif self.salary_to is not None:
            return self.salary_to
        else:
            return 0

    def get_salary_info(self):
        """Информация по зарплате"""
        if self.avg_salary == 0:
            return "Зарплата не указана"

        salary_info = ""
        if self.salary_from is not None:
            salary_info += f"от {self.salary_from}"
        if self.salary_to is not None:
            if salary_info:
                salary_info += " "
            salary_info += f"до {self.salary_to}"
        if self.currency is None:
            self.currency = ""

        return f"{salary_info} {self.currency}"

    """Методы сравнения вакансий по зарплате"""
    def __eq__(self, other):
        return self.avg_salary == other.avg_salary

    def __lt__(self, other):
        return self.avg_salary < other.avg_salary

    def __gt__(self, other):
        return self.avg_salary > other.avg_salary

    def to_dict(self):
        """Перевод вакансии в формат словаря"""
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "salary": {"from": self.salary_from, "to": self.salary_to, "currency": self.currency},
            "snippet": {"requirement": self.requirement, "responsibility": self.responsibility},
        }

    @classmethod
    def from_json(cls, data: dict):
        """Перевод вакансии из формата json"""
        if data.get("salary") is None:
            salary_from = None
            salary_to = None
            currency = None
        else:
            salary_from = data.get("salary").get("from")
            salary_to = data.get("salary").get("to")
            currency = data.get("salary").get("currency")
        id = data.get("id")
        name = data.get("name")
        url = data.get("url")
        requirement = data.get("snippet").get("requirement")
        responsibility = data.get("snippet").get("responsibility")

        return cls(
            id=id,
            name=name,
            url=url,
            salary_from=salary_from,
            salary_to=salary_to,
            currency=currency,
            requirement=requirement,
            responsibility=responsibility,
        )
