### Тестовое задание по созданию API и получению данных с сайта [mosmetro.ru](https://www.mosmetro.ru)

Для запуска необходим файл с переменными окружения `.env`
```text
POSTGRES_CONTAINER_PASSWORD=example
PUBLIC_IP_ADDRESS=127.0.0.1
```
`POSTGRES_CONTAINER_PASSWORD` - пароль пользователя postgres  
`PUBLIC_IP_ADDRESS` - IP адрес интерфейса на котором будут доступны контейнеры

Пример запуска с одновременной сборкой контейнеров:
```text
> docker-compose up --build
```

#### Контейнеры

В файле `docker-compose.yaml` указаны параметры сборки и запуска следующих контейнеров:
- `database (postgres_1)` - база данных PostgreSQL (публичный порт 9432)
- `scraper (scraper_1)` - получения данных [/press/news](https://www.mosmetro.ru/press/news), 
  интервал опроса 10 минут
- `application (application_1)` – приложение Flask (публичный порт 8181), запущено через Gunicorn

#### API

```text
GET /metro/news?days={0}
```

Получение списка новостей за `{0}` дней начиная с текущей даты (значение по умолчанию 5)

Пример выполнения запроса с помощью curl:
```text
> curl http://127.0.0.1:8181/metro/news?days=10
```

Ответ в формате JSON:
```text
{
    "news": [
        {
            "news_title": "Карта «Тройка» заработает в вашем смартфоне в этом году",
            "image_url": "https://www.mosmetro.ru/.../f2bfaefe5e7c2576a746105835d510f3.jpg",
            "public_date":"2021-01-22"
        }, {
            
            ...
            
        }
    ],
    "period": ["2021-01-23","2021-01-13"]
}
```

#### Тест

Простой тест производительности с постепенно возрастающим профилем нагрузки  
- параметры: `/metro/news?days={0}` 0-10
- процессы: 5
- запросы: 100-1500
```text
> python simple_load_test.py
```

Результат:
```text
requests: 100, days: 2, exec: 0.807, rps: 124
requests: 200, days: 4, exec: 1.633, rps: 122
requests: 300, days: 10, exec: 2.532, rps: 118
...
requests: 1300, days: 6, exec: 10.461, rps: 124
requests: 1400, days: 1, exec: 10.925, rps: 128
requests: 1500, days: 0, exec: 11.703, rps: 128
requests: 12000, avg rps: 125
```
