# словарь для поиска вакансий на Superjob
dict_sj = {
    "Разработчики": [
        {"key": 48, "title": "Программист, разработчик"},
        {"key": 604, "title": "Программист, разработчик"},
        {"key": 36, "title": "Программист, разработчик"},
         {"key": 40, "title": "Программист, разработчик"},
         {"key": 42, "title": "Программист, разработчик"},
        {"key": 47, "title": "Программист, разработчик"}
    ],
    "Аналитики": [
        {"key": 38, "title": "Аналитик"}
    ],
    "Инженеры": [
        {"key": 49, "title": "Сетевой инженер"},
        {"key": 51, "title": "Системный администратор"},
        {"key": 628, "title": "DevOps-инженер"},
        {"key": 629, "title": "DevOps-инженер"},
        {"key": 503, "title": "DevOps-инженер"},
        {"key": 37, "title": "Администрирование баз данных"},
        {"key": 55, "title": "Системный инженер"}
    ],
    "Прочие": [
        {"key": 43, "title": "Дизайнер, художник"},
        {"key": 56, "title": "Тестировщик"},
        {"key": 650, "title": "Дата-сайентист"},
        {"key": 627, "title": "Дата-сайентист"}, 
        {"key": 546, "title": "Информационная безопасность"}
    ]
}


# Категории профессий hh.ru по id
dict_hh = {
    "Разработчики": [
        {"id": 96, "name": "Программист, разработчик"},
        {"id": 104, "name": "Руководитель группы разработки"}
       
    ],
    "Аналитики": [
        {"id": 156, "name": "BI-аналитик, аналитик данных"},
        {"id": 10, "name": "Аналитик"},
        {"id": 150, "name": "Бизнес-аналитик"},
        {"id": 164, "name": "Продуктовый аналитик"},
        {"id": 148, "name": "Системный аналитик"},
        {"id": 157, "name": "Руководитель отдела аналитики"}
    ],
    "Инженеры": [
        {"id": 160, "name": "DevOps-инженер"},
        {"id": 112, "name": "Сетевой инженер"},
        {"id": 113, "name": "Системный администратор"},
        {"id": 114, "name": "Системный инженер"}
    ],
    "Прочие": [
        {"id": 12, "name": "Арт-директор, креативный директор"},
        {"id": 25, "name": "Гейм-дизайнер"},
        {"id": 34, "name": "Дизайнер, художник"},
        {"id": 36, "name": "Директор по информационным технологиям (CIO)"},
        {"id": 73, "name": "Менеджер продукта"},
        {"id": 155, "name": "Методолог"},
        {"id": 165, "name": "Дата-сайентист"},
        {"id": 116, "name": "Информационная безопасность"},
        {"id": 107, "name": "Руководитель проектов"},
        {"id": 121, "name": "Специалист технической поддержки"},
        {"id": 124, "name": "Тестировщик"},
        {"id": 125, "name": "Технический директор (CTO)"},
        {"id": 126, "name": "Технический писатель"}
    ]
}

