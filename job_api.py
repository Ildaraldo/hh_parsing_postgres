import requests
from abc import ABC, abstractmethod
from employer import Employer
from vacancy import Vacancy


class JobAPI(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_employers(self, keyword) -> dict:
        """
        Метод для получения информации о работодателях по API
        keyword: Ключевое слово запроса
        """
        pass

    @abstractmethod
    def get_employer_vacancies(self, employer_id) -> dict:
        """
        Метод для получения вакансий работодателя по API
        keyword: Ключевое слово запроса
        """
        pass


class HeadHunterAPI(JobAPI):
    """
    Класс для получений вакансий с HeadHunter (hh.ru)
    """
    def __init__(self, page=0, per_page=50):
        self.__page = page  # номер страницы
        self.__per_page = per_page  # количество получаемых вакансий на одну страницу

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, page: int):
        self.__page = page

    @property
    def per_page(self):
        return self.__per_page

    @per_page.setter
    def per_page(self, per_page: int):
        self.__per_page = per_page

    def get_employers(self, keyword) -> list:
        """
        Метод для получения информации о работодателях с hh.ru по API
        keyword: Ключевое слово запроса
        """
        employers = []  # список работодателей

        # параметры запроса по API
        employers_parameters = {
            "text": keyword,
            "only_with_vacancies": True,
            "per_page": self.__per_page,
            "page": self.__page
        }

        # получение работодателей по API
        hh_employers = requests.get(url='https://api.hh.ru/employers', params=employers_parameters).json()

        for hh_employer in hh_employers["items"]:
            employer = Employer(employer_id=hh_employer["id"],
                                employer_name=hh_employer["name"],
                                url=hh_employer["alternate_url"],
                                url_vacancies=hh_employer["vacancies_url"],
                                open_vacancies_numbers=hh_employer["open_vacancies"])
            employers.append(employer)

        return employers

    def get_employer_vacancies(self, employer_id) -> list:
        """
        Метод для получения вакансий работодателя с hh.ru по API
        keyword: Ключевое слово запроса
        """
        vacancies = []  # список вакансий работодателя

        # параметры запроса по API
        parameters = {
            "per_page": self.__per_page,
            "page": self.__page
        }

        # получение вакансий работодателя по API
        hh_employer_vacancies = requests.get(url=f'https://api.hh.ru/vacancies?employer_id={employer_id}',
                                             params=parameters).json()

        for vacancy in hh_employer_vacancies["items"]:
            if vacancy["salary"] is not None and vacancy["salary"]["from"] is not None:
                salary_from = vacancy["salary"]["from"]
            else:
                salary_from = 0

            if vacancy["salary"] is not None and vacancy["salary"]["to"] is not None:
                salary_to = vacancy["salary"]["to"]
            else:
                salary_to = 0

            if vacancy["address"] is not None and vacancy["address"]["city"] is not None:
                city = vacancy["address"]["city"]
            else:
                city = ""

            if vacancy["salary"] is not None and vacancy["salary"]["currency"] is not None:
                currency = vacancy["salary"]["currency"]
            else:
                currency = ""

            vacancy = Vacancy(vacancy_id=vacancy["id"],
                              title=vacancy["name"],
                              url=vacancy["alternate_url"],
                              salary_from=salary_from,
                              salary_to=salary_to,
                              description=f'{vacancy["snippet"]["requirement"]}\n'
                                          f'{vacancy["snippet"]["responsibility"]}',
                              city=city,
                              currency=currency,
                              employer_id=vacancy["employer"]["id"])

            vacancies.append(vacancy)

        return vacancies

