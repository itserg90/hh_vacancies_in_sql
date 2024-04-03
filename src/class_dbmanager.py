import psycopg2


class DBManager:
    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
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
                    for name, quantity in cur.fetchall():
                        print(f"Компания {name}: {quantity} вакансий")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_all_vacancies(self):
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT companies.name, vacancies.name, vacancies.vacancy_url, vacancies.salary FROM companies
                        JOIN vacancies USING(id_company)
                        ORDER BY companies.name
                    """)
                    for number, (company_name, vacancy_name, url, salary) in enumerate(cur.fetchall(), 1):
                        if not salary:
                            salary = 'Зарплата не указана'
                        print(
                            f"{number}. Компания: {company_name}\n"
                            f"Вакансия: {vacancy_name}\n"
                            f"Зарплата: {salary}\n"
                            f"Ссылка: {url}\n")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_avg_salary(self):
        try:
            with psycopg2.connect(dbname=self.database_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT ROUND(AVG(salary)) FROM vacancies
                        WHERE salary <> 0
                    """)
                    print(f"Средняя зарплата по вакансиям: {cur.fetchall()[0][0]} руб.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_higher_salary(self):
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_keyword(self, job_name):
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
