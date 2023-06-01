from django.urls import path
from app_ingles.views import Juego, Conjugaciones, Listadeverbos

app_name = "app_ingles"

urlpatterns = [
    path("juego", Juego.as_view()),
    path("reset", Juego.reset),
    path("respuesta", Juego.formulario_traduccion),
    path("verboconjugado", Conjugaciones.formulario_conjugacion),
    path("conjugaciones", Conjugaciones.as_view()),
    path("listadeverbos", Listadeverbos.as_view()),
]
