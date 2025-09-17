from src.hh import HH
from src.json_storage import JsonStorage
from src.vacancy import Vacancy


def user_interface():
    """Функция взаимодействия с пользователем"""
    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий на hh.ru")
        print("2. Выход")

        choice = input("\nВведите номер действия: ").strip()

        if choice == "1":
            search_vacancies()

            continue_search_vacancies()

        elif choice == "2":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова")


def search_vacancies():
    """Поиск вакансий по запросу"""
    search = input("Введите поисковый запрос: ").strip()
    if not search:
        print("Запрос не может быть пустым!")
        return

    print("Ищем вакансии...")
    result = HH().load_vacancies(search)

    if not result:
        print("Вакансии не найдены!")
        return

    vacancies = [Vacancy.from_json(r) for r in result]
    storage = JsonStorage("data/vacancies.json")
    storage.add_vacancies(vacancies)

    print(f"По результатам поиска '{search}' найдено {len(result)} вакансий")
    print("1. Вывести результат")
    print("2. Продолжить")

    choice = input("\nВведите номер действия: ").strip()

    if choice == "1":
        for v in vacancies:
            print(v)
    elif choice == "2":
        return
    else:
        print("Неверный выбор. Попробуйте снова")


def continue_search_vacancies():
    """Функция-продолжение поиска"""
    print("1. Топ N вакансий по зарплате")
    print("2. Поиск по ключевым словам в описании")
    print("3. Выход")

    choice = input("\nВведите номер действия: ").strip()

    if choice == "1":
        top_vacancies()
    elif choice == "2":
        search_by_keywords()
    elif choice == "3":
        return
    else:
        print("Неверный выбор. Попробуйте снова")
        continue_search_vacancies()


def top_vacancies():
    """Вывод топ N вакансий по зарплате"""
    storage = JsonStorage("data/vacancies.json")
    data = storage.get_vacancies([""])
    vacancies = [Vacancy.from_json(d) for d in data]

    try:
        n = int(input("Сколько вакансий показать: ").strip())
        if n <= 0:
            print("Число должно быть положительным!")
            return
    except ValueError:
        print("Введите корректное число!")
        return

    vacancies_with_salary = [v for v in vacancies if v.avg_salary > 0]
    vacancies_with_salary.sort(key=lambda x: x.avg_salary, reverse=True)
    top_vacancies = vacancies_with_salary[:n]
    print(f"Топ {n} вакансий по зарплате:")
    for vacancy in top_vacancies:
        print(vacancy)


def search_by_keywords():
    """Поиск вакансий по ключевым словам в описании"""
    keywords_input = input("Введите ключевые слова через запятую: ").strip()
    if not keywords_input:
        print("Нужно ввести хотя бы одно ключевое слово!")
        return

    keywords = [k.strip().lower() for k in keywords_input.split(",")]

    storage = JsonStorage("data/vacancies.json")
    data = storage.get_vacancies(keywords)
    vacancies = [Vacancy.from_json(d) for d in data]

    if not vacancies:
        print("Вакансии не найдены!")
        return

    print(f"Вакансии с ключевыми словами: {', '.join(keywords)}")
    for vacancy in vacancies:
        print(vacancy)
