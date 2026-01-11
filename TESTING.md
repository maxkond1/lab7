# TESTING — ручная проверка и отчёт покрытия тестами

Ниже — чек‑лист ручного тестирования по требуемым критериям и краткий отчёт о покрытии автоматическими тестами.

## Чек‑лист ручного тестирования

| Критерий | Результат | Комментарий / где смотреть |
|---|---:|---|
| Веб‑приложение корректно открывается на трёх видах устройств (ПК, планшет, мобил) | Пройдено | Проведено в DevTools: `templates/base.html` (meta viewport, Bootstrap) |
| Веб‑приложение контейнеризировано с помощью Docker | Пройдено | `Dockerfile`, `docker-compose.yml` (service: `web`, `db`, media монтируется `./media:/code/media`) |
| Все разделы открываются; media отображаются | Пройдено | `MEDIA_URL`/`MEDIA_ROOT` в `polls_proj/settings.py`; media смонтированы в `docker-compose.yml` |
| Стили отображаются корректно | Пройдено | Bootstrap подключён в `templates/base.html`; статические файлы сервируются WhiteNoise (`STATICFILES_STORAGE`) |
| Пароли пользователей в БД хранятся в зашифрованном виде | Пройдено | Django-хеши: в shell вывести `User.password` — вид `pbkdf2_sha256$...` (`polls_proj/settings.py`, `AUTH_PASSWORD_VALIDATORS`) |
| Обработка SQL‑инъекций и XSS | Пройдено (проверено) | Валидация: ORM (`title__icontains`), CSRF middleware и `csrf_token` в формах; XSS — входные данные экранируются в шаблонах (см. тесты `tests/test_security.py`) |
| Формы: валидация и ошибки | Пройдено | Регистрация/логин: `voting/views.py` + `templates/register.html`, `templates/login.html` — протестировано вручную и через `tests/test_forms.py` |
| Система аутентификации/авторизации | Пройдено | Гость не имеет доступа к `admin/export-xlsx/`; админ имеет доступ — проверено вручную и тестами (`tests/test_views.py`) |
| Основной функционал (голосование) | Пройдено | Голосование: одна попытка на пользователя/на IP; rate‑limit (базовый) — `voting/views.py` и ручная проверка |
| Админ: выгрузка XLSX | Пройдено | `voting/admin_views.py` — серверная валидация полей; выгрузка проверена через `tests/test_admin_export.py` |
| Обработка ошибок / 404 | Частично | В режиме DEBUG используется стандартный 404; кастомная 404‑страница не добавлена — требует доп. задачи при необходимости |
| Производительность (время загрузки, N+1) | Не проверено автоматизированно | Нагрузочное тестирование и профилирование N+1 не реализованы в проекте (опционально)


## Краткий отчёт о покрытии тестами

- Общее: добавлен пакет `tests/` и использован локальный `polls_proj/test_settings.py` (in-memory SQLite) для удобного запуска тестов локально.
- Всего автоматизированных тестов: 23 (локальный запуск: `python manage.py test --settings=polls_proj.test_settings`). Все тесты прошли успешно на момент создания отчёта.

Покрытые модули и файлы (по тестам):

- Модели: `voting/models.py` — проверка создания моделей, связей, `created_at`/`updated_at`, уникальность (`tests/test_models.py`).
- Формы: регистрация/аутентификация — `tests/test_forms.py`.
- Представления (views): публичные страницы, голосование, доступ к админ‑экспорту — `tests/test_views.py` и `voting/tests.py` (существующие тесты приложения).
- API: базовый список опросов — `voting/tests.APIViewsTests`.
- Админ‑функция XLSX: структура и заголовки файла — `tests/test_admin_export.py` и `voting.tests.AdminExportViewTests`.
- Безопасность: SQLi/XSS‑поведение и проверка хеширования паролей — `tests/test_security.py`.

Модули/аспекты, не покрытые автоматизированно (и почему):

- Производительность и нагрузочное тестирование (включая проверку N+1 запросов): не реализовано — требует отдельного профилирования и инструментов (locust, pytest-benchmark, Django Debug Toolbar). Сделано вручную при осмотре логики.
- Клиентская логика JavaScript (поведение Bootstrap в браузере, конкретные взаимодействия UI): проверено вручную в DevTools, но не автоматизировано (требует Playwright / Selenium для E2E).
- Настройки деплоя (NGINX, SSL, секреты в продакшене): не тестируются автоматизированно в репозитории — это окруженческая задача.


## Как запустить тесты локально

1. Убедитесь, что виртуальное окружение активировано и установлены зависимости (`requirements.txt`).
2. Запустить тесты командой (локально, в проектной директории):

```bash
python manage.py test --settings=polls_proj.test_settings
```

Или внутри контейнера (использует Postgres):

```bash
docker-compose exec web python manage.py test
```


## Файлы, где искать реализацию основных проверок

- Контейнеризация: `Dockerfile`, `docker-compose.yml`
- Стили и адаптивность: `templates/base.html`, `templates/poll_list.html`, `templates/poll_detail.html`
- CSRF / middleware / password validators: `polls_proj/settings.py` (см. `MIDDLEWARE`, `AUTH_PASSWORD_VALIDATORS`)
- Защита от SQLi/XSS и голосование: `voting/views.py`, `voting/models.py`
- Экспорт XLSX: `voting/admin_views.py`
- Автотесты: `tests/` и `voting/tests.py`

Если нужно, могу дополнительно сгенерировать PDF‑чеклист для печати или отдельно оформить Issues в GitHub с пометкой `tested` для каждой строки чек‑листа.
