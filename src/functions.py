import psycopg2

from typing import Dict, List
from src.class_company import Company
from src.class_vacancy import Vacancy


def create_database(database_name: str, params: dict) -> None:
    """Создаем базу данных и таблицы в ней"""
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()

    try:
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE companies (
                            id_company SERIAL,
                            name VARCHAR,
                            company_url VARCHAR  NOT NULL,
                            accredited_it_employer BOOLEAN,
                            CONSTRAINT pk_id_company PRIMARY KEY (id_company),
                            CONSTRAINT chk_company_url CHECK (company_url LIKE 'http%')
                        )
                """)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    try:
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE vacancies
                        (
                            id_vacancy INTEGER NOT NULL UNIQUE,
                            name VARCHAR,
                            id_company INTEGER REFERENCES companies(id_company) NOT NULL,
                            vacancy_url VARCHAR NOT NULL,
                            salary INTEGER,
                            city VARCHAR,
                            published_date DATE NOT NULL,
                            experience VARCHAR,
                            requirement TEXT,
                            CONSTRAINT chk_vacancy_url CHECK (vacancy_url LIKE 'http%')
                        )
                """)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def save_data_to_database(company_data: Dict[str, Company], vacancy_data: Dict[str, List[Vacancy]], database_name: str,
                          params: dict) -> None:
    """Сохраняем данные в таблицы базы данных"""
    try:
        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                if company_data:
                    for company_name, company_object in company_data.items():
                        cur.execute(
                            """
                            INSERT INTO companies (name, company_url, accredited_it_employer)
                            VALUES (%s, %s, %s)
                            RETURNING id_company
                            """,
                            (company_object.name, company_object.url, company_object.accredited_it_employer)
                        )
                        company_id = cur.fetchone()[0]
                        for vacancy_object in vacancy_data[company_name]:
                            if vacancy_data:
                                cur.execute(
                                    """
                                    INSERT INTO vacancies
                                    (id_vacancy, name, id_company, vacancy_url, salary,
                                    city, published_date, experience, requirement)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """,
                                    (vacancy_object.id, vacancy_object.name, company_id, vacancy_object.url,
                                     vacancy_object.salary, vacancy_object.city, vacancy_object.published_date,
                                     vacancy_object.experience, vacancy_object.requirement)
                                )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
