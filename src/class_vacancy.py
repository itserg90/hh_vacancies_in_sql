class Vacancy:
    """Класс для создания объектов вакансий"""

    def __init__(self, id_vacancies, name: str, url: str, salary: (dict, None), city: str, published_date: str,
                 experience: str, requirement: str):
        self.id = id_vacancies
        self.name = name
        self.url = url
        self.salary = salary
        self.__validate_salary()

        self.city = city
        self.published_date = published_date
        self.experience = experience
        self.requirement = requirement

    def __validate_salary(self) -> None:
        """Валидация зарплаты"""

        if not self.salary:
            self.salary = 0
        elif self.salary["from"] and self.salary["to"]:
            self.salary = round((self.salary["from"] + self.salary["from"]) / 2)
        elif self.salary["from"]:
            self.salary = self.salary["from"]
        else:
            self.salary = self.salary["to"]

    @classmethod
    def cast_to_object(cls, hh_vacancies: dict) -> dict:
        """Преобразуем данные JSON в объекты класса"""

        current_dict = {}

        for company, vacancies in hh_vacancies.items():
            current_dict[company] = []
            for vacancy in vacancies:
                current_dict[company].append(cls(vacancy["id"],
                                                 vacancy["name"],
                                                 vacancy["alternate_url"],
                                                 vacancy["salary"],
                                                 vacancy["city"],
                                                 vacancy["published_date"],
                                                 vacancy["experience"],
                                                 vacancy["requirement"]))
        return current_dict

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self.__dict__.values())}"
