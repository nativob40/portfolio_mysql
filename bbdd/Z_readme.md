# Importar y Exportar datos a una BD:

### Importar datos a una BD desde un archivo JSON.

    python manage.py loaddata ingles_db.json

### Exportar datos desde una BD a un archivo JSON.

    python manage.py dumpdata --indent 2 app_ingles --database ingles_db > ingles_db.json
