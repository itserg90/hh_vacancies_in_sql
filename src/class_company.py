class Company:
    """Класс для создания объектов компаний"""

    def __init__(self, name: str, url: str, accredited_it_employer: str):
        self.name = name
        self.url = url
        self.accredited_it_employer = accredited_it_employer

    @classmethod
    def cast_to_object_list(cls, hh_companies: dict) -> dict:
        """Преобразуем данные JSON в объекты класса"""

        current_dict = {}

        for company, vacancies in hh_companies.items():
            current_dict[company] = cls(company,
                                        vacancies["alternate_url"],
                                        vacancies["accredited_it_employer"])
        return current_dict

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
