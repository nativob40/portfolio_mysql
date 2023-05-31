from django.contrib import admin
from app_ingles.models import *


# Register your models here.

# Esto es para ver los datos en el panel de ADMIN


@admin.register(Traduccion_de_verbos_ingles)
class Traduccion_de_verbos_ingles_Admin(admin.ModelAdmin):
    list_display = ("id", "verbo", "traduccion_uno", "traduccion_dos")

    def get_queryset(self, request):
        # Esto es para cuando tengo varias bbdd.
        return super().get_queryset(request).using("ingles_db")


@admin.register(Conjugacion_preterite)
class Conjugacion_preterite_Admin(admin.ModelAdmin):
    list_display = ("id", "verbo", "persona", "conjugacion")

    def get_queryset(self, request):
        # Esto es para cuando tengo varias bbdd.
        return super().get_queryset(request).using("ingles_db")


@admin.register(Conjugacion_present)
class Conjugacion_present_Admin(admin.ModelAdmin):
    list_display = ("id", "verbo", "persona", "conjugacion")

    def get_queryset(self, request):
        # Esto es para cuando tengo varias bbdd.
        return super().get_queryset(request).using("ingles_db")


@admin.register(Conjugacion_present_continuous)
class Conjugacion_present_continuous_Admin(admin.ModelAdmin):
    list_display = ("id", "verbo", "persona", "auxiliar", "conjugacion")

    def get_queryset(self, request):
        # Esto es para cuando tengo varias bbdd.
        return super().get_queryset(request).using("ingles_db")


@admin.register(Conjugacion_future)
class Conjugacion_future_Admin(admin.ModelAdmin):
    list_display = ("id", "verbo", "persona", "auxiliar", "conjugacion")

    def get_queryset(self, request):
        # Esto es para cuando tengo varias bbdd.
        return super().get_queryset(request).using("ingles_db")
