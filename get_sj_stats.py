import requests
from predict_salary import predict_rub_salary
from itertools import count


def get_vacansies(page, language, sj_key):
    headers = {
        'X-Api-App-Id': sj_key,
        }

    payload = {
        'keyword': 'Программист {}'.format(language),
        'town': 'Москва',
        'page': page,
        'count': 100
    }

    url = 'https://api.superjob.ru/2.0/vacancies/'
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    vacancies = response.json()

    return vacancies


def get_sj_statistics(languages, sj_key):
    language_vacancies = {}

    for language in languages:
        salaries = []
        avg_salary = 0

        for page in count(0, 1):
            vacancies = get_vacansies(page, language, sj_key)

            for vacancy in vacancies['objects']:
                if vacancy['currency'] == 'rub':
                    predicted_salary = predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])
                if predicted_salary:
                    salaries.append(predicted_salary)

            if not vacancies['more']:
                break

        if salaries:
            avg_salary = sum(salaries) // len(salaries)

        language_vacancies[language] = {
            "vacancies_found": vacancies['total'],
            "vacancies_processed": len(salaries),
            "average_salary": avg_salary
        }

    return language_vacancies
