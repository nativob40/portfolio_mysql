from django.urls import path
from . import views
from app_dashboard.views import Dash_uno

app_name = 'app_dashoard'

urlpatterns = [
    path('',Dash_uno.as_view()),
    path('test',views.Dash_uno.testing),
    ]