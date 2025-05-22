# -*- coding: utf-8 -*-
from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import df, df_ML, model
from utils.params import cat_features_names, num_features_names
from layouts import first_tabs, last_tabs
import plotly.io as pio
import settings as st

pio.templates['custom'] = pio.templates['plotly'].update(
    layout=dict(colorway=st.MY_PALETTE)
)

# Загружаем данные
DF_MAIN = df   # основной DataFrame для вкладки Аналитика
DF_ML = df_ML     # DataFrame для ML-прогноза
MODEL = model       # загруженная модель

def register_callbacks(app):
    """
    Регистрирует колбеки приложения.
    Здесь мы используем один унифицированный колбек для Выбрать всех графиков вкладки "Аналитика".
    """

    # --- Рендер вкладок ---
    @app.callback(
        Output('tabs_content', 'children'), #определяем какая вкладка будет первая выводится и изменяьтся при нажатии
        Input('tabs', 'active_tab')
    )
    def render_tab(active_tab): # изменения в  dash-bootstrap-components >= 2.0.0
        if active_tab == 'tab-1':
            return first_tabs()
        elif active_tab == 'tab-2':
            return last_tabs()
        # return first_tabs() if active_tab == 'tab-1' else last_tabs()



    # --- Унифицированный колбек для Выбрать всех аналитических графиков ---
    @app.callback(
        # Шесть выходов: пять графиков + карта
        Output('quant-bar', 'figure'),
        Output('spec_skil_bar', 'figure'),
        Output('salary-scatter', 'figure'),
        Output('perc-pie',    'figure'),
        Output('vacancy-map', 'figure'),
        # Шесть входов: четыре фильтра и два таба
        Input('web_sel',    'value'),
        Input('city_sel',   'value'),
        Input('region_sel', 'value'),
        Input('spec_sel',   'value'), # селекторы вери и этот
        Input('spec_skil_spec',   'active_tab'), # табы
        Input('salary_tabs','active_tab'),
        Input('perc_tabs',  'active_tab'),
    )
    def update_analytics(web_sel, city_sel, region_sel, spec_sel, spec_skil_spec, salary_tab, perc_tab):
        """
        Обновляет Выбрать все аналитические графики:
        1. Bar chart: Топ‑20 городов
        2. Scatter: специализации по городам
        3. Bar chart: топ‑20 навыков
        4. Scatter: топ‑10 вакансий по зарплате
        5. Pie chart: распределение по опыту/образованию/графику
        6. Mapbox: география вакансий
        """
        # --- 1) Берём копию DataFrame, чтобы не менять глобальный ---
        df_copy = DF_MAIN.copy()

        # --- 2) Фильтрация по сайтам, если выбран не "Выбрать все" ---
        if web_sel and 'Выбрать все' not in web_sel:
            df_copy = df_copy[df_copy['website'].isin(web_sel)]
        # --- 3) Фильтрация по городам ---
        if city_sel and 'Выбрать все' not in city_sel:
            df_copy = df_copy[df_copy['city'].isin(city_sel)]
        # --- 4) Фильтрация по регионам ---
        if region_sel and 'Выбрать все' not in region_sel:
            df_copy = df_copy[df_copy['subjects_RF'].isin(region_sel)]
        # --- 5) Фильтрация по специализациям ---
        if spec_sel and 'Выбрать все' not in spec_sel:
            df_copy = df_copy[df_copy['specialization'].isin(spec_sel)]

        # --- 6) Bar chart: Топ‑20 городов ---
        # cnt = df_copy['city'].value_counts().nlargest(20)
        # fig_quant = px.bar(
        #     x=cnt.index.tolist(),
        #     y=cnt.values.tolist(),
        #     labels={'x':'Город','y':'Число вакансий'},
        #     title='Топ‑20 городов по числу вакансий'
        # )

        cnt = df_copy['city'].value_counts().nlargest(50).reset_index()
        cnt.columns = ['city', 'count']

        fig_quant = go.Figure(go.Treemap(
            labels=cnt['city'],
            parents=[""] * len(cnt),
            values=cnt['count'],
            hoverinfo="label+value+percent entry"
        ))
        fig_quant.update_layout(title='Топ‑50 городов по числу вакансий')





        # cnt = df_copy['city'].value_counts().nlargest(50).reset_index()
        # cnt.columns = ['city', 'count']

        # fig_quant = px.treemap(
        #     cnt,
        #     path=['city'],
        #     values='count',
        #     title='Топ‑50 городов по числу вакансий'
        # )
        # fig_treemap.show()
        
        # --- 7) Scatter: специализации по городам ---
        # spec_count = df.groupby('city')['specialization'].count().nlargest(20)
        # fig_spec = px.scatter(
        #     x=spec_count.index.tolist(),
        #     y=spec_count.values.tolist(),
        #     labels={'x':'Город','y':'Количество специализаций'},
        #     title='Востребованные специальности'
        # )

        # # --- 8) Bar chart: топ‑20 навыков ---
        # skills = (
        #     df_copy['skills']
        #       .dropna()
        #       .str.split(',')
        #       .explode()
        #       .str.strip()
        # )
        # top_skills = skills.value_counts().nlargest(20)
        # fig_skill = px.bar(
        #     x=top_skills.index.tolist(),
        #     y=top_skills.values.tolist(),
        #     labels={'x':'Навык','y':'Частота'},
        #     title='Востребованные навыки'
        # )
        if spec_skil_spec == 'spec':
            top = df_copy['specialization'].value_counts(normalize=True).nlargest(5) * 100
            chart_title = 'Топ-5 востребованных специализаций'
            x_label = 'Специализация'
        else:
            top = df_copy['skills'].str.split(',').explode().str.strip().value_counts(normalize=True).nlargest(5) * 100
            chart_title = 'Топ-5 востребованных навыков'
            x_label = 'Навык'

        fig_spec_skill = go.Figure(go.Bar(
            x=top.index.tolist(),
            y=top.values.tolist(),
            marker=dict(color=top.values.tolist()),
        ))
        fig_spec_skill.update_layout(
            title=chart_title,
            xaxis_title=x_label,
            yaxis_title='Процент частоты (%)'
        )

        

        if salary_tab == 'distribution':
    # 1) РАСПРЕДЕЛЕНИЕ ЗАРПЛАТ (каждая вакансия = точка, полупрозрачность)
    # берём все ненулевые зарплаты
            # 1) Берём только колонку salary_from и убираем NaN
            salaries = df_copy['salary_from']

