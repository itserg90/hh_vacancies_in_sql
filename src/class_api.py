from abc import ABC, abstractmethod
import requests


class AbstractApi(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


class ApiVacanciesHh(AbstractApi):
    """Класс для получения списка вакансий на HeadHunter по запросу"""

    def __init__(self):
        self.hh_companies = {'1С Гейм Студиос': {}, 'Тензор': {}, 'BI.ZONE': {}, 'Positive Technologies': {},
                             'Selectel': {}, 'Ростелеком': {},
                             'Лаборатория Касперского': {}, 'Sitronics Group': {}, '3Logic Group': {},
                             'Лига Цифровой Экономики': {}, 'Rubytech': {}}
        self.hh_vacancies = {'1С Гейм Студиос': [], 'Тензор': [], 'BI.ZONE': [], 'Positive Technologies': [],
                             'Selectel': [], 'Ростелеком': [],
                             'Лаборатория Касперского': [], 'Sitronics Group': [], '3Logic Group': [],
                             'Лига Цифровой Экономики': [], 'Rubytech': []}

    def get_vacancies(self) -> None:
        """Получаем запрос из сервера"""

        for company_name in self.hh_vacancies:
            url = f"https://api.hh.ru/vacancies?per_page=100&text={company_name}&search_field=company_name"
            result = requests.get(url)
            if result.status_code == 200:
                company = result.json()["items"][0]["employer"]
                self.hh_companies[company_name].update(alternate_url=company["alternate_url"],
                                                       accredited_it_employer=company["accredited_it_employer"])
                for vacancy in result.json()["items"]:
                    if vacancy["employer"]["name"].lower() == company_name.lower():
                        self.hh_vacancies[company_name].append({"id": vacancy["id"],
                                                                "name": vacancy["name"],
                                                                "alternate_url": vacancy["alternate_url"],
                                                                "salary": vacancy["salary"],
                                                                "city": vacancy["area"]["name"],
                                                                "published_date": vacancy["published_at"][:10],
                                                                "experience": vacancy["experience"]["name"],
                                                                "requirement": vacancy["snippet"]["requirement"]})
