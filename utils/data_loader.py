# utils/data_loader.py Этот модуль будет содержать функции для загрузки данных и модели.
import pandas as pd
from catboost import CatBoostRegressor


df = pd.read_csv('data/df_vacancylast_6227.csv', sep=';') # загрузка датасета
df_ML = pd.read_csv('data/df_vac_not_skills_7626.csv', sep=';') # lдатасет для второй вкладки (расчет заработной платы)

model = CatBoostRegressor() # создаем модель
model.load_model('data/model_ML_salary.cbm') # загружаем модель ML