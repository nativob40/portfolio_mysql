from django.urls import path

# from . import views
from app_ingles.views import Juego, Resultados, Conjugaciones, Listadeverbos


app_name = "app_ingles"

urlpatterns = [
    path("juego", Juego.as_view()),
    path("reset", Juego.reset),
    # path("resultados", Resultados.as_view()),  # ESTO SOLO SE USA PARA CARGAR LOS VERBOS A LA BBDD.
    path("respuesta", Juego.formulario_traduccion),
    path("verboconjugado", Conjugaciones.formulario_conjugacion),
    path("conjugaciones", Conjugaciones.as_view()),
    path("listadeverbos", Listadeverbos.as_view()),
]
