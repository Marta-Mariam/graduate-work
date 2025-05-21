# utils/data_loader.py Этот модуль будет содержать функции для загрузки данных и модели.

# -*- coding: utf-8 -*-
import pandas as pd
from catboost import CatBoostRegressor


df = pd.read_csv('data/df_vacancylast_6227.csv', sep=';') 
df_ML = pd.read_csv('data/df_vac_not_skills_7626.csv', sep=';') # для второй вкладки (расчет заработной платы)

model = CatBoostRegressor()
model.load_model('data/model_ML_salary.cbm')

# def load_main_data():
#     """
#     Загружает основной датасет для визуализаций:
#     - df_vacancylast_6227.csv
#     """
#     df = pd.read_csv(DATA_PATH_MAIN, sep=';')
#     return df

# def load_ml_data():
#     """
#     Загружает датасет для обучения и предсказания:
#     - df_vac_not_skills_7626.csv
#     """
#     df_ml = pd.read_csv(DATA_PATH_ML, sep=';')
#     return df_ml

# def load_model():
#     """
#     Загружает заранее обученную модель CatBoostRegressor.
#     Модель должна быть обучена на df_vac_not_skills_7626.csv и сохранена в формате .cbm.
#     """
#     model = CatBoostRegressor()
#     model.load_model(MODEL_PATH)
#     return model
