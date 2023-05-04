
from django.urls import path
from . import views
from app_italiano.views import Juego,Listadeverbos,Conjugaciones


app_name = 'app_italiano'

urlpatterns = [

    path('juego',Juego.as_view()),
    path('reset',views.Juego.reset),
    #path('resultados',Resultados.as_view()), # ESTO SOLO SE USA PARA CARGAR LOS VERBOS A LA BBDD.
    path('respuesta',views.Juego.formulario_traduccion),
    path('verboconjugado',views.Conjugaciones.formulario_conjugacion),
    path('conjugaciones',Conjugaciones.as_view()),
    path('listadeverbos',Listadeverbos.as_view()),

]