import requests
from pprint import pprint


def stats_of_vacancies(page, language, vacancies_for_page):
    payload = {
        'area': 1,
        'text': "Программист {}".format(language),
        'page': page,
        'per_page': vacancies_for_page,
    }
    url = 'https://api.hh.ru/vacancies/'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def get_hh_statistics():
    vacancies_for_page = 100
    salaries = []
    vacancies_count = {}
    vacancies_programming = {}
    languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#",
                 "C"]
    for language in languages:
        vacancies_processed = 0
        for page in range(20):
            vacancies = stats_of_vacancies(page, language, vacancies_for_page)
            if page >= vacancies["pages"] - 1:
                break
            salaries.append(get_salary(vacancies['items']))
            if salaries:
                vacancies_processed += 1
            vacancies_count[language] = vacancies_programming
            vacancies_programming["vacancies_found"] = vacancies["found"]
            vacancies_programming["vacancies_processed"] = vacancies_processed
        print(vacancies_count)
    return vacancies_count


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from+salary_to)/2
    elif salary_from:
        return salary_from*1.2
    else:
        return salary_to*0.8


def get_salary(vacancies):
    language_salaries = []
    for vacancy in vacancies:
        salary = vacancy['salary']
        if not salary:
            language_salaries.append(None)
        elif salary['currency'] != 'RUR':
            language_salaries.append(None)
        else:
            language_salaries.append(predict_rub_salary(salary['from'], salary['to']))
    return language_salaries


def main():
    pprint(get_hh_statistics())


if __name__ == '__main__':
    main()
