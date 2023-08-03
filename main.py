from db_manager import DBManager
from job_api import HeadHunterAPI


def main():
    """
    Главная функция
    """
    hh_api = HeadHunterAPI()  # объект для работы с API hh.ru
    db = DBManager(database="hh_ru")  # объект для работы с БД

    employers = hh_api.get_employers(keyword="")  # получаем список работодателей

    # получаем список вакансий работодателей
    vacancies = []
    for employer in employers:
        vacancies += hh_api.get_employer_vacancies(employer_id=employer.id)

    # добавляем в БД
    db.add_employers(employers=employers)
    db.add_vacancies(vacancies=vacancies)

    print('Количество вакансий каждой компании: ')
    print(db.get_companies_and_vacancies_count())

    print('\nВсе вакансии: ')
    print(db.get_all_vacancies())

    print('\nСредняя зарплата по вакансиям: ')
    print(db.get_avg_salary())

    print('\nВсе вакансии, где зарплата выше среднего: ')
    print(db.get_vacancies_with_higher_salary())

    print('\nВсе вакансии, где есть слово "Монтажник": ')
    print(db.get_vacancies_with_keyword(keyword='Монтажник'))


main()
