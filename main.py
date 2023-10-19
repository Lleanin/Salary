import requests
import pprint


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


def get_hh_statistics():
    vacancies_for_page = 100
    salaries = []
    language_vacancies_hh = {}
    languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#",
                 "C"]
    for language in languages:
        vacancies_processed = 0
        salaries_sum = 0
        for page in range(19):
            vacancies_hh = stats_of_vacancies_hh(page, language, vacancies_for_page)
            if page >= vacancies_hh["pages"] - 1:
                break
            salaries.append(get_salary(vacancies_hh['items']))
            for salary_list in salaries:
                if salary_list is not None:
                    vacancies_processed += 1
                for salary in salary_list:
                    if salary:
                        salaries_sum += salary
        avg_salary = salaries_sum//vacancies_processed
        language_vacancies_hh[language] = {"vacancies_found": vacancies_hh["found"],
                                           "vacancies_processed": vacancies_processed,
                                           "average_salary": avg_salary
                                           }
    return language_vacancies_hh


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from+salary_to)/2
    elif salary_from:
        return salary_from*1.2
    else:
        return salary_to*0.8


def get_salary(vacancies_hh):
    language_salaries_hh = []
    for vacancy in vacancies_hh:
        salary = vacancy['salary']
        if not salary:
            language_salaries_hh.append(None)
        elif salary['currency'] != 'RUR':
            language_salaries_hh.append(None)
        else:
            language_salaries_hh.append(predict_rub_salary(salary['from'], salary['to']))
    return language_salaries_hh


def stats_of_vacancies_sj(page, language, vacancies_for_count):
    headers = {
        'X-Api-App-Id': "v3.r.137888823.3493536d8f3aec3215deaaf17ed4ec077f87bbc8.85e33e64bb8f1feb2b7563192bae7a64dd0822de",
        }
    payload = {
        'keyword': 'Программист',
        'town': 'Москва',
        'page': page,
        'count': vacancies_for_count
    }

    url = 'https://api.superjob.ru/2.0/vacancies/'
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    vacancies_sj = response.json()
    return vacancies_sj


def get_salary_sj(vacancies_sj):
    language_salaries_sj = []
    for vacancy in vacancies_sj['objects']:
        if vacancy['payment_from'] == 0:
            language_salaries_sj.append(vacancy['payment_to'])
        elif vacancy['payment_to'] == 0:
            language_salaries_sj.append(vacancy['payment_from'])
        elif vacancy['payment_to'] and vacancy['payment_from'] != 'rur':
            language_salaries_sj.append(None)
        else:
            language_salaries_sj.append(predict_rub_salary(vacancy['payment_from'], vacancy['payment_to']))
    return language_salaries_sj


def get_sj_statistics():
    vacancies_for_count = 100
    salaries = []
    language_vacancies_sj = {}
    languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#",
                 "C"]
    for language in languages:
        vacancies_processed = 0
        salaries_sum = 0
        for page in range(19):
            vacancies_sj = stats_of_vacancies_sj(page,
                                                 language,
                                                 vacancies_for_count)
            if page >= vacancies_sj["pages"] - 1:
                break
            salaries.append(get_salary(vacancies_sj['items']))
            for salary_list in salaries:
                if salary_list is not None:
                    vacancies_processed += 1
                for salary in salary_list:
                    if salary:
                        salaries_sum += salary
        avg_salary = salaries_sum//vacancies_processed
        language_vacancies_sj[language] = {"vacancies_found": vacancies_sj["found"],
                                           "vacancies_processed": vacancies_processed,
                                           "average_salary": avg_salary
                                           }
    return language_vacancies_sj


def main():
    pprint.pp(get_sj_statistics())


if __name__ == '__main__':
    main()
