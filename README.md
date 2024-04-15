# Дипломная работа

Менеджер ключей

## Задача:

Нужно сделать HTTP сервис для одноразовых секретов
наподобие [https://onetimesecret.com/](https://onetimesecret.com/?locale=ru).

Он должен позволить создать секрет, задать кодовую фразу для его открытия и cгенерировать код, по которому можно
прочитать секрет только один раз. UI не нужен, это должен быть JSON Api сервис.

Для написание сервиса можно использовать [FastAPI](https://github.com/tiangolo/fastapi) или любой другой фреймворк.

- Метод `/generate` должен принимать секрет и кодовую фразу и отдавать `secret_key` по которому этот секрет можно
  получить.
- Метод `/secrets/{secret_key}` принимает на вход кодовую фразу и отдает секрет.

### Требования:

- Язык программирования: Python 3.7.
- Использование [Docker](https://www.docker.com/), сервис должен запускаться с
  помощью `[docker-compose up](https://docs.docker.com/compose/reference/up/)`.
- Требований к используемым технологиям нет.
- Код должен соответствовать PEP, необходимо использование type hints, к публичным методам должна быть написана
  документация на английском языке.

### Усложнения:

- Написаны тесты (постарайтесь достичь покрытия в 70% и больше). Вы можете
  использовать [pytest](https://docs.pytest.org/en/latest/) или любую другую библиотеку для тестирования.
- Сервис асинхронно обрабатывает запросы.
- Данные сервиса хранятся во внешнем хранилище, запуск которого также описан в `docker-compose`. Мы рекомендуем
  использовать [MongoDB](https://www.mongodb.com/), но Вы можете использовать любую подходящую базу.
- Секреты и кодовые фразы не хранятся в базе в открытом виде.
- Добавлена возможность задавать время жизни для секретов. Можно попробовать реализовать это с
  помощью [TTL индексов](https://docs.mongodb.com/manual/core/index-ttl/).

---

### Переменные среды

Шаблон файла [.env](.env.template)

| Переменная                      | Описание                                                                                      |
|---------------------------------|-----------------------------------------------------------------------------------------------|
| `APPLICATION__PASSWORD_GEN_LEN` | Длина генерируемого пароля                                                                    |
| `DATABASE__MONGO_DSN`           | Строка подключения к БД вида `mongodb://[username:password@]host[/[defaultauthdb][?options]]` |
| `DATABASE__MONGO_DB_NAME`       | Имя базы данных                                                                               |
| `APPLICATION__CORS_ORIGINS`     | Список разрешенных хостов для CORS                                                            |
| `APPLICATION__CORS_METHODS`     | Список разрешенных методов для CORS                                                           |
| `APPLICATION__CORS_HEADERS`     | Список разрешенных заголовков для CORS                                                        |


### Точка входа

```powershell
 python -m uvicorn src.main:app --host 0.0.0.0 --port 8080 --workers 2
```