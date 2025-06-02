# -*- coding: utf-8 -*-
from dash import Dash
import dash_bootstrap_components as dbc
from layouts import create_layout
from callbacks import register_callbacks


# Инициализируем Dash-приложение:
# - bootstrap‑тема для стилей
# - suppress_callback_exceptions=True, чтобы коллбэки на динамические элементы не падали
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server # для деплоя
app.title = "Анализ рынка труда в IT"
app.layout = create_layout()              # Основной layout из layouts.py
register_callbacks(app)                   # Регистрируем все коллбэки

if __name__ == '__main__':
    app.run(debug=True)                   # Запуск в режиме отладки