# 2) Фильтруем по диапазону (например, от 10 000 до 600 000)
            salaries = salaries[salaries.between(10000, 500000)]
            fig_salary = go.Figure(go.Box(
                y=salaries,   # данные по зарплатам
                boxpoints=False,                     # рисовать все точки
                # jitter=0.5,                          # разброс точек внутри «коробки»
                # pointpos=-1.8,                       # сместить точки влево
                # marker=dict(
                #     size=4,
                #     color='indigo',
                #     opacity=0.6
                # ),
                name='Оплата труда', # trace если убрать fig.update_traces(showlegend=False, hoverinfo='skip')
                # line=dict(color='darkorange'),
                # hoverinfo='skip'# откбчение подсказок медианы и так далее
            ))

            fig_salary.update_layout(
                title='Распределение заработной платы',
                yaxis_title='Зарплата от, ₽',
                xaxis=dict(showticklabels=False),    # ось X скрываем, т.к. она не несёт смысла
                # height=300,
                # margin=dict(l=20, r=20, t=40, b=20) # внутренними отступами (margin) вокруг графика внутри фигуры (Figure)
            )

        else:
    # 2) СРЕДНЯЯ ЗАРПЛАТА ПО ТОП‑10 СПЕЦИАЛИЗАЦИЯМ
            mean_spec = (df_copy.groupby('specialization')['salary_from'].mean().nlargest(10))
            fig_salary = go.Figure(go.Scatter(
                x=mean_spec.index.tolist(),
                y=mean_spec.values.tolist(),
                mode='lines+markers',
                marker=dict(size=8, color='darkblue'),
                line=dict(width=2),
                hovertemplate='<b>%{x}</b><br>Средняя зарплата: %{y:.0f} ₽<extra></extra>'
            ))

            fig_salary.update_layout(
                title='Рейтинг специальностей по средней заработной плате',
                xaxis_title='Специализация',
                yaxis_title='Средняя зарплата, ₽',
                # height=300,
                #  margin=dict(l=20, r=20, t=40, b=20)
            )

        col_map = {'exp': 'experience', 'edu': 'education', 'sched': 'work_schedule'} # из выбора, loyouts
        col = col_map.get(perc_tab, 'experience') # по умолчанию, id perc_tab
        # считаем distribution на отфильтрованных данных
        value_counts = df_copy[col].value_counts()
        avg_salaries = df_copy.groupby(col) ['salary_from'].mean()
        hover_text = [f"{cat}<br>Вакансий: {value_counts[cat]}<br>Средняя зарплата: {avg_salaries[cat]:,.0f} ₽"for cat in value_counts.index]
        fig_pie = go.Figure(go.Pie(
            labels=value_counts.index.tolist(), # названия секторов
            values=value_counts.values.tolist(), # значения (размер сектора)
            # hoverinfo='label+percent+value', # текст при наведении: метка + процент + значение
            # textinfo='label+percent' # текст на графике: метка + процент
            hoverinfo='text', # использовать собственный hovertext
            hovertext=hover_text,  # передаем сюда наш список
            # textinfo='label+percent' # текст прямо на круге
        ))
        title_map = {'experience': 'опыту работы', 'education': 'образованию', 'work_schedule': 'графику работы'}
        fig_pie.update_layout( title=f'Распределение по {title_map.get(col, col)}')


        # # --- 10) Pie chart:exp/edu/sched ---
        # col_map = {'exp':'experience', 'edu':'education', 'sched':'work_schedule'}
        # col = col_map.get(perc_tab, 'experience') # по умолчанию experience
        # fig_pie = px.pie(
        #     DF_MAIN,  # строим на полном DF для сравнения
        #     names=col,
        #     title=f'Распределение по {col}'
        # )

        # --- 11) Mapbox: география вакансий ---
        # 11.1) Агрегация по координатам
        agg = (
            df_copy
            .groupby(['city_latitude','city_longitude'], as_index=False)
            .size()
            .rename(columns={'size':'vacancy_count'})
        )
        fig_map = go.Figure(go.Scattermapbox(
            lat=agg['city_latitude'],
            lon=agg['city_longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=agg['vacancy_count'],
                sizemode='area',
                sizemin=6,
                sizeref=2.*max(agg['vacancy_count'])/(30.**2),
                opacity=0.8
            ),
            text=agg['vacancy_count'],
            hovertemplate='Вакансий: %{text}<extra></extra>'
        ))
        fig_map.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=55.75, lon=37.62),
                zoom=4
            ),
            title='География вакансий',
            height=600,
            margin=dict(r=0, t=30, l=0, b=0),
            dragmode='pan'
        )
        # # 11.2) Построение карты
        # fig_map = px.scatter_mapbox(
        #     agg,
        #     lat='city_latitude',
        #     lon='city_longitude',
        #     size='vacancy_count',            # размер маркера ~ числу вакансий
        #     size_max=30,                     # макс. размер
        #     hover_data={                     # наводим подсказку
        #         'vacancy_count': True,
        #         'city_latitude': False,
        #         'city_longitude': False
        #     },
        #     zoom=4,                          # стартовый zoom
        #     center={'lat':55.75,'lon':37.62},# центр на Москву
        #     height=600,
        #     title='География вакансий (размер маркера ~ числу вакансий)'
        # )
        # # 11.3) Настройка параметров маркеров
        # fig_map.update_traces(
        #     marker=dict(
        #         sizemin=6,        # мин. размер точки
        #         opacity=0.8       # прозрачность
        #     )
        # )
        # # 11.4) Финальное оформление карты
        # fig_map.update_layout(
        #     mapbox_style="open-street-map",
        #     margin={"r":0,"t":30,"l":0,"b":0},
        #     dragmode='pan'   # зажатие ЛКМ — перетаскивание карты
        # )

        # --- Возврат шести фигур по порядку ---
        return fig_quant, fig_spec_skill, fig_salary, fig_pie, fig_map




    # -------------------------
    # 8) Прогноз зарплаты через ML на DF_ML
    @app.callback( # State -данные, которые передаются в callback, но НЕ запускают его. То есть они не являются триггером как Input
        Output('ML_output','children'),
        Output('vacancy_list','children'),
        Input('button','n_clicks'),
        State('input_city','value'),
        State('input_specialization','value'),
        State('input_experience','value'),
        State('input_education','value'),
        State('input_work','value'),
    )
    def predict_salary(n_clicks, city, spec, exp, edu, work):
        # если не нажато — ничего не ренд
        if not n_clicks:
            return '', '' #так как у нас 2 Output мы должны вернуть 2 значения возвращаем 2 пустых

        # фильтрация DF_ML по Выбрать всем 5 параметрам
        filtr = DF_ML[
            (DF_ML['city'] == city) &
            (DF_ML['specialization'] == spec) &
            (DF_ML['experience'] == exp) &
            (DF_ML['education'] == edu) &
            (DF_ML['work_schedule'] == work)
        ]
        if filtr.empty:
            return "❌ Нет подходящих вакансий", dbc.Alert('Не найдено, попробуйте изменить поиск', color='warning')
        
        # медиана salary_up для выбранных или для Выбрать всех, если нет совпадений
        median_up = filtr['salary_up'].median()

        # категория профессии — наиболее частая среди специализации
        prof_cat = DF_ML[DF_ML['specialization'] == spec]['profession_category'].mode().iloc[0]

        # формируем DataFrame для модели
        inp = pd.DataFrame([{
            'salary_up': median_up,
            'city': city,
            'profession_category': prof_cat,
            'specialization': spec,
            'experience': exp,
            'work_schedule': work,
            'education': edu
        }])

        # оставляем только нужные признаки в правильном порядке
        inp = inp[num_features_names + cat_features_names]

        # делаем прогноз
        pred = MODEL.predict(inp)
            # Исключаем superjob только для вывода
        no_sj = filtr[filtr['website'] != 'superjob']
        text = f"💰 {int(pred)} ₽ ± 20000 ₽ (найдено {len(no_sj)} вакансий)"
        # text = f"💰 {int(pred)} ₽ ± 20000 ₽ (найдено {len(filtr)} вакансий)" # считает все вакансии

        # строим таблицу вакансий, если есть данные
 
        rows = [
            html.Tr([
                html.Td(r['website']),
                html.Td(r['job_title']), # html.Td(...) — ячейки таблицы.
                html.Td(html.A('Открыть', href=r['link'], target='_blank')) # Ссылку (html.A(...)) с текстом "Открыть", ведущую на r['link'],target='_blank' — ссылка откроется в новой вкладке. 
            ]) for _, r in no_sj.iterrows() # Перебираем .iterrows() — каждая вакансия кроме sj
            # ]) for _, r in filtr.iterrows() # показывает все вакансии
        ]
        table = dbc.Table( # Используется dbc.Table (из dash_bootstrap_components) для красивой таблицы:
            [html.Thead(html.Tr([html.Th('Сайт'), html.Th('Вакансия'), html.Th('Ссылка')])), #Шапка (Thead) с названиями колонок.
            html.Tbody(rows)], #Тело (Tbody) — сгенерированные строки.
            striped=True, bordered=True, hover=True
        )

        return text, table