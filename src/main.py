from src.class_api import ApiVacanciesHh
from src.class_vacancy import Vacancy
from src.class_company import Company
from src.config import config
from src.functions import create_database, save_data_to_database
from src.class_dbmanager import DBManager


def main():
    api = ApiVacanciesHh()
    api.get_vacancies()
    # Название базы данных
    database_name = 'hh_vacancies'

    vacancy_list = Vacancy.cast_to_object_list(api.hh_vacancies)
    company_list = Company.cast_to_object_list(api.hh_companies)

    create_database(database_name, config())
    save_data_to_database(company_list, vacancy_list, database_name, config())

    db = DBManager(database_name, config())
    while True:
        print("Здравствуйте. Выберите действие и получите информацию о вакансиях.\n"
              "1. Получить список всех компаний и количество вакансий у каждой компании\n"
              "2. Получить список всех вакансий (название компании, название вакансии, зарплата и ссылка на вакансию)\n"
              "3. Получить среднюю зарплату по вакансиям\n"
              "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
              "5. Получить список всех вакансий, в названии которых содержится переданное слово\n"
              "0. Завершить программу\n")
        user_input = input("Введите цифру желаемого действия: \n")
        if user_input == '1':
            db.get_companies_and_vacancies_count()
        elif user_input == '2':
            db.get_all_vacancies()
        elif user_input == '3':
            db.get_avg_salary()
        elif user_input == '4':
            db.get_vacancies_with_higher_salary()
        elif user_input == '5':
            job_name = input('Введите желаемую вакансию: ')
            db.get_vacancies_with_keyword(job_name)
        elif user_input == '0':
            print("Спасибо. Всего хорошего!")
            break
        else:
            print("Введите корректный ответ")


if __name__ == '__main__':
    main()
