-- Создание таблицы employers (работодателей)
CREATE TABLE employers
(
	employer_id varchar PRIMARY KEY NOT NULL,
	employer_name text,
	employer_url varchar,
	employer_url_vacancies varchar,
	employer_open_vacancies_number smallint
);

-- Создание таблицы vacancies (вакансий)
CREATE TABLE vacancies
(
	vacancy_id varchar PRIMARY KEY NOT NULL,
	vacancy_name varchar,
	vacancy_url varchar,
	salary real,
	salary_from real,
	salary_to real,
	salary_currency varchar,
	city varchar,
	description text,
	employer_id varchar REFERENCES employers(employer_id) ON DELETE CASCADE
);