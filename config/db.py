import os


MIXTA = {
    'italiano_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'employees',
        'USER': 'root',
        'PASSWORD': 'Nuevopass00!',
        'HOST': '172.21.0.2',#'172.26.0.3',
        'PORT': 3306,
    }
}

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },}

MYSQL = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'employees',
        'USER': 'root',
        'PASSWORD': 'Nuevopass00!',
        'HOST': '172.26.0.3',
        'PORT': 3306,
    }
}
