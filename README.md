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
