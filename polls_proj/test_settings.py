from .settings import *

# Use in-memory SQLite for local test runs to avoid external DB dependency.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
