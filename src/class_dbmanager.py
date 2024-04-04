import os

import psycopg2


class DBManager:
    """Класс для взаимодействия с базой данных"""

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Получаем список всех компаний и количество вакансий у каждой компании"""
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT companies.name, COUNT(*) FROM companies
                        JOIN vacancies USING(id_company)
                        GROUP BY companies.name
                        ORDER BY companies.name
                    """)
                    current_list = []
                    for name, quantity in cur.fetchall():
                        current_list.append((name, quantity))
                        print(f"Компания {name}: {quantity} вакансий")
                    print("")
                    return current_list
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_all_vacancies(self):
        """
        Получаем список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
        """
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT companies.name, vacancies.name, vacancies.vacancy_url, vacancies.salary FROM companies
                        JOIN vacancies USING(id_company)
                        ORDER BY companies.name
                    """)
                    current_list = []
                    for number, (company_name, vacancy_name, url, salary) in enumerate(cur.fetchall(), 1):
                        if not salary:
                            salary = 'Зарплата не указана'
                        print(
                            f"{number}. Компания: {company_name}\n"
                            f"Вакансия: {vacancy_name}\n"
                            f"Зарплата: {salary}\n"
                            f"Ссылка: {url}\n")
                        current_list.append((company_name, vacancy_name, salary, url))
                    return current_list
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_avg_salary(self):
        """Получаем среднюю зарплату по вакансиям"""
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT ROUND(AVG(salary)) FROM vacancies
                        WHERE salary <> 0
                    """)
                    result = cur.fetchall()[0][0]
                    print(f"\nСредняя зарплата по вакансиям: {result} руб.\n")
                    return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT c.name, v.name, v.vacancy_url, v.salary, v.city,
                        v.published_date, v.experience, v.requirement FROM vacancies AS v 
                        JOIN companies AS c USING(id_company)
                        WHERE v.salary > (SELECT ROUND(AVG(vacancies.salary)) FROM vacancies WHERE v.salary <> 0)
                        ORDER BY v.salary DESC
                    """)
                    current_list = []
                    for number, (
                            company_name, vacancy_name, url, salary, city, pub_date, experience,
                            requirement) in enumerate(cur.fetchall(), 1):
                        if not salary:
                            salary = 'Зарплата не указана'
                        print(f"{number}. Компания: {company_name}\n"
                              f"Вакансия: {vacancy_name}\n"
                              f"Ссылка: {url}\n"
                              f"Зарплата: {salary}\n"
                              f"Город: {city}\n"
                              f"Дата публикации: {pub_date}\n"
                              f"Опыт: {experience}\n"
                              f"Требования: {requirement}\n")
                        current_list.append((company_name,
                                             vacancy_name,
                                             url,
                                             salary,
                                             city,
                                             pub_date,
                                             experience,
                                             requirement))
                    return current_list
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_keyword(self, job_name):
        """Получаем список всех вакансий, в названии которых содержится переданное в метод слово"""
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"""
                        SELECT c.name, v.name, v.vacancy_url, v.salary, v.city,
                        v.published_date, v.experience, v.requirement FROM vacancies AS v 
                        JOIN companies AS c USING(id_company)
                        WHERE LOWER(v.name) LIKE LOWER('%{job_name}%')
                        ORDER BY v.salary DESC
                    """)
                    current_list = []
                    for number, (
                            company_name, vacancy_name, url, salary, city, pub_date, experience,
                            requirement) in enumerate(cur.fetchall(), 1):
                        if not salary:
                            salary = 'Зарплата не указана'
                        print(f"{number}. Компания: {company_name}\n"
                              f"Вакансия: {vacancy_name}\n"
                              f"Ссылка: {url}\n"
                              f"Зарплата: {salary}\n"
                              f"Город: {city}\n"
                              f"Дата публикации: {pub_date}\n"
                              f"Опыт: {experience}\n"
                              f"Требования: {requirement}\n")
                        current_list.append((company_name,
                                             vacancy_name,
                                             url,
                                             salary,
                                             city,
                                             pub_date,
                                             experience,
                                             requirement))
                    return current_list
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
