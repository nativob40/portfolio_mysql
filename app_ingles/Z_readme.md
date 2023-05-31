### Indicar en que BBDD se van a guardar los datos.

Ej:

    ####### TRADUCCION ######

    df_lista_de_verbos = pd.read_csv("/script/csv/ingles/traduccion.csv")

    df_lista_de_verbos.drop(["Unnamed: 0"], axis="columns", inplace=True)
    for i in range(len(df_lista_de_verbos.columns)):
        datos = Traduccion_de_verbos_ingles(
            verbo=df_lista_de_verbos.columns[i],
            traduccion_uno=df_lista_de_verbos.iloc[0].values[i],
            traduccion_dos=df_lista_de_verbos.iloc[1].values[i],
        )
        datos.save(using="ingles_db")

datos.save(**using="ingles_db"**) donde **"ingles_db"** es el nombre de la BBDD que digura en el archivo **settings.py**

### Hacer migracion a una BBDD especifica de una APP especifica

### Archivo settings.py

    MIXTA = {
        "italiano_db": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        },
        "ingles_db": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db_ingles.sqlite3",
        },
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "employees",
            "USER": "root",
            "PASSWORD": "Nuevopass00!",
            "HOST": "172.26.0.3",  #'172.26.0.3',
            "PORT": 3306,
        },
    }

### Comandos

    python manage.py makemigrations app_ingles

    python manage.py migrate app_ingles --database=ingles_db

Si aparece el error **django.db.utils.OperationalError: no such table:**, comentar la carga de datos. En este caso esta dentro del archivo **view.py**
