class Employer:
    """
    Класс работодателя
    """
    def __init__(self, employer_id: str, employer_name: str, url: str, url_vacancies: str, open_vacancies_numbers: int):
        self.__id = employer_id  # id работодателя в платформе
        self.__name = employer_name  # название компании
        self.__url = url  # ссылка
        self.__url_vacancies = url_vacancies  # ссылка на вакансии работодателя
        self.__open_vacancies_numbers = open_vacancies_numbers  # количество открытых вакансий

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def url_vacancies(self):
        return self.__url_vacancies

    @property
    def open_vacancies_numbers(self):
        return self.__open_vacancies_numbers


