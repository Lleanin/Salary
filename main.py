import requests
import pprint


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
    language_vacancies = {}
    languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#",
                 "C"]
    for language in languages:
        vacancies_processed = 0
        salaries_sum = 0
        for page in range(19):
            vacancies = stats_of_vacancies(page, language, vacancies_for_page)
            if page >= vacancies["pages"] - 1:
                break
            salaries.append(get_salary(vacancies['items']))
            for salary_list in salaries:
                if salary_list is not None:
                    vacancies_processed += 1
                for salary in salary_list:
                    if salary:
                        salaries_sum += salary
        avg_salary = salaries_sum//vacancies_processed
        language_vacancies[language] = {"vacancies_found": vacancies["found"],
                                        "vacancies_processed": vacancies_processed,
                                        "average_salary": avg_salary,
                                        }
    return language_vacanciesы


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
    pprint.pp(get_hh_statistics())


if __name__ == '__main__':
    main()

headers = {
    'X-Api-App-Id': "v3.r.137888823.3493536d8f3aec3215deaaf17ed4ec077f87bbc8.85e33e64bb8f1feb2b7563192bae7a64dd0822de"
    }
url = 'https://api.superjob.ru/2.0/vacancies/'
response = requests.get(url, headers=headers)
response.raise_for_status()
vacancies = response.json()
for vacancy in vacancies:
    print(vacancy['objects'])
    # profession = vacancy["objects"]
    # pprint.pp(profession)
# pprint.pp(vacancies['profession'])
