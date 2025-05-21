'''Этот файл будет содержать глобальные настройки и параметры, которые могут использоваться в разных частях приложения.'''
# -*- coding: utf-8 -*-
import os

# # Корневая директория проекта
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Пути к CSV-файлам
# DATA_PATH_MAIN = os.path.join(BASE_DIR, 'data', 'df_vacancylast_6227.csv')
# DATA_PATH_ML   = os.path.join(BASE_DIR, 'data', 'df_vac_not_skills_7626.csv')

# # Путь к сохранённой модели CatBoost (обученной на DATA_PATH_ML)
# MODEL_PATH = os.path.join(BASE_DIR, 'data', 'model_ML_salary.cbm')

# Списки признаков для подачи в модель
CATEGORICAL_COLUMNS = [
    'city', 'profession_category', 'specialization',
    'experience', 'work_schedule', 'education'
]
NUMERICAL_COLUMNS = ['salary_up']

# Колонки, которые выводим в таблице вакансий
VACANCY_COLUMNS = ['website', 'job_title', 'link']

