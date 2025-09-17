import pytest

from src.vacancy import Vacancy


@pytest.fixture
def vacancies():
    return [
        {
            "id": "125314150",
            "name": "Junior Java-разработчик",
            "url": "https://api.hh.ru/vacancies/125314150?host=hh.ru",
            "salary": {"from": 90000, "to": None, "currency": "RUB"},
            "snippet": {
                "requirement": "Знание <highlighttext>Java</highlighttext> Core, понимание ООП. Опыт с Spring / \n"
                "Spring Boot — на практике или учебных проектах. Знакомство с REST API, RPC...",
                "responsibility": "Участвовать в разработке и доработке backend-функционала на \n"
                "<highlighttext>Java</highlighttext>. Исправлять баги, писать простые фичи \n"
                "под руководством наставника. Писать чистый и...",
            },
        },
        {
            "id": "125317422",
            "name": "Backend-разработчик (Python\\Java)",
            "url": "https://api.hh.ru/vacancies/125317422?host=hh.ru",
            "salary": {"from": None, "to": 100000, "currency": "RUB"},
            "snippet": {
                "requirement": "Желания постоянно улучшить продукт. Будет плюсом: Знание языка Go, понимание как \n"
                "работают каналы и горутины. Знание языка <highlighttext>Java</highlighttext>.",
                "responsibility": "Разработка новых функций. Разработка RESTful сервисов. Настройка и оптимизация \n"
                "PostgreSQL. Проектирование архитектуры. Развертывание сервисов на серверах \n"
                "(Виртуальных машинах). ",
            },
        },
        {
            "id": "125255595",
            "name": "Java-разработчик/Web-программист/Front End developer в Астане",
            "url": "https://api.hh.ru/vacancies/125255595?host=hh.ru",
            "salary": None,
            "snippet": {
                "requirement": "Обязательное знание: HTML, CSS, JS. Желательно знание CMS: October Cms, OpenCart, \n"
                "Joomla, Bitrix CMS. Умение изучать и разбираться с кодом.",
                "responsibility": "Выполнение заявок по техподдержке. Внесение правок в сайты. Доработка сайтов. \n"
                "Исправление ошибок.",
            },
        },
        {
            "id": "125341679",
            "name": "Java Developer (Trainee)",
            "url": "https://api.hh.ru/vacancies/125341679?host=hh.ru",
            "salary": {"from": 80000, "to": 100000, "currency": None},
            "snippet": {
                "requirement": "IT or technical education (students welcome!). English: Intermediate+. Solid \n"
                "knowledge of <highlighttext>Java</highlighttext> Core & SQL. Basic understanding \n"
                "of Spring Framework. ",
                "responsibility": "...foundation in <highlighttext>Java</highlighttext> programming and apply it to \n"
                "real-world projects. Design and improve applications using advanced \n"
                "<highlighttext>Java</highlighttext> features and...",
            },
        },
    ]


def test_vacancy_init(vacancies):
    result = [Vacancy.from_json(v) for v in vacancies]
    assert len(result) == 4
    assert result[0].name == "Junior Java-разработчик"
    assert result[3].id == "125341679"


def test_avg_salary(vacancies):
    result = [Vacancy.from_json(v) for v in vacancies]
    assert result[1].avg_salary == 100000
    assert result[2].salary_from is None
    assert result[2].salary_to is None
    assert result[2].avg_salary == 0
    assert result[3].avg_salary == 90000


def test_str(vacancies):
    result = [Vacancy.from_json(v) for v in vacancies]
    assert str(result[0]) == "Вакансия: Junior Java-разработчик | Зарплата: от 90000 RUB"
    assert str(result[1]) == "Вакансия: Backend-разработчик (Python\\Golang) | Зарплата: до 100000 RUB"
    assert (
        str(result[2])
        == "Вакансия: Веб-разработчик/Web-программист/Front End developer в Астане | Зарплата: Зарплата не указана"
    )
    assert str(result[3]) == "Вакансия: Java Developer (Trainee) | Зарплата: от 80000 до 100000 "


def test_compare(vacancies):
    result = [Vacancy.from_json(v) for v in vacancies]
    assert result[0] < result[1]
    assert result[1] > result[2]
    assert result[0] == result[3]


def test_to_dict(vacancies):
    result = [Vacancy.from_json(v) for v in vacancies]
    assert result[0].to_dict() == {
        "id": "125314150",
        "name": "Junior Java-разработчик",
        "url": "https://api.hh.ru/vacancies/125314150?host=hh.ru",
        "salary": {"from": 90000, "to": None, "currency": "RUB"},
        "snippet": {
            "requirement": "Знание <highlighttext>Java</highlighttext> Core, понимание ООП. Опыт с Spring / \n"
            "Spring Boot — на практике или учебных проектах. Знакомство с REST API, RPC...",
            "responsibility": "Участвовать в разработке и доработке backend-функционала на \n"
            "<highlighttext>Java</highlighttext>. Исправлять баги, писать простые фичи под \n"
            "руководством наставника. Писать чистый и...",
        },
    }
