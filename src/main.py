from src.class_api import ApiVacanciesHh
from src.class_vacancy import Vacancy
from src.class_company import Company
from src.config import config
from src.functions import create_database, save_data_to_database
from src.class_dbmanager import DBManager


def main():
    api = ApiVacanciesHh()
    api.get_vacancies()

    database_name = 'hh_vacancies'

    vacancy_list = Vacancy.cast_to_object_list(api.hh_vacancies)

    company_list = Company.cast_to_object_list(api.hh_companies)

    create_database(database_name, config())
    save_data_to_database(company_list, vacancy_list, database_name, config())

    db = DBManager(database_name, config())
    db.get_companies_and_vacancies_count()
    db.get_all_vacancies()
    db.get_avg_salary()
    db.get_vacancies_with_higher_salary()
    job_name = input('Введите желаемую вакансию: ')
    db.get_vacancies_with_keyword(job_name)


if __name__ == '__main__':
    main()