# Список с ключевыми навыками в сфере информативных технологий
list_skills = ['microservices', 'github', '1с', 'git', 'django', 'android studio', 'grpc', 'machine learning', 'ms project', 'elasticsearch',
'mqtt', 'flutter', 'spacy', 'pycharm', 'apache', 'power bi', 'nestjs', 'graphql', 'selenium', 'unreal engine', 'sqlite',
'оптимизация sql', 'c#', 'spring', 'redshift', 'macos', 'безопасность', 'jira', 'circleci', 'kubernetes', 'лидерство', 'soap',
'work-life balance', 'межличностные навыки', 'scala', 'logstash', 'neo4j', 'access', 'hadoop', 'индексы', 'gitlab', 'azure',
'traefik', 'dry', 'adobe photoshop', 'godot', 'оптимизация производительности', 'mariadb', 'prometheus', 'tensorflow', 'eclipse',
'opencv', 'ruby', 'python', 'redis', 'google sheets', 'notion', 'hive', 'эмоциональный интеллект', 'optuna', 'canva', 'powershell',
'webpack', 'asana', 'xcode', 'unity', 'haskell', 'scrum', 'solid', 'numpy', 'kibana', 'tdd', 'unit testing', 'управление проектами',
'репликация', 'testng', 'angular', 'yandex cloud', 'monolith', 'webstorm', 'clickup', 'мультизадачность', 'matplotlib', 'less', 'bash',
'c', 'bootstrap', 'тайм-менеджмент', 'английский язык', 'plotly', 'scikit-learn', 'kiss', 'программирование', 'самоорганизация',
'clickhouse', 'jquery', 'oop', 'nltk', 'mocha', 'решение проблем', 'react native', 'rest api', 'hugging face', 'cypress', 'lightgbm',
'bdd', 'metabase', 'управление конфликтами', 'allure', 'illustrator', 'кросс-функциональное взаимодействие', 'hyperledger', 'soapui',
'outlook', 'kotlin', 'flask', 'микросервисы', 'superset', 'коммуникативные навыки', 'raspberry pi', 'sql', 'ооп', 'iot', 'keras',
'swift', 'excel', 'adobe xd', 'блокчейн', 'расстановка приоритетов', 'rest', 'ruby on rails', 'google cloud', 'elixir', 'argocd',
'gpt', 'docker', 'jmeter', 'solidity', 'гибкость', 'powerpoint', 'кэширование', 'spark', 'playwright', 'статистика', 'gulp', 
'figma', 'swiftui', 'terraform', 'rabbitmq', 'pytest', 'scipy', 'oracle', 'openapi', 'обучаемость', 'html', 'looker', 'работа в команде',
'agile', 'matlab', 'стрессоустойчивость', 'аналитическое мышление', 'react', 'confluence', 'nuxt.js', 'flink', 'pl/sql', 'принятие решений',
'iis', 'aws', 'zephyr', 'perl', 'grafana', 'структуры данных', 'word', 'vite', 'github actions', 'техническая документация', 'jest',
'express.js', 'mongodb', 'шардинг', 'javascript', 'laravel', 'snowflake', 'linux', 'php', 'ubuntu', 'cassandra', 'dask', 'trello',
'jenkins', 'big data', 'креативность', 'c++', 'firebase', 'tailwind css', 'delphi', 'bigquery', 'openstack', 'groovy', 'bitbucket',
'адаптивность', 'коммуникабельность', 'командная работа', 'junit', 'rust', 'microsoft word', 'gamedev', 'pytorch', 'xgboost', 'dart',
'ansible', 'airflow', 'fastapi', 'postgresql', 'vue.js', 'анализ данных', 'docker swarm', 'clean architecture', 'vs code', 'внимание к деталям',
'phoenix', 'appium', 'vue', 'android sdk', 'gcp', 'testrail', 'tableau', 'typescript', 'asp.net', 'ethereum', 'arduino', 'google slides',
'ci/cd', 'data analysis', 'css', 'kafka', 'design patterns', 'gatling', 'windows', 'helm', 'kanban', 'databricks', 'go', 'qlikview',
'seaborn', 'критическое мышление', 'mvc', 'ddd', 'qlik sense', 'базы данных', 'spring boot', 'ms sql server', 'pandas', 'polars',
'алгоритмы', 'windows server', 'zsh', 'catboost', 'postman', 'intellij idea', 'locust', 'sass', 'sas', 'java', 'системное мышление',
'bert', 'swagger', 'next.js', 'data science', 'r', 'mysql', 'dynamodb', 'gitlab ci/cd', 'работа с неопределенностью', 'vba', 'visio',
'nginx', 'lua', 'hbase']

# -*- coding: utf-8 -*-
# Списки имён признаков для подготовки входа в модель

# Категориальные признаки
cat_features_names = [
    'city',
    'profession_category',
    'specialization',
    'experience',
    'work_schedule',
    'education'
]

# Числовые признаки
num_features_names = ['salary_up']
