# План - банан

## Что использовалось

- Python 3.11
- ASGI: FastAPI + uvicorn
- MongoDB: pymongo + motor
- AES: PyCryptodome

## Мы не знаем, что это такое...

### Шифруй его полностью...
#### Запрос

`POST: /generate`
```json
{
  "message": "hello",
  "secret_key": "password",
  "ttl": 0
}
```

#### Ответ

```json
{
  "status": "ok",
  "secret_id": "66237f3bf4abc2781dda6403",
  "secret_key": "password"
}
```

### Ну а дальше-то... дальше-то что?

#### Запрос
```
GET /secrets/66237f3bf4abc2781dda6403
-H secret_key: password
```

#### Ответ
```json
{
  "status": "ok",
  "data": "hello"
}
```

## Почему Mongo

- [x] Рекомендация
- [x] Желание попробовать новое
- [x] TTL индексы
- [x] Скорость - нет связей
- [x] Горизонтальная масштабируемость

### Альтернатива

- [x] Реляционная с триггерами
- [x] Реляционная с cron
- [x] Redis с TTL

### Проблемы

- [x] Не ACID (условно)
- [x] Запись на диск
- [x] Лицензия
- [x] TTL

### Архитектура

- [x] Паттерн репозиторий
- [x] Слабая связность
- [x] Легко тестировать
- [x] Легко заменить - одна точка входа

## Почему FastAPI

- [x] Рекомендация
- [x] Вкусно и точка!
- [x] Стильно! Модно! Молодежно! Компактно!
- [x] async - спасет Мир! ~~но это не точно~~
- [x] OpenAPI и Pydantic из коробки
- [x] REST, NoSQL

## Шифрование

- [x] Почему AES
- [x] Ключ - хеширование пароля SHA3-256 (32байта)
- [x] Шифрование AES-256 + вектор 128бит
- [x] Заброшенная библиотека Python - горе в семье

```python
from hashlib import sha3_256
from platform import system

platform = system().lower()

if platform == "windows":
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad, unpad
    from Cryptodome.Random import get_random_bytes
elif platform in ("linux", "darwin"):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
else:
    raise Exception(f"Unknown platform {platform}")

...

def encrypt(plaintext: str, key: str) -> bytes:
    key = sha3_256(key.encode()).digest()

    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    encrypted_data = iv + ciphertext

    return encrypted_data
...
```

#### Запрос

```json
{
  "message": "hello",
  "secret_key": "password",
  "ttl": 0
}
```

#### Результат

 _id                      | data                                         
--------------------------|----------------------------------------------
 66237f3af4abc2781dda6401 | zs3X2T0PswZnnQjapl1UwoNJ/EqU+ZyinVeK/ZTNuWU= 
 66237f3bf4abc2781dda6403 | l2kjD/PcnJ2tdhy1OorhNo4dr+Ma1FIoCAgtRogvIGU= 

## Тестирование

```sh
pytest --cov-report html --cov=.
```

```sh
pytest --cov-report term --cov=.
```

- [ ] Мочим настройки, подменяем БД - в репозитории
- [ ] Мочим репозиторий и шифровщик - в сервисах
- [ ] Мочим сервисы в API
- [ ] HTTPX

```
Name                                    Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------------------
src\config\application.py                   9      0      6      0   100%
src\config\database.py                      4      0      0      0   100%
src\config\settings.py                      8      0      0      0   100%
src\database\mongodb.py                    13      0      6      0   100%
src\exceptions\app_http_exception.py        3      0      0      0   100%
src\main.py                                17      0      4      0   100%
src\repository\repository_item.py          18      0      6      0   100%
src\repository\secret_data.py              21      0      2      0   100%
src\router\common.py                        6      0      2      0   100%
src\router\secret_data.py                  19      0      4      0   100%
src\schemas\common.py                       4      0      0      0   100%
src\schemas\create_secret_request.py        5      0      0      0   100%
src\schemas\create_secret_response.py       5      0      0      0   100%
src\schemas\exception.py                    3      0      0      0   100%
src\schemas\get_secret_response.py          4      0      0      0   100%
src\services\secret_data.py                30      0     10      0   100%
src\utils\common.py                         5      0      0      0   100%
src\utils\crypto.py                        25      5      4      1    72%
-------------------------------------------------------------------------
TOTAL                                     199      5     44      1    97%

```
