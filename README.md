# ⚡ fast-short-url

Минималистичный, быстрый и аккуратно спроектированный сервис сокращения ссылок на **FastAPI + PostgreSQL + SQLAlchemy 2.x**.

Без лишней магии. Без legacy. Только то, что нужно.

## 🚀 Возможности

- Сокращение URL
- TTL (время жизни ссылок)
- Счётчик переходов
- Фоновая очистка просроченных ссылок
- Разделение логики (service / db / api)


## 🧱 Стек

- **Python 3.14**
- **FastAPI**
- **SQLAlchemy 2.x**
- **PostgreSQL**
- **Alembic**
- **Pydantic v2**

## 📦 Установка

```bash
git clone https://github.com/1ns0mn1a7/fast-short-url.git
cd fast-short-url

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## ⚙️ Конфигурация

Все настройки через **Pydantic Settings**.

`ENV`
```env
DATABASE_URL=postgresql+psycopg://admin:password@localhost:5432/shortener
DEBUG=true
```

`app/config.py` уже всё подхватывает автоматически.

## 🗄 База данных

Создать БД:
```sql
CREATE DATABASE shortener;
```

Применить миграции:
```bash
alembic upgrade head
```

## ▶️ Запуск
```bash
fastapi dev app/main.py
```
Документация:

- Swagger → http://127.0.0.1:8000/docs
- OpenAPI → http://127.0.0.1:8000/openapi.json

## API

### Создать короткую ссылку

`POST /shorten`

```json
{
  "url": "https://example.com"
}
```

Ответ:
```json
{
  "short_url": "aB9xQ2"
}
```

### Редирект

`GET /{code}`

- `307` Temporary Redirect
- `404`, если ссылка истекла или не существует

### Статистика

`GET /{code}/stats`

Ответ:

```json
{
  "code": "aB9xQ2",
  "clicks": 42
}
```

## 🧹 Очистка ссылок с истеченным сроком

- Автоматически запускается через `BackgroundTasks`
- Удаляет все ссылки, у которых `expires_at < now(UTC)`

```python
service.cleanup_expired_links()
```

## Цель проекта

Проект написан в учебных целях, Fast API сила!