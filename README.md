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
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Или запустите `setup_venv.ps1` в корне проекта: 

```powershell
./setup_venv.ps1
```

Docker notes (static & media):

- The `web` service runs `migrate` and `collectstatic` on start. Static files are collected to `staticfiles/` and served by WhiteNoise.
- Media uploads are stored on the host in the `media/` folder (mounted into the container). Ensure `media/` exists and is writable.

Start with Docker Compose:

```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

After startup, open http://localhost:8000. Uploaded media will be available under `/media/`.

Demo data
---------
To create demo users and polls run (inside container):

```bash
docker-compose exec web python manage.py createdemo
```

Or locally in venv (ensure DB is reachable):

```powershell
#.venv\Scripts\Activate.ps1
#DB_HOST=localhost
python manage.py createdemo
```

Default demo credentials created by this command:

- Admin: `admin` / `Secur3Pass!`
- User: `user1` / `pass1234`

Use these to log into the admin at `http://localhost:8000/admin` or to test registered-user voting.
