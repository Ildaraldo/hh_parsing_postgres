import psycopg2
from employer import Employer
from job_api import HeadHunterAPI
from vacancy import Vacancy


class DBManager:
    """
    Класс для работы с БД
    """
    def __init__(self, database: str, host="localhost", user="postgres", password="postgres"):
        self.__host = host  # название хоста
        self.__database = database  # название БД
        self.__user = user  # имя пользователя
        self.__password = password  # пароль

    # @classmethod
    # def query_insert_into(cls, table_name: str, data_: list, column_names: list) -> str:
    #     """
    #     Функция, которая формирует sql команду insert
    #     table_name: название таблицы
    #     data_: данные для добавления
    #     column_names: название столбцов
    #     """
    #     columns_numbers = len(data_[0])  # количество столбцов
    #     data_numbers = len(data_)  # длина списка
    #
    #     query = f"INSERT INTO {table_name} \n"  # заголовок запроса
    #
    #     # названия столбцов
    #     if column_names:
    #         query += "("
    #         for i in range(columns_numbers):
    #             query += column_names[i]
    #             if i != columns_numbers - 1:
    #                 query += ", \n"
    #         query += ") \n"
    #
    #     query += "VALUES \n"
    #
    #     # заполняем данные
    #     for i in range(data_numbers):
    #         query += "("
    #         for j in range(columns_numbers):
    #             if data_[i][j].isdecimal():
    #                 query += data_[i][j]
    #             else:
    #                 parameter = "".join([symbol for symbol in list(data_[i][j]) if symbol != "'"])
    #                 query += f"'{parameter}'"
    #
    #             if j != columns_numbers - 1:
    #                 query += ", \n"
    #
    #         if i != data_numbers - 1:
    #             query += "), \n"
    #         else:
    #             query += ");\n"
    #
    #     return query

    def send_data_to_database(self, query: str):
        """
        Функция, которая отправляет запрос в БД (запись)
        :query - sql запрос
        """
        # отправляем запрос в БД
        with psycopg2.connect(host=self.__host, database=self.__database, user=self.__user,
                              password=self.__password) as dbconnect:
            cursor = dbconnect.cursor()

            cursor.execute(query)
            dbconnect.commit()

        dbconnect.close()

    def receive_data_from_database(self, query: str):
        """
        Функция, которая отправляет запрос в БД (чтение)
        :query - sql запрос
        """
        # отправляем запрос в БД
        with psycopg2.connect(host=self.__host, database=self.__database, user=self.__user,
                              password=self.__password) as dbconnect:
            cursor = dbconnect.cursor()

            cursor.execute(query)
            dbconnect.commit()
            data_from_database = cursor.fetchall()

        dbconnect.close()
        return data_from_database

    def add_employers(self, employers: list[Employer]):
        """
        Функция вставки данных (работодателей) в таблицу employers
        :employers - список работодателей
        """
        # формируем текст запроса
        query = ("INSERT INTO employers "
                 "(employer_id, "
                 "employer_name, "
                 "employer_url, "
                 "employer_url_vacancies, "
                 "employer_open_vacancies_number) VALUES ")

        for i in range(len(employers)):
            query += (f"('{employers[i].id}', "
                      f"'{employers[i].name}', "
                      f"'{employers[i].url}', "
                      f"'{employers[i].url_vacancies}', "
                      f"'{employers[i].open_vacancies_numbers}')")

            if i != len(employers) - 1:
                query += ", "
            else:
                query += "; "

        # query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'employers'"
        # column_names = [column_name[0] for column_name in self.__receive_data_from_database(query=query)]

        # column_names = ["employer_id",
        #                 "employer_name",
        #                 "employer_url",
        #                 "employer_url_vacancies",
        #                 "employer_open_vacancies_number"]
        # query = self.query_insert_into(table_name="employers", column_names=column_names, data_=employers)

        # отправляем запрос в БД
        self.send_data_to_database(query)

    def add_vacancies(self, vacancies: list[Vacancy]):
        # формируем текст запроса
        query = ("INSERT INTO vacancies "
                 "(vacancy_id, "
                 "vacancy_name, "
                 "vacancy_url, "
                 "salary, "
                 "salary_from, "
                 "salary_to, "
                 "salary_currency, "
                 "city, "
                 "description, "
                 "employer_id) VALUES ")

        for i in range(len(vacancies)):
            query += (f"('{vacancies[i].vacancy_id}', "
                      f"'{vacancies[i].title}', "
                      f"'{vacancies[i].url}', "
                      f"'{vacancies[i].salary_avg()}', "
                      f"'{vacancies[i].salary_from}', "
                      f"'{vacancies[i].salary_to}', "
                      f"'{vacancies[i].currency}', "
                      f"'{vacancies[i].city}', "
                      f"'{vacancies[i].description}', "
                      f"'{vacancies[i].employer_id}')")

            if i != len(vacancies) - 1:
                query += ", "
            else:
                query += "; "

        # отправляем запрос в БД
        self.send_data_to_database(query)

    def get_companies_and_vacancies_count(self):
        """
        Функция, которая получает список всех компаний и количество вакансий у каждой компании
        """
        query = ("SELECT employer_name AS Компания, COUNT(*) AS Количество_вакансий FROM employers "
                 "LEFT JOIN vacancies USING (employer_id) GROUP BY Компания ORDER BY Количество_вакансий;")

        return self.receive_data_from_database(query)

    def get_all_vacancies(self):
        """
        Функция, получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        query = ("SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url "
                 "FROM vacancies LEFT JOIN employers USING (employer_id);")

        return self.receive_data_from_database(query)

    def get_avg_salary(self):
        """
        Функция, получает среднюю зарплату по вакансиям
        """
        # salary_sum = 0
        # counter = 0
        #
        # vacancies_salary = self.__receive_data_from_database("SELECT salary FROM vacancies;")
        # for vacancy_salary in vacancies_salary:
        #     salary_sum += vacancy_salary[0]
        #     if vacancy_salary[0] > 0:
        #         counter += 1
        #
        # return salary_sum / counter

        # запрос, который считает среднюю зарплату -> считается сумма зарплат и делится на количество
        query = ("SELECT sum_.c1 / "
                 "(SELECT COUNT(*) FROM (SELECT salary FROM vacancies WHERE salary > 0) AS t) "
                 "FROM (SELECT SUM(salary) AS c1 FROM vacancies WHERE salary > 0) AS sum_")

        return self.receive_data_from_database(query)[0][0]

    def get_vacancies_with_higher_salary(self):
        """
        Функция, получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        # считаем среднюю зарплату, далее вызываем запрос, который выводит вакансии, у которых зарплата выше среднего
        query = f"SELECT * FROM vacancies WHERE salary > {self.get_avg_salary()};"  # формируем текст запроса
        return self.receive_data_from_database(query)

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Функция, получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например “python”
        """
        query = (f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{keyword}%';")  # формируем текст запроса
        return self.receive_data_from_database(query)

