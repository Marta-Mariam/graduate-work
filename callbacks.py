from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import df, df_ML, model
from utils.params import cat_features_names, num_features_names # для ML признаки по которым модель обучалась 
from layouts import first_tabs, last_tabs
import settings as st


# Загружаем данные
DF_MAIN = df   # основной DataFrame для вкладки Аналитика
DF_ML = df_ML     # DataFrame для ML-прогноза
MODEL = model       # Модель ML

def register_callbacks(app):
    @app.callback(
        Output('tabs_content', 'children'), # определяем какая вкладка будет первая выводится и изменяться при нажатии
        Input('tabs', 'active_tab')
    )
    def render_tab(active_tab): # изменения в  dash-bootstrap-components >= 2.0.0 "active_tab", выбор вкладок
        if active_tab == 'tab-1':
            return first_tabs()
        elif active_tab == 'tab-2':
            return last_tabs()


    # первый модуль(вкладка Аналитика)
    # унифицированный колбек для всех графиков
    @app.callback(
        Output('quant-bar', 'figure'), # график дерево
        Output('spec_skil_bar', 'figure'), # график навыки/скилы
        Output('salary-scatter', 'figure'), # график уровень зп
        Output('perc-pie',    'figure'), # график круг
        Output('vacancy-map', 'figure'), # график карта
        Input('web_sel',    'value'), # селектор
        Input('city_sel',   'value'), # селектор
        Input('region_sel', 'value'), # селектор
        Input('spec_sel',   'value'), # селектор
        Input('spec_skil_spec',   'active_tab'), # tabs
        Input('salary_tabs','active_tab'), # tabs
        Input('perc_tabs',  'active_tab'), # tabs
    )
    def update_analytics(web_sel, city_sel, region_sel, spec_sel, spec_skil_spec, salary_tab, perc_tab):

        # берём копию DataFrame, чтобы не менять глобальный
        df_copy = DF_MAIN.copy()

        # фильтрация по селекторам, по умолчанию "выбрать все"
        if web_sel and 'Выбрать все' not in web_sel: # происходит фильтрация по заданным параметрам из селектора в случае если не указанов "выбрать все"
            df_copy = df_copy[df_copy['website'].isin(web_sel)] #
        if city_sel and 'Выбрать все' not in city_sel:
            df_copy = df_copy[df_copy['city'].isin(city_sel)]
        if region_sel and 'Выбрать все' not in region_sel:
            df_copy = df_copy[df_copy['subjects_RF'].isin(region_sel)]
        if spec_sel and 'Выбрать все' not in spec_sel:
            df_copy = df_copy[df_copy['specialization'].isin(spec_sel)]


    # график, дерево диаграммы  топ 50 городов с наибольшим количеством вакансий 
        cnt = df_copy['city'].value_counts().nlargest(30).reset_index()
        cnt.columns = ['city', 'count']

        fig_quant = go.Figure(go.Treemap(
            labels=cnt['city'],
            parents=[""] * len(cnt),
            values=cnt['count'],
            hoverinfo="label+value+percent entry",
            marker=dict(line=dict(width=1, color='#482314')),
            marker_colors=st.PALET_TREEMAP
        ))
        # обновление графика
        fig_quant.update_layout(
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            # width=900, # по горизонтали 
            margin=dict(t=20, b=10, l=10, r=10), # минимальные отступы
            )
        
        fig_quant.update_traces(root_color='rgba(0,0,0,0)')


    # график топ 5 по частоте специальностей и навыков 
        if spec_skil_spec == 'spec':
            top = df_copy['specialization'].value_counts(normalize=True).nlargest(5) * 100
            chart_title = 'Топ-5 востребованных специализаций'
            x_label = 'Специализация'
            labels = top.index.tolist()
            values = top.values.tolist()
            xaxis_settings = dict()  # без изменения шрифта
        else:
            # .explode() преобразование каждого лемента в строку(т.е. вычленяет знач. разбитые по ",")
            # .value_counts(normalize=True) — считаем частоту навыков
            top = df_copy['skills'].str.split(',').explode().str.strip().value_counts(normalize=True).nlargest(5) * 100 
            chart_title = 'Топ-5 востребованных навыков'
            x_label = 'Навык'
            labels = top.index.tolist()
            values = top.values.tolist()
            xaxis_settings = dict(    # увеличенный шрифт только для skills
                tickfont=dict(size=16)                
            )
        # nобъеденяем два списка в пары, перебор пар, выводим
        hover_text = [f'{label}<br>{val:.1f}%' for label, val in zip(labels, values)]

        fig_spec_skill = go.Figure(go.Bar(
            x=labels,
            y=values,
            hoverinfo='text',
            hovertext=hover_text,
            marker=dict(color=st.PALET_BAR, line=dict(color='#482314', width=1))
        ))

        fig_spec_skill.update_layout(
            # title=chart_title,
            title_x=0.5,
            xaxis=dict(**xaxis_settings), # создание словаря для параметра xaxis с распаковкой значений из другого словаря xaxis_settings
            yaxis_title='Процент частоты (%)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=30, b=30, l=30, r=30),
            height=456
            # margin=dict(t=60, b=100)
        )


    # график ящик с усами/высокооплачиваемые специальности "среднее"
        if salary_tab == 'distribution': # активная вкладка
            salaries = df_copy['salary_from']
            # фильтруем по диапазону (от 10 000 до 500 000)
            salaries = salaries[salaries.between(10000, 500000)]
            fig_salary = go.Figure(go.Box(
                y=salaries,  # данные по зарплатам
                boxpoints=False,
                fillcolor='#ad4818', # заливка ящика
                line=dict(color='#482314', width=1), # цвет и толщина границ
                # jitter=0.5,                          # разброс точек внутри «коробки»
                # pointpos=-1.8,                       # сместить точки влево
                # marker=dict(size=4, color='rgba(128,90,213,0.5)', showscale=True, opacity=0.6),
                # name='Оплата труда' # trace если убрать fig.update_traces(showlegend=False, hoverinfo='skip')
                # line=dict(color='darkorange'),
                # hoverinfo='skip'# отключение подсказок медианы и так далее
            ))

            fig_salary.update_layout(
                title=dict(text='Распределение заработной платы', x=0.5),
                yaxis_title='Зарплата от, ₽',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showticklabels=False), # ось X скрываем, т.к. она не несёт смысла
                # height=300,
                # margin=dict(l=20, r=20, t=40, b=20) # внутренние отступы (margin) вокруг графика внутри фигуры (Figure)
            )
        else:
            mean_spec = (df_copy.groupby('specialization')['salary_from'].mean().nlargest(10))
            fig_salary = go.Figure(go.Scatter(
                x=mean_spec.index.tolist(),
                y=mean_spec.values.tolist(),
                mode='lines+markers',
                marker=dict(size=10,
                            color=mean_spec.values.tolist(),  # градиент по зарплате
                            colorscale=st.PALET,
                            # opacity=0.6, # прозрачность
                            showscale=True, # цветовая шкала
                            # colorbar=dict(title='Зарплата'),
                            line=dict(width=1, color='#482314')
                            ),
                line=dict(width=2, color='#482314'), #цвет линии
                hovertemplate='<b>%{x}</b><br>Средняя зарплата: %{y:.0f} ₽<extra></extra>'
            ))

            fig_salary.update_layout(
                title=dict(text='Рейтинг специальностей по средней заработной плате',
                           x=0.5),
                # xaxis_title='Специализация',
                yaxis_title='Средняя зарплата, ₽',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',             
                # height=300,
                #  margin=dict(l=20, r=20, t=40, b=20)
            )


    # круговой график (опыт, образование, график работы)
        col_map = {'exp': 'experience', 'edu': 'education', 'sched': 'work_schedule'} # из выбора, loyouts
        col = col_map.get(perc_tab, 'experience') # по умолчанию, id perc_tab
        value_counts = df_copy[col].value_counts()
        avg_salaries = df_copy.groupby(col) ['salary_from'].mean() # расчет среднего
        median_salaries = df_copy.groupby(col) ['salary_from'].median() # расчет медианы
        hover_text = [
            f"{cat}<br>Вакансий: {value_counts[cat]}"
            f"<br>Средняя зарплата: {avg_salaries[cat]:,.0f} ₽"
            f"<br>Медианная зарплата: {median_salaries[cat]:,.0f} ₽"
            for cat in value_counts.index
            ]
        # построение графика
        fig_pie = go.Figure(go.Pie(
            labels=value_counts.index.tolist(), # названия секторов
            values=value_counts.values.tolist(), # значения (размер сектора)
            # hoverinfo='label+percent+value', # текст при наведении: метка + процент + значение
            # textinfo='label+percent' # текст на графике: метка + процент
            hoverinfo='text', # использовать собственный hovertext
            hovertext=hover_text,  # передаем сюда наш список
            # textinfo='label+percent' # текст прямо на круге
            marker=dict(colors=st.PALET_PIE,  line=dict(color='#482314', width=0.5)),  # применяем цвета
            textfont=dict(size=14, color='#333333')
        ))

        title_map = {'experience': 'опыту работы', 'education': 'образованию', 'work_schedule': 'графику работы'}
        fig_pie.update_layout( title=f'Распределение по {title_map.get(col, col)}', title_x=0.5,  # центрируем заголовок
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=16, color='#333333')))


    # график-карта
        agg = (
            df_copy.groupby(['city_latitude','city_longitude'], as_index=False).size().rename(columns={'size':'vacancy_count'})
        )
        fig_map = go.Figure(go.Scattermapbox(
            lat=agg['city_latitude'],
            lon=agg['city_longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=agg['vacancy_count'],
                sizemode='area',
                sizemin=6,
                sizeref=2.*max(agg['vacancy_count'])/(30.**2), # настройка размера кружочков на карте в радиусах
                opacity=0.8,
                color='#c14b11'
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
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            # title='География вакансий',
            height=600,
            margin=dict(r=0, t=30, l=0, b=0),
            dragmode='pan',
        )


    #  Возврат шести фигур по порядку
        return fig_quant, fig_spec_skill, fig_salary, fig_pie, fig_map


    #  Прогноз зарплаты через ML на DF_ML
    @app.callback( # State -данные, которые передаются в callback, но не запускают его. То есть они не являются триггером как Input
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

        # фильтрация DF_ML выбор по всем 5 параметрам
        filtr = DF_ML[
            (DF_ML['city'] == city) &
            (DF_ML['specialization'] == spec) &
            (DF_ML['experience'] == exp) &
            (DF_ML['education'] == edu) &
            (DF_ML['work_schedule'] == work)
        ]
        if filtr.empty:
            return "❌ Нет подходящих вакансий", ''# , dbc.Alert('Не найдено, попробуйте изменить поиск', color='#ebedd9')
        # так как модель обучали на 7 параметрах а вводим 5 остальные 2 берем уже от сортировки параметр.
        # медиана salary_up для выбранных или для "Выбрать всех", если нет совпадений
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
            # исключаем superjob только для вывода
        # no_sj = filtr[filtr['website'] != 'superjob']
        # text = f"💰 {int(pred):,} ₽ ± 20 000 ₽ (найдено {len(no_sj)} вакансий)".replace(',', ' ')
        # text = html.Pre(f"💰 Предсказанная заработная плата составила {int(pred):,} ₽\nВозможная погрешность прогноза — до ± 21000 ₽\nПо вашему запросу найдено {len(filtr)} вакансий".replace(',', ' ')) # считает все вакансии
        pred_text = html.Div([
            html.P(f"💰 Предсказанная заработная плата: {int(pred):,} ₽".replace(',', ' ')),
            html.P("📉 Возможная погрешность прогноза: до ± 21 000 ₽"),
            html.P(f"🔎 Найдено релевантных вакансий: {len(filtr)}")
        ], style={'textAlign': 'left', 'marginTop': '0px', 'fontSize': '20px', 'lineHeight': '1.6'})

        # строим таблицу вакансий, если есть данные
        sorted_filtr = filtr.sort_values(by='website', key=lambda x: x == 'superjob') # фильтрует так чтобы 'superjob' был в конце
        rows = [
            html.Tr([
                html.Td(r['website'], style={'background': 'none', 'text-decoration': 'none'}),
                html.Td(r['job_title'], style={'background': 'none', 'text-decoration': 'none'}), # html.Td(...) — ячейки таблицы.
                html.Td(html.A('Открыть', href=r['link'], target='_blank'), style={'background': 'none', 'color': 'black'}) # Ссылку (html.A(...)) с текстом "Открыть", ведущую на r['link'],target='_blank' — ссылка откроется в новой вкладке. 
            # ]) for _, r in no_sj.iterrows() # Перебираем .iterrows() — каждая вакансия кроме sj
            ]) for _, r in sorted_filtr.iterrows() # показывает все вакансии
        ]
        table = dbc.Table( # используется dbc.Table (из dash_bootstrap_components) для красивой таблицы:
            [html.Thead(html.Tr([html.Th('Сайт', className="bg-transparent"), html.Th('Вакансия', className="bg-transparent"),
                                  html.Th('Ссылка', className="bg-transparent")])), # шапка (Thead) с названиями колонок.
            html.Tbody(rows)], className="bg-transparent", # тело (Tbody) — сгенерированные строки.
            striped=False, bordered=True, hover=False
        )

        return pred_text, table