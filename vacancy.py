class Vacancy:
    """
    Класс для работы с вакансиями
    """
    def __init__(self, vacancy_id: int, title: str, url: str, salary_from: int, currency: str,
                 salary_to: int, description: str, city: str, employer_id: str):
        self.__vacancy_id = vacancy_id  # id вакансии
        self.__title = title  # название вакансии
        self.__url = url  # ссылка на вакансию
        self.__description = description  # описание вакансии
        self.__salary_from = salary_from  # зарплата от
        self.__salary_to = salary_to  # зарплата до
        self.__currency = currency  # валюта
        self.__city = city  # город
        self.__employer_id = employer_id  # id работодателя

    def __str__(self):
        return (f"id вакансии: {self.__vacancy_id}\n"
                f"Название вакансии: {self.__title}\n"
                f"Ссылка на вакансию: {self.__url}\n"
                f"Зарплата от: {self.__salary_from}\n"
                f"Зарплата до: {self.__salary_from}\n"
                f"Валюта: {self.__currency}\n"
                f"Описание вакансии: {self.__description}\n"
                f"Город: {self.__city}\n")

    def salary_avg(self):
        """
        Функция для подсчета средней зарплаты
        """
        if self.salary_to > 0:
            return self.__salary_from + (self.__salary_to - self.__salary_from) / 2
        else:
            return self.__salary_from

    def __comparison(self, other, operator: str):
        """
        Функция сравнения двух вакансий по зарплате
        :other -> другая вакансия
        :operator -> оператор сравнения
                    'ge' = больше, либо равно
                    'gt' = больше
                    'le' = меньше, либо равно
                    'lt' = меньше
                    'eq' = равно
        """
        local_operator = operator.strip().lower()

        if isinstance(other, self.__class__):
            if local_operator == "ge":
                return True if self.salary_avg() >= other.salary_avg() else False
            elif local_operator == "gt":
                return True if self.salary_avg() > other.salary_avg() else False
            elif local_operator == "lt":
                return True if self.salary_avg() < other.salary_avg() else False
            elif local_operator == "le":
                return True if self.salary_avg() <= other.salary_avg() else False
            elif local_operator == "eq":
                return True if self.salary_avg() == other.salary_avg() else False
            else:
                return False
        else:
            raise Exception(f"Объект принадлежит к классу {other.__class__}, а не к классу {self.__class__}")

    def __ge__(self, other):
        return self.__comparison(other=other, operator="ge")

    def __gt__(self, other):
        return self.__comparison(other=other, operator="gt")

    def __le__(self, other):
        return self.__comparison(other=other, operator="le")

    def __lt__(self, other):
        return self.__comparison(other=other, operator="lt")

    def __eq__(self, other):
        return self.__comparison(other=other, operator="eq")

    @property
    def vacancy_id(self):
        return self.__vacancy_id

    @property
    def title(self):
        return self.__title

    @property
    def salary_from(self):
        return self.__salary_from

    @property
    def salary_to(self):
        return self.__salary_to

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url

    @property
    def employer_id(self):
        return self.__employer_id

    @property
    def currency(self):
        return self.__currency

    @property
    def city(self):
        return self.__city
