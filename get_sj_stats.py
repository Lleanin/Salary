import requests
from predict_salary import predict_rub_salary


def get_vacansies_sj(page, language, sj_key):
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
    vacancies_sj = response.json()
    return vacancies_sj


def get_sj_statistics(languages, sj_key):
    pages_limit = 5
    language_vacancies_sj = {}
    for language in languages:
        salaries = []
        for page in range(pages_limit):
            vacancies_sj = get_vacansies_sj(page, language, sj_key)
            if not vacancies_sj['objects']:
                break
            for vacancy in vacancies_sj['objects']:
                predicted_salary = predict_rub_salary(vacancy['payment_from'],
                                                      vacancy['payment_to'])
                if predicted_salary:
                    salaries.append(predicted_salary)
        total_vacancies = vacancies_sj['total']
        avg_salary = None
        if salaries:
            avg_salary = int(
                sum(salaries) / len(salaries))

        language_vacancies_sj[language] = {
            "vacancies_found": total_vacancies,
            "vacancies_processed": len(salaries),
            "average_salary": avg_salary
        }
    return language_vacancies_sj
