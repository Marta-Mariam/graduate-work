from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.data_loader import df, df_ML



def first_tabs():

    return dbc.Container([
        # html.Div([
        #     html.H5("Интерактивная карта"), 
        # ], className="headings"),
        html.Br(), # элемент переноса строки в HTML-документе.Он используется для создания новой строки или начала нового абзаца в блоке

        # фильтры: сайты, города, регионы, специализации
        dbc.Row([
            dbc.Col([
                dbc.Label("Сайты"),
                dcc.Dropdown(
                    id='web_sel',
                    options=[{'label': x, 'value': x} for x in ['Выбрать все'] + sorted(df['website'].unique())],
                    value=['Выбрать все'],
                    placeholder="Выберите сайт",
                    multi=True,
                    clearable=False
                )
            ], xs=12, sm=6, md=3),# width=3
            dbc.Col([
                dbc.Label("Город"),
                dcc.Dropdown(
                    id='city_sel',
                    options=[{'label': x, 'value': x} for x in ['Выбрать все'] + sorted(df['city'].unique())],
                    value=['Выбрать все'],
                    placeholder="Выберите город",
                    multi=True,
                    clearable=False
                )
            ], xs=12, sm=6, md=3),
            dbc.Col([
                dbc.Label("Субъекты РФ"),
                dcc.Dropdown(
                    id='region_sel',
                    options=[{'label': x, 'value': x} for x in ['Выбрать все'] + sorted(df['subjects_RF'].unique())],
                    value=['Выбрать все'],
                    placeholder="Выберите регион",
                    multi=True,
                    clearable=False
                )
            ], xs=12, sm=6, md=3),
            dbc.Col([
                dbc.Label("Специальности"),
                dcc.Dropdown(
                    id='spec_sel',
                    options=[{'label': x, 'value': x} for x in ['Выбрать все'] + sorted(df['specialization'].unique())],
                    value=['Выбрать все'],
                    placeholder="Специальность",
                    multi=True,
                    clearable=False
                )
            ], xs=12, sm=6, md=3),
        ]),
        html.Br(),

        dbc.Row([
            dbc.Col([
                html.H4("Распределение количества вакансий", className='graph-title'),
                html.Div(
                dcc.Graph(id='quant-bar'), className='graph-card')
            ], xs=12, sm=6, md=8),

            dbc.Col([
                html.H4("Востребованные специальности и навыки", className='graph-title'),
                dbc.Tabs(id='spec_skil_spec', active_tab='spec', children=[
                    dbc.Tab(label='Топ 5 специальностей', tab_id='spec'),
                    dbc.Tab(label='Топ 5  навыков', tab_id='skil')
                ]),
                html.Div(
                dcc.Graph(id='spec_skil_bar'), className='graph-card')
            ], xs=12, sm=6, md=4),
        ]),
        html.Br(),

        dbc.Row([
            dbc.Col([
                html.H4("Показатели заработной платы на рынке труда", className='graph-title'),
                dbc.Tabs(id='salary_tabs', active_tab='distribution', className='graph-figure', children=[
                    dbc.Tab(label='Уровень зарплат', tab_id='distribution'),
                    dbc.Tab(label='Рейтинг оплаты труда', tab_id='average'),
                ]),
                html.Div( # чтобы была гипкость и однородность графиков
                dcc.Graph(id='salary-scatter'), className='graph-card'
                )
            ], xs=12, sm=6, md=6),

            dbc.Col([
                html.H4("Анализ зарплат по ключевым параметрам", className='graph-title'),
                dbc.Tabs(id='perc_tabs', active_tab='exp', children=[
                    dbc.Tab(label='Опыт', tab_id='exp'),
                    dbc.Tab(label='Образование', tab_id='edu'),
                    dbc.Tab(label='График работы', tab_id='sched'),
                ]),
                html.Div(
                dcc.Graph(id='perc-pie'), className='graph-card')
            ], xs=12, sm=6, md=6),
        ]),
        html.Br(),

        html.H4("Географическое распределение вакансий по России", className='graph-title'),
        html.Div(
        dcc.Graph(
            id='vacancy-map',
            style={'height': '600px', 'width': '100%'},
            config={
                'scrollZoom': True   # колесом мыши — масштабирование
            }
        ), className='graph-card'),
        html.Br(),

        # Подвал
        #html.Div("Выбрать все расчеты были произведены по данным за промежуток от 03.04.2025 по 05.05.2025", style={'fontStyle': 'italic'})
    ], fluid=True)


def last_tabs():
    """
    Вкладка «Прогноз зарплаты»
    - 5 dropdown’ов для параметров
    - кнопка «Рассчитать»
    - область вывода результата и списка вакансий
    """
    return dbc.Container([
        html.H2("Калькулятор рыночной зарплаты", className='headingstu'),
        html.Br(),

        dbc.Row([
            # Ввод параметров
            dbc.Col([
                dbc.Label("Город"),
                dcc.Dropdown(
                    id='input_city',
                    options=[{'label': c, 'value': c} for c in sorted(df_ML['city'].unique())],
                placeholder="Введите город",
                
                ),
                html.Br(),

                dbc.Label("Специализация"),
                dcc.Dropdown(
                    id='input_specialization',
                    options=[{'label': s, 'value': s} for s in sorted(df_ML['specialization'].unique())],
                placeholder="Введите специализацию",
                ),
                html.Br(),

                dbc.Label("Опыт"),
                dcc.Dropdown(
                    id='input_experience',
                    options=[{'label': e, 'value': e} for e in sorted(df_ML['experience'].unique())],
                placeholder="Введите опыт",
                ),
                html.Br(),

                dbc.Label("Образование"),
                dcc.Dropdown(
                    id='input_education',
                    options=[{'label': ed, 'value': ed} for ed in sorted(df_ML['education'].unique())],
                placeholder="Введите образование",
                ),
                html.Br(),

                dbc.Label("График работы"),
                dcc.Dropdown(
                    id='input_work',
                    options=[{'label': w, 'value': w} for w in sorted(df_ML['work_schedule'].unique())],
                placeholder="Введите график работы",
                ),
                html.Br(),

                dbc.Button("Рассчитать", id='button', class_name='button')
            ],  xs=12, sm=6, md=4),


            # Вывод результата
            dbc.Col([
                html.Div(id='ML_output', style={'fontSize': '24px', 'padding' :'5px', 'margin': '10px auto', 'text-align': 'center'}), #prediction-output'
                html.Div(id='vacancy_list')
            ],xs=12, sm=6, md=8),
        ])
    ], fluid=True)



def create_layout():
    """
    Главный layout с двумя вкладками:
    - Анализ данных
    - Прогноз уровня зарплатной платы
    """
    return dbc.Container([
        html.Div([
            html.H1(
                "Анализ Российского рынка труда в сфере информационных технологий",
                className='custom-header'
            )
        ]),
        dbc.Tabs(id='tabs', active_tab='tab-1', style={'font-weight': 'bold', 'font-size': '18px'}, children=[
            dbc.Tab(label='Аналитика', tab_id='tab-1'), 
            dbc.Tab(label='Прогноз уровня заработной платы', tab_id='tab-2'),
        ]),
        html.Div(id='tabs_content')
    ], fluid=True, style={'maxWidth': '98%'})
