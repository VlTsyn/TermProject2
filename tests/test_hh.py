from unittest.mock import Mock, patch

import pytest

from src.hh import HH


@pytest.fixture
def mock_vacancies_response():
    return {
        "items": [
            {
                "id": "125314150",
                "name": "Junior Java-разработчик",
                "url": "https://api.hh.ru/vacancies/125314150?host=hh.ru",
                "salary": {"from": 80000, "to": 100000, "currency": "RUB"},
                "snippet": {
                    "requirement": "Знание <highlighttext>Java</highlighttext> Core, понимание ООП. Опыт с Spring \n"
                    "/ Spring Boot — на практике или учебных проектах. Знакомство с REST API, RPC...",
                    "responsibility": "Участвовать в разработке и доработке backend-функционала на \n"
                    "<highlighttext>Java</highlighttext>. Исправлять баги, писать простые фичи \n"
                    "под руководством наставника. Писать чистый и...",
                },
            },
            {
                "id": "125317422",
                "name": "Backend-разработчик (Python\\Golang)",
                "url": "https://api.hh.ru/vacancies/125317422?host=hh.ru",
                "salary": {"from": 90000, "to": 105000, "currency": "RUB"},
                "snippet": {
                    "requirement": "Желания постоянно улучшить продукт. Будет плюсом: Знание языка Go, понимание \n"
                    "как работают каналы и горутины. Знание языка <highlighttext>Java</highlighttext>.",
                    "responsibility": "Разработка новых функций. Разработка RESTful сервисов. Настройка и \n"
                    "оптимизация PostgreSQL. Проектирование архитектуры. Развертывание сервисов \n"
                    "на серверах (Виртуальных машинах). ",
                },
            },
        ]
    }


@patch("requests.get")
def test_load_vacancies(mock_get, mock_vacancies_response):
    mock_response = Mock()
    mock_response.json.return_value = mock_vacancies_response
    mock_get.return_value = mock_response

    hh = HH()
    result = hh.load_vacancies("")
    assert len(result) == 4
    assert result[0]["name"] == "Junior Java-разработчик"
    assert result[1]["id"] == "125317422"
    assert hh.params["page"] == 2
