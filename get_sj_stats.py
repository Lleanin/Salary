import requests
from predict_salary import predict_rub_salary


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
    return vacancies, len(vacancies['objects'])


def get_sj_statistics(languages, sj_key):
    pages_limit = 5
    language_vacancies = {}
    for language in languages:
        sum = 0
        salaries_sum = 0
        salaries = []
        for page in range(pages_limit):
            vacancies, total_vacancies = get_vacansies(page, language, sj_key)
            sum += total_vacancies
            for vacancy in vacancies['objects']:
                predicted_salary = predict_rub_salary(vacancy['payment_from'],
                                                      vacancy['payment_to'])
                if predicted_salary:
                    salaries.append(predicted_salary)
        avg_salary = 0
        if salaries:
            for salary in salaries:
                salaries_sum += salary
            avg_salary = salaries_sum // len(salaries)
        language_vacancies[language] = {
            "vacancies_found": sum,
            "vacancies_processed": len(salaries),
            "average_salary": avg_salary
        }
    return language_vacancies
