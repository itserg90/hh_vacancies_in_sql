import psycopg2

from src.class_dbmanager import DBManager
from src.functions import create_database, save_data_to_database
from src.class_company import Company
from src.class_vacancy import Vacancy


def drop_database(name, params):
    """Удаляет тестовую базу данных"""
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {name}")
    conn.close()


def test_cast_to_object_company(dict_company):
    current_dict = Company.cast_to_object_list(dict_company)
    assert current_dict['test_1'].name == 'test_1'


def test_cast_to_object_vacancy(dict_vacancy):
    current_dict = Vacancy.cast_to_object_list(dict_vacancy)
    assert current_dict['test_1'][0].name == 'vac_1'


def test_create_and_save_to_database(data_company, data_vacancy, get_database_name, get_params):
    def get_company_and_vacancy():
        """Получаем имя компании и вакансии из тестовой базы данных"""
        try:
            with psycopg2.connect(dbname=get_database_name, **get_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT companies.name, vacancies.name FROM companies
                        JOIN vacancies USING(id_company)
                    """)
                    return cur.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    create_database(get_database_name, get_params)
    save_data_to_database(data_company, data_vacancy, get_database_name, get_params)
    assert get_company_and_vacancy() == ('com_1', 'vac_1')
    drop_database(get_database_name, get_params)


def test_get_companies_and_vacancies_count_dbmanager(data_company, data_vacancy, get_database_name, get_params):

    create_database(get_database_name, get_params)
    save_data_to_database(data_company, data_vacancy, get_database_name, get_params)
    db = DBManager(get_database_name, get_params)
    assert db.get_companies_and_vacancies_count()[0] == ('com_1', 1)
    db.get_all_vacancies()
    drop_database(get_database_name, get_params)


def test_get_all_vacancies_dbmanager(data_company, data_vacancy, get_database_name, get_params):
    create_database(get_database_name, get_params)
    save_data_to_database(data_company, data_vacancy, get_database_name, get_params)
    db = DBManager(get_database_name, get_params)
    assert db.get_all_vacancies()[0] == ('com_1', 'vac_1', 100, 'http_url_1')
    drop_database(get_database_name, get_params)


def test_get_avg_salary_dbmanager(data_company, data_vacancy, get_database_name, get_params):
    create_database(get_database_name, get_params)
    save_data_to_database(data_company, data_vacancy, get_database_name, get_params)
    db = DBManager(get_database_name, get_params)
    assert int(db.get_avg_salary()) == 150
    drop_database(get_database_name, get_params)


def test_get_vacancies_with_higher_salary_dbmanager(data_company, data_vacancy, get_database_name, get_params):
    create_database(get_database_name, get_params)
    save_data_to_database(data_company, data_vacancy, get_database_name, get_params)
    db = DBManager(get_database_name, get_params)
    assert db.get_vacancies_with_higher_salary() is None
    drop_database(get_database_name, get_params)


def test_get_vacancies_with_keyword_dbmanager(data_company, data_vacancy, get_database_name, get_params):
    create_database(get_database_name, get_params)
    save_data_to_database(data_company, data_vacancy, get_database_name, get_params)
    db = DBManager(get_database_name, get_params)
    assert db.get_vacancies_with_keyword('vac_1') is None
    drop_database(get_database_name, get_params)
