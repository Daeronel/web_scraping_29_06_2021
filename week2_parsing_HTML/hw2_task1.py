import time
import requests
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

ENDPOINT_URL = "https://hh.ru/search/vacancy"


class HHScraper:
    def __init__(self, start_url, params, num_pages, headers):
        self.start_url = start_url
        self.start_params = params
        self.num_pages = num_pages
        self.headers = headers
        self.info_about_vacancies = []

    # получаем HTML код страницы
    def get_html_string(self, url, params):
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            time.sleep(1)
            print(e)
            return None
        return response.text

    # преобразуем HTML в объект BS
    @staticmethod
    def get_dom(html_string):
        return BeautifulSoup(html_string, "html.parser")

    # запускаем сбор данных
    def run(self):
        self.parse_page(self.start_url, self.start_params)
        for page_number in range(1, self.num_pages):
            params = self.start_params
            params["page"] = page_number
            self.parse_page(self.start_url, params)

        self.save_info_about_vacancies()

    # извлекаем данные для вакансии
    def get_info_from_element(self, element):
        info = {}

        info["cite"] = "hh.ru"
        info["name"] = element.find(
            attrs={"data-qa": "vacancy-serp__vacancy-title"}
        ).text
        href_tag = element.find(
            attrs={"data-qa": "vacancy-serp__vacancy-title"}
        )
        info["href"] = href_tag["href"]

        try:
            salary = element.find(attrs={"data-qa": "vacancy-serp__vacancy-compensation"}).text
            salary = salary.replace(u"\u202f", "")  # убираем no-break пробелы
            salary_list = salary.split()
            if len(salary_list) == 4:
                info["min_salary"] = salary_list[0]
                info["max_salary"] = salary_list[2]
                info["salary_currency"] = salary_list[3]
            elif len(salary_list) == 3:
                info["min_salary"] = salary_list[1]
                info["max_salary"] = '-'
                info["salary_currency"] = salary_list[2]
        except AttributeError as e:
            print(e)
            info["min_salary"] = '-'
            info["max_salary"] = '-'
            info["salary_currency"] = '-'
        except ValueError as e:
            print(e)
            info["min_salary"] = '-'
            info["max_salary"] = '-'
            info["salary_currency"] = '-'
        except TypeError as e:
            info["min_salary"] = '-'
            info["max_salary"] = '-'
            info["salary_currency"] = '-'
        return info

    # сохраняем все вакансии в json-файл
    def save_info_about_vacancies(self):
        path = "data.json"
        with open(path, "w") as f:
            json.dump(self.info_about_vacancies, f)
        pass

    # находим все вакансии на странице
    def parse_page(self, url, params):
        html_string = self.get_html_string(url, params)
        if html_string is None:
            print("Error")
            return

        soup = HHScraper.get_dom(html_string)
        vacancies_elements = soup.find_all(
            attrs={"class": "vacancy-serp-item"}
        )
        for element in vacancies_elements:
            info = self.get_info_from_element(element)
            self.info_about_vacancies.append(info)


if __name__ == "__main__":
    string = input()
    num_pages = input()
    num_pages = int(num_pages)
    PARAMS = {
        "text": string.replace(' ', '+'),
    }
    scraper = HHScraper(ENDPOINT_URL, PARAMS, num_pages, headers)
    scraper.run()
