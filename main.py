import requests
from pprint import pprint

count = 0
vacancies_for_page = 100

languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "C#",
             "C"]
vacancies_count = {}


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
    return vacancies


def get_hh_statistics():
    for language in languages:
        for page in range(20):
            response = stats_of_vacancies()
            if page >= response["pages"] - 1:
                break
        vacancies_count[language] = response["found"]
    return vacancies_count


url = 'https://api.hh.ru/vacancies/'
response = requests.get(url)
response.raise_for_status()
vacancies = response.json()
pprint(vacancies['items'][0]['salary'])
