import requests
from pprint import pprint


def stats_of_vacancies(page, language):
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
    return vacancies['items']


def get_hh_statistics():
    for language in languages:
        for page in range(20):
            response = stats_of_vacancies()
            if page >= response["pages"] - 1:
                break
        vacancies_count[language] = response["found"]
    return vacancies_count


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from+salary_to)/2
    elif salary_from:
        return salary_from*1.2
    else:
        return salary_to*0.8


def get_salary(vacancies):
    avg_salaries = []
    for vacancy in vacancies:
        salary = vacancy['salary']
        if not salary:
            avg_salaries.append(None)
        elif salary['currency'] != 'RUR':
            avg_salaries.append(None)
        else:
            avg_salaries.append(predict_rub_salary(salary['from'], salary['to']))
    return avg_salaries


if __name__ == '__main__':
    count = 0
    vacancies_for_page = 100

    languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#",
                 "C"]
    vacancies_count = {}

    vacancies = stats_of_vacancies(0, 'Python')
    vacancies_programming = {}

    salaries = get_salary(vacancies)
