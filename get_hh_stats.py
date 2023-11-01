import requests
from predict_salary import predict_rub_salary


def stats_of_vacancies_hh(page, language, vacancies_for_page):
    payload = {
        'area': 1,
        'text': "Программист {}".format(language),
        'page': page,
        'per_page': vacancies_for_page,
    }
    url = 'https://api.hh.ru/vacancies/'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vacancies_hh = response.json()
    return vacancies_hh


def get_hh_statistics(languages):
    vacancies_for_page = 100
    salaries = []
    language_vacancies_hh = {}
    for language in languages:
        vacancies_processed = 0
        salaries_sum = 0
        for page in range(19):
            vacancies_hh = stats_of_vacancies_hh(page,
                                                 language,
                                                 vacancies_for_page)
            if page >= vacancies_hh["pages"] - 1:
                break
            salaries = get_salary_hh(vacancies_hh['items'])
            for salary in salaries:
                if salary:
                    vacancies_processed += 1
                    salaries_sum += salary
        avg_salary = salaries_sum//vacancies_processed
        language_vacancies_hh[language] = {
            "vacancies_found": vacancies_hh["found"],
            "vacancies_processed": vacancies_processed,
            "average_salary": avg_salary
        }
    return language_vacancies_hh


def get_salary_hh(vacancies_hh):
    language_salaries_hh = []
    for vacancy in vacancies_hh:
        salary = vacancy['salary']
        if not salary:
            language_salaries_hh.append(None)
        elif salary['currency'] != 'RUR':
            language_salaries_hh.append(None)
        else:
            language_salaries_hh.append(predict_rub_salary(salary['from'],
                                                           salary['to']))
    return language_salaries_hh