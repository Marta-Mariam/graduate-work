'''Этот файл будет содержать глобальные настройки и параметры, которые могут использоваться в разных частях приложения.'''
# -*- coding: utf-8 -*-
import os


# Списки признаков для подачи в модель
CATEGORICAL_COLUMNS = [
    'city', 'profession_category', 'specialization',
    'experience', 'work_schedule', 'education'
]
NUMERICAL_COLUMNS = ['salary_up']

# Колонки, которые выводим в таблице вакансий
VACANCY_COLUMNS = ['website', 'job_title', 'link']

MY_PALETTE = ['#0c3e69', '#cf3aa2', '#1fb880', '#c2051b', '#cdeb09', '#6D6027', '#dfcbc2', '#cf3aa2', '#ebedd9', '#dfd5de']

PALET = ['#321b02', '#c14b11', '#ebedd9', '#e9e8e7']
PALET_PIE = ['#ede7ce', '#cdc4a0', '#b1775e', '#a85f40', '#bf5521', '#c14b11', '#702702']
PALET_BAR = [ '#fbfbc4', '#f3be73', '#c14b11', '#6f2607', '#321b02']

PALET_TREEMAP = [
    '#f1e0c6', '#e5c9a7', '#d9b582', '#d1a653', '#c79435',
    '#be7938', '#b16518', '#a15512', '#9d4c0c', '#9a4306',
    '#9e4507', '#a34a09', '#a9540d', '#ae5e11', '#b76e19',
    '#c47a21', '#d19033', '#dda04b', '#e8b563', '#f2c579',
    '#f8d393', '#fcdead', '#fde6c4', '#feeed9', '#fff4e7',
    '#fee8da', '#f7d8c8', '#f1cabb', '#e9baad', '#e1ac9f',
    '#d99e93', '#d09088', '#c7837d', '#bd766f', '#b46b66',
    '#a55f5b', '#a85e5a', '#b56d67', '#b86e68', '#b06a65',
    '#a85f5c', '#a05a57', '#985652', '#91514d', '#894c48',
    '#814844', '#79433f', '#71403b', '#6a3b37', '#633832'
]

GRAPH_LAYOUT = {
    'height': 500,
    'margin': dict(l=40, r=20, t=40, b=40),
    'plot_bgcolor': '#ffffff',
    'paper_bgcolor': '#f8f9fa',
    'font': dict(size=14, color='#333333'),
}

# settings.py
GRAPH_LAYOUT_STYLE = dict(
    plot_bgcolor='rgba(0,0,0,0)',     # прозрачный фон
    paper_bgcolor='rgba(0,0,0,0)',    # прозрачный фон вокруг графика
    margin=dict(l=60, r=40, t=50, b=50),
    font=dict(color='#333', size=14),
)
plot_bgcolor='rgba(128, 90, 213, 0.1)',  # фиолетовый с прозрачностью
paper_bgcolor='rgba(128, 90, 213, 0.15)'