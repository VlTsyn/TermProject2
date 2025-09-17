import json
from unittest.mock import patch

import pytest

from src.hh import HH
from src.interface import (
    continue_search_vacancies,
    search_by_keywords,
    search_vacancies,
    top_vacancies,
    user_interface,
)
from src.json_storage import JsonStorage


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


def test_search_vacancies(capsys, vacancies, tmp_file):
    with patch.object(JsonStorage, "__init__", lambda self, filepath: setattr(self, "filepath", tmp_file)):
        with patch("builtins.input", return_value=""):
            search_vacancies()
            result = capsys.readouterr()
            assert "Запрос не может быть пустым!" in result.out
        with patch.object(HH, "load_vacancies", return_value=[]) as mock_load:
            with patch("builtins.input", return_value="wertyu"):
                search_vacancies()
                mock_load.assert_called_once_with("wertyu")
                result = capsys.readouterr()
                assert "Вакансии не найдены!" in result.out
        with patch.object(HH, "load_vacancies", return_value=vacancies) as mock_load:
            with patch("builtins.input", side_effect=["java", "1"]):
                search_vacancies()
                mock_load.assert_called_once_with("java")
                result = json.loads(tmp_file.read_text(encoding="utf-8"))
                assert len(result) == 4
                capture = capsys.readouterr()
                assert "Вакансия: Java Developer" in capture.out
            mock_load.reset_mock()
            with patch("builtins.input", side_effect=["java", "2"]):
                search_vacancies()
                mock_load.assert_called_once_with("java")
                result = json.loads(tmp_file.read_text(encoding="utf-8"))
                assert len(result) == 4
                capture = capsys.readouterr()
                assert "Продолжить" in capture.out
            mock_load.reset_mock()
            with patch("builtins.input", side_effect=["java", "3"]):
                search_vacancies()
                mock_load.assert_called_once_with("java")
                result = json.loads(tmp_file.read_text(encoding="utf-8"))
                assert len(result) == 4
                capture = capsys.readouterr()
                assert "Неверный выбор. Попробуйте снова" in capture.out


def test_continue_search_vacancies(capsys):
    with patch("src.interface.top_vacancies") as mock_top:
        with patch("builtins.input", return_value="1"):
            continue_search_vacancies()
            mock_top.assert_called_once_with()
    with patch("src.interface.search_by_keywords") as mock_key:
        with patch("builtins.input", return_value="2"):
            continue_search_vacancies()
            mock_key.assert_called_once_with()
    with patch("builtins.input", side_effect=["4", "3"]):
        continue_search_vacancies()
        capture = capsys.readouterr()
        assert "Неверный выбор. Попробуйте снова" in capture.out


def test_top_vacancies(capsys, tmp_file, vacancies):
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False)
    with patch.object(JsonStorage, "__init__", lambda self, filepath: setattr(self, "filepath", tmp_file)):
        with patch("builtins.input", return_value="-1"):
            top_vacancies()
            capture = capsys.readouterr()
            assert "Число должно быть положительным!" in capture.out
        with patch("builtins.input", return_value="qwe"):
            top_vacancies()
            capture = capsys.readouterr()
            assert "Введите корректное число!" in capture.out
        with patch("builtins.input", return_value="1"):
            top_vacancies()
            capture = capsys.readouterr()
            assert (
                "Вакансия: Backend-разработчик (Python\\Java) | Зарплата: до 100000 RUB"
                and "Топ 1 вакансий по зарплате:" in capture.out
            )
        with patch("builtins.input", return_value="3"):
            top_vacancies()
            capture = capsys.readouterr()
            assert (
                "Вакансия: Java Developer (Trainee) | Зарплата: от 80000 до 100000"
                and "Топ 3 вакансий по зарплате:" in capture.out
            )


def test_search_by_keywords(capsys, tmp_file, vacancies):
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False)
    with patch.object(JsonStorage, "__init__", lambda self, filepath: setattr(self, "filepath", tmp_file)):
        with patch("builtins.input", return_value=""):
            search_by_keywords()
            capture = capsys.readouterr()
            assert "Нужно ввести хотя бы одно ключевое слово!" in capture.out
        with patch("builtins.input", return_value="java"):
            search_by_keywords()
            result = vacancies
            assert len(result) == 4
        with patch("builtins.input", return_value="qwertry"):
            search_by_keywords()
            capture = capsys.readouterr()
            assert "Вакансии не найдены!" in capture.out


def test_user_interface(capsys, tmp_file):
    with patch.object(JsonStorage, "__init__", lambda self, filepath: setattr(self, "filepath", tmp_file)):
        with patch("src.interface.search_vacancies"):
            with patch("builtins.input", side_effect=["java", "1", "3", "2"]):
                user_interface()
