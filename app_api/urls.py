from django.urls import path
from app_api.views import *

app_name = 'app_api'

urlpatterns = [
    path('departamentos', DepartamentosListAPIView.as_view(), name='lista_departamentos'),
    
               ]
