import json

import pytest

from src.json_storage import JsonStorage
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


@pytest.fixture
def tmp_file(tmp_path):
    return tmp_path / "test_file.json"


@pytest.fixture
def tmp_storage(tmp_file):
    return JsonStorage(str(tmp_file))


@pytest.fixture
def vacancy_objs(vacancies):
    return [Vacancy.from_json(v) for v in vacancies]


@pytest.fixture
def new_vacancy():
    return [
        {
            "id": "7894656123",
            "name": "Java Developer (Trainee)",
            "url": "https://api.hh.ru/vacancies/125341679?host=hh.ru",
            "salary": {"from": 80000, "to": 100000, "currency": None},
            "snippet": {
                "requirement": "IT or technical education (students welcome!). English: Intermediate+. Solid \n"
                "knowledge of <highlighttext>Java</highlighttext> Core & SQL. Basic understanding \n"
                "of Spring Framework. ",
                "responsibility": "...foundation in <highlighttext>Java</highlighttext> programming and apply it \n"
                "to real-world projects. Design and improve applications using advanced \n"
                "<highlighttext>Java</highlighttext> features and...",
            },
        }
    ]


@pytest.fixture
def extra_vacancy(new_vacancy):
    return [Vacancy.from_json(v) for v in new_vacancy]


def test_load(tmp_file, tmp_storage, vacancies):
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False)
    data = tmp_storage._load()
    assert isinstance(data, list)
    assert data == vacancies


def test_filenotfound_error():
    storage = JsonStorage("filenotfound.json")
    data = storage._load()
    assert data == []


def test_decode_error(tmp_file, tmp_storage):
    tmp_file.write_text("{wqertethgjf", encoding="utf-8")
    data = tmp_storage._load()
    assert data == []


def test_add_vacancies(tmp_file, tmp_storage, vacancy_objs, extra_vacancy):
    tmp_storage.add_vacancies(vacancy_objs)
    with open(tmp_file, "r", encoding="utf-8") as f:
        data_1 = json.load(f)
    assert len(data_1) == 4

    tmp_storage.add_vacancies(extra_vacancy)
    with open(tmp_file, "r", encoding="utf-8") as f:
        data_2 = json.load(f)
    assert len(data_2) == 5


def test_get_vacancies(tmp_file, tmp_storage, vacancies):
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False)
    data = tmp_storage.get_vacancies("java")
    assert len(data) == 2


def test_delete_vacancies(tmp_file, tmp_storage, vacancies):
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False)
    tmp_storage.delete_vacancies("разработчик")
    with open(tmp_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
