import requests
import pandas as pd
import time
from params import dict_hh

PER_PAGE = 50
ALL_ROLES = [role for group in dict_hh.values() for role in group] # создаем список професий из словаря "без подгруппы"
ID_TO_NAME = {r['id']: r['name'] for r in ALL_ROLES} # создаем словарь с id и названием професии для записи в колонку специальность

# функция для запроса вакансий с API hh.ru
def vacancies_hh(prof_role_id): # передаем id вакансии с списка ALL_ROLES
    url = "https://api.hh.ru/vacancies"
    vacancies = []
    
    for page in range(5): # до 5 запросов по каждому id чтобы не выходить за лимиты API hh.ru
        params = {
            "area": 113,  # по России
            "professional_role": prof_role_id, # id професии
            "per_page": PER_PAGE,
            "page": page
        }
        response = requests.get(url, params=params) # запрос
        if response.status_code != 200:
            print(f" Ошибка запроса: {response.status_code}")
            break

        data = response.json() # парсим ответ
        vacancies.extend(data.get("items", [])) # добавляем вакансии в список

        if page >= data.get("pages", 1) - 1: # (data.get("pages") — сколько всего страниц доступно по данному запросу) если страниц меньше чем 7 то остановка цикла
            break

        time.sleep(0.3)

    return vacancies

# обрабатываем данные по id конкретной вакансии которую мы получили после функции vacancies_hh и передаем id наз-ие вакансии из списка
# 2-ой запрос для получения расширенной информации по самой вакансии, без этого нам не получить инфу для колонок, первый запрос возвращает 
# инфу(ее мало) и id самой вакансии, уже зная id вакансии мы по ней еще раз делаем более детальныцй запрос на API

def parse_vacancy(vacancy_summary, prof_role_id):
    vacancy_id = vacancy_summary.get("id")
    try:
        full_response = requests.get(f"https://api.hh.ru/vacancies/{vacancy_id}")
        if full_response.status_code != 200:
            print(f" Не удалось получить данные по вакансии ID {vacancy_id}")
            return None

        vacancy = full_response.json()

        # для обработки вложенного словаря (чтобы процесс продолжался и в случае отсутвие значения возвращаем пустой словарь)
        salary = vacancy.get("salary") or {}
        experience = vacancy.get("experience") or {}
        schedule = vacancy.get("schedule") or {}
        area = vacancy.get("area") or {}
        employer = vacancy.get("employer") or {}
        education = vacancy.get("education") or {}
        key_skills = vacancy.get("key_skills") or []


        return {
            "сайт": "hh.ru",
            "айди специальности": prof_role_id,
            "специальность": ID_TO_NAME.get(prof_role_id, ""),
            "название вакансии": vacancy.get("name"),
            "компания": employer.get("name", "—"),
            "ссылка": vacancy.get("alternate_url"),
            "ключевые навыки": ", ".join(skill.get("name", "") for skill in key_skills),
            "описание": vacancy.get("description"),
            "зарплата от": salary.get("from"),
            "зарплата до": salary.get("to"),
            "валюта": salary.get("currency"),
            "опыт": experience.get("name"),
            "график": schedule.get("name"),
            "образование": education.get("name") if isinstance(education, dict) else None, # может не быть словарем, жестко обрабатываем 
            "город": area.get("name"),
            "дата публикации": vacancy.get("published_at")
        }

    except Exception as e:
        print(f" Ошибка при обработке вакансии ID {vacancy_id}: {e}")
        return None

# основной блок
HH_data = []

for role in ALL_ROLES:
    print(f"Получение вакансий: {role['name']} (ID {role['id']})")
    vacancies = vacancies_hh(role['id']) # id вакансии из списка
    for vacancy in vacancies:
        parsed = parse_vacancy(vacancy, role['id']) # передаем полученные вакансии и роль id
        if parsed:
            HH_data.append(parsed)

# Сохраняем в DataFrame
df = pd.DataFrame(HH_data)
df.to_csv("HH.csv", index=False, encoding='utf-8-sig', sep=';')

print("Данные сохранены в HH.csv")



