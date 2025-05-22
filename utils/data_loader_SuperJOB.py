import requests
import time # time.sleep, чтобы делать паузы между запросами и не перегружать API.
import pandas as pd
from datetime import datetime
from params import dict_sj
from dotenv import load_dotenv
import os

load_dotenv()
KEY = os.getenv('KEY')
PER_PAGE = 50 # сколько вакансий загружать за один запрос (максимум — 100 у SuperJob)


# функция: отправляем запрос на сервер по названиям интересующих нас вакансий 
def vacancias_SJ(keyword):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {"X-Api-App-Id": KEY}
    vacancies = [] # список для сохранения вакансий
    page = 0 # номер начала страницы

    while True:
        params = {
            "keyword": keyword, # передаем ключевое слово с названием вакансии
            "page": page,
            "count": PER_PAGE
        }
        requests_sj = requests.get(url, headers=headers, params=params) # отправляем запрос на сервер API hh.ru
        print(f"[{keyword}] {requests_sj.status_code}") # для отображения информации о загрузке данных
        if requests_sj.status_code != 200: # если не успешно (200 успех) то прерываем работу
            break
        data = requests_sj.json() # парсим json приводим в формат python словарь
        vacancies.extend(data.get("objects", [])) # извлекаем из словаря значения по ключу "objects" и добавляем поэтапно в список
        if not data.get("more", False): # если данных больше нет выход
            break
        page += 1 # следующая страница
        time.sleep(0.3) # пауза для запроса на сервер API

    return vacancies

# парсинг обработка данных
def parse_vacancy(vac, category, title, key):
    date_published = vac.get("date_published") # получаем информацию о дате размещения вакансии 
    if date_published:
        date_published = datetime.fromtimestamp(date_published).strftime('%Y-%m-%d') # преобразуем в формат год-месяц-день

    vacancy_id = vac.get("id")
    link = f"https://www.superjob.ru/vacancy/{vacancy_id}" if vacancy_id else None # получаем ссылку на вакансию

    return {
        "сайт": "superjob",
        "id": vacancy_id,
        "ссылка": link,
        "компания": vac.get("firm_name"),
        "категория": category,
        "айди специальности": key,
        "специальность": title,
        "название": vac.get("profession"),
        "описание": vac.get("vacancyRichText"),
        "зарплата от": vac.get("payment_from"),
        "зарплата до": vac.get("payment_to"),
        "валюта": vac.get("currency"),
        "опыт": vac.get("experience", {}).get("title"),
        "график": vac.get("type_of_work", {}).get("title"),
        "образование": vac.get("education", {}).get("title"),
        "город": vac.get("town", {}).get("title", "Россия"),
        "дата публикации": date_published       
    }

SuperJOB_data = [] # создаем список, в котором будем хранить данные в виде словаря

# основной блок
for category, roles in dict_sj.items(): # перебираем ключи и значения из нашего словаря с вакансиями
    for role in roles:
        key = role['key']
        title = role['title']
        sj_vacancies = vacancias_SJ(title) # вызываем функцию для запроса к API, передаем ей ключевое слово вакансии
        for v in sj_vacancies: # перебираем результат возврата функции sj_vacancies
            parsed = parse_vacancy(v, category, title, key)
            if parsed:
                SuperJOB_data.append(parsed) # записываем результат

df = pd.DataFrame(SuperJOB_data) # создаем датафрейм
df.to_csv("SuperJOB.csv", index=False, encoding="utf-8-sig")
print(" Готово! Сохранено в SuperJOB.csv") # информируем о завершении