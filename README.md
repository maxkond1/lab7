# Voting App (Django)

Приложение для голосования с Docker и PostgreSQL.

Запуск (локально с Docker):

```bash
# в корне проекта
docker-compose build
docker-compose up -d
# выполнить миграции
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Проект содержит:
- Django + DRF
- Модель `Poll`, `Option`, `Vote`
- Базовая модель с `created_at`/`updated_at`
- Админка и экспорт XLSX

Сделайте git-репозиторий и запушьте на GitHub, затем пришлите ссылку.

Локальная установка виртуального окружения (Windows PowerShell):

```powershell
# Создать и активировать виртуальное окружение
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1

# Установить зависимости и выполнить миграции
python -m pip install --upgrade pip
```markdown
# Voting App (Django)

Приложение для голосования с использованием Docker и PostgreSQL.

Запуск через Docker (рекомендуемый способ):

```bash
# В корне проекта
docker-compose build
docker-compose up -d
# Выполнить миграции и создать суперпользователя
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Кратко про проект:
- Django + Django REST Framework
- Модели: `Poll`, `Option`, `Vote`
- Абстрактная базовая модель с `created_at`/`updated_at`
- Административная панель и экспорт в XLSX (openpyxl)

Локальная установка (Windows PowerShell):

```powershell
# Создать и активировать виртуальное окружение
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1

# Установить зависимости и выполнить миграции
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Также можно запустить скрипт `setup_venv.ps1` в корне проекта для автоматизации этих шагов:

```powershell
./setup_venv.ps1
```

Docker: статические файлы и media

- Сервис `web` выполняет `migrate` и `collectstatic` при старте. Статические файлы собираются в `staticfiles/` и обслуживаются WhiteNoise.
- Загружаемые media-файлы сохраняются на хосте в папке `media/` (смонтирована в контейнер). Убедитесь, что папка `media/` существует и доступна для записи.

Запуск (повтор):

```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Откройте в браузере http://localhost:8000. Загруженные media доступны по пути `/media/`.

Демo-данные
-----------
Чтобы создать демонстрационные учётные записи и примеры опросов, выполните (в контейнере):

```bash
docker-compose exec web python manage.py createdemo
```

Или локально в venv (если база данных доступна из окружения):

```powershell
# Активировать .venv
python manage.py createdemo
```

Дефолтные демо‑учётные данные, создаваемые командой:

- Админ: `admin` / `Secur3Pass!`
- Пользователь: `user1` / `pass1234`

Эти учётные данные можно использовать для входа в админку: `http://localhost:8000/admin` и для тестирования голосования от зарегистрированного пользователя.

```
