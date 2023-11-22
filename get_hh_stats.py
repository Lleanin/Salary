import requests
from predict_salary import predict_rub_salary


def get_vacancies(page, language, vacancies_for_page):
    area = 1
    payload = {
        'area': area,
        'text': "Программист {}".format(language),
        'page': page,
        'per_page': vacancies_for_page
    }
    url = 'https://api.hh.ru/vacancies/'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies, len(vacancies['items'])


def get_hh_statistics(languages):
    vacancies_for_page = 100
    salaries = []
    language_vacancies = {}
    for language in languages:
        sum = 0
        vacancies_response = get_vacancies(0,
                                           language,
                                           vacancies_for_page)[0]
        vacancies_processed = 0
        salaries_sum = 0
        pages_limit = vacancies_response['pages']
        for page in range(pages_limit):
            vacancies, vacancies_counter = get_vacancies(page,
                                                         language,
                                                         vacancies_for_page)
            sum += vacancies_counter
            salaries = get_salary(vacancies['items'])
            for salary in salaries:
                if salary:
                    salaries_sum += salary
                    vacancies_processed += 1
        try:
            avg_salary = salaries_sum//vacancies_processed
        except ZeroDivisionError:
            avg_salary = 0
        language_vacancies[language] = {
            "vacancies_found": sum,
            "vacancies_processed": vacancies_processed,
            "average_salary": avg_salary
        }
    return language_vacancies


def get_salary(vacancies):
    language_salaries = []
    for vacancy in vacancies:
        salary = vacancy['salary']
        if not salary:
            continue
        elif salary['currency'] != 'RUR':
            continue
        else:
            language_salaries.append(predict_rub_salary(salary['from'],
                                                        salary['to']))
    return language_salaries
