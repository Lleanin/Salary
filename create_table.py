import os
from terminaltables import AsciiTable
from dotenv import load_dotenv
from get_sj_stats import get_sj_statistics
from get_hh_stats import get_hh_statistics


def create_table(vacancy_statistic):
    vacancies_table = [
        ["Язык программирования",
         "Вакансий найдено",
         "Вакансий обработано",
         "Средняя зарплата"]
    ]
    for language, language_statistics in vacancy_statistic.items():
        vacancies_found = language_statistics["vacancies_found"]
        vacancies_processed = language_statistics["vacancies_processed"]
        average_salary = language_statistics['average_salary']
        vacancies_table.append([language,
                                vacancies_found,
                                vacancies_processed,
                                average_salary])
    table = AsciiTable(vacancies_table)
    return table.table


def main():
    load_dotenv()
    sj_key = os.getenv("SJ_SECRET_KEY")

    languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#",
                 "Swift"]
    print(create_table(get_sj_statistics(languages, sj_key)))
    print(create_table(get_hh_statistics(languages)))


if __name__ == '__main__':
    main()
