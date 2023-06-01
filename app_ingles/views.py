from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
import pandas as pd
from script.lectura_csv import Verbo
from .forms import Formulario_conjugacion_ingles, Formulario_traduccion_ingles
from .models import (
    Conjugacion_future,
    Conjugacion_present,
    Conjugacion_present_continuous,
    Conjugacion_preterite,
    Traduccion_de_verbos_ingles,
)

df_preterite = pd.read_csv("script/csv/ingles/preterite.csv")
df_present = pd.read_csv("script/csv/ingles/present.csv")
df_present_continuous = pd.read_csv("script/csv/ingles/present_continuous.csv")
df_future = pd.read_csv("script/csv/ingles/future.csv")
df_lista_de_verbos = pd.read_csv("script/csv/ingles/traduccion.csv")
df_lista_de_verbos.drop(["Unnamed: 0"], axis="columns", inplace=True)


class Resultados(TemplateView):
    template_name = "ingles/resultados.html"


class Juego(TemplateView):
    template_name = "ingles/juego_traduccion_ingles.html"

    correctas = 0
    incorrectas = 0
    listado_incorrectas = []

    def formulario_traduccion(request):
        if request.method == "POST":
            mi_formulario = Formulario_traduccion_ingles(request.POST)

            if mi_formulario.is_valid():
                datos = mi_formulario.cleaned_data
                verbo = Verbo.traduccion(
                    verbo=datos["verbo"],
                    palabra_en_español=datos["verbo_traducido"],
                    idioma="ingles",
                )

                if verbo[2] == "Correcto":
                    Juego.correctas += 1
                    verbo_eliminar = datos["verbo"]
                    df_present.drop([f"{verbo_eliminar}"], axis="columns", inplace=True)

                    if df_present.shape[1] - 1 == 0:  # Fin del Juego
                        Juego.reset()
                    else:
                        return render(
                            request,
                            "ingles/respuesta_correcta.html",
                            {"dato": datos, "significado": verbo[1]},
                        )
                else:
                    Juego.incorrectas += 1
                    Juego.listado_incorrectas.append(verbo)
                    return render(
                        request,
                        "ingles/respuesta_incorrecta.html",
                        {"dato": datos, "significado": verbo[1]},
                    )

        return render(request, "ingles/juego_traduccion.html")

    def reset(self):
        Juego.correctas = 0
        Juego.incorrectas = 0
        Juego.listado_incorrectas = []

        global df_present
        df_present = pd.read_csv("script/csv/ingles/present.csv")

        return HttpResponseRedirect("/ingles/juego")

    def get_context_data(self, **kwargs):
        v_aleatorio = Verbo.verbo_aleatorio(df_present)[0]
        context = super().get_context_data(**kwargs)

        ########### Cual es el significado del verbo? ###########
        context["etiqueta"] = v_aleatorio.upper()
        context["input_oculto"] = v_aleatorio

        ########### Tabla de Resultados ###########
        context["cantidad_de_verbos"] = df_present.shape[1] - 1
        context["porcentaje_cantidad_de_verbos"] = (df_present.shape[1] - 1) * 100 / 250
        # --------------------------------------------------------------------------------------#
        context["correctas"] = Juego.correctas
        context["porcentaje_correctas"] = Juego.correctas * 100 / 250
        # --------------------------------------------------------------------------------------#
        context["incorrectas"] = Juego.incorrectas
        context["porcentaje_incorrectas"] = Juego.incorrectas * 100 / 250

        ########### Tabla de Respuestas Incorrectas ###########
        context["tabla_significado"] = Juego.listado_incorrectas

        return context


class Listadeverbos(TemplateView):
    template_name = "ingles/tabla_de_verbos.html"

    df_lista_de_verbos = pd.read_csv(
        "/home/danilo/Python/Django/porfolio_mysql/script/csv/ingles/traduccion.csv"
    )
    df_lista_de_verbos.drop(["Unnamed: 0"], axis="columns", inplace=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ###########
        context["lista"] = Traduccion_de_verbos_ingles.objects.using("ingles_db").all()

        return context


class Conjugaciones(TemplateView):
    template_name = "ingles/conjugaciones.html"

    def present(verbo):
        persona = list(df_present["Unnamed: 0"])
        cant_personas = list(range(len(persona)))
        conjugacion = list(df_present[f"{verbo}"].values)

        dict_conjugacion = {
            "range": cant_personas,
            "persona": persona,
            "conjugacion": conjugacion,
        }
        print(dict_conjugacion)
        return dict_conjugacion

    def formulario_conjugacion(request):
        if request.method == "POST":
            mi_formulario = Formulario_conjugacion_ingles(request.POST)

            if mi_formulario.is_valid():
                datos = mi_formulario.cleaned_data
                verbo_conjugado_present = Conjugacion_present.objects.using(
                    "ingles_db"
                ).filter(verbo=datos["verbo"])
                verbo_conjugado_present_continuous = (
                    Conjugacion_present_continuous.objects.using("ingles_db").filter(
                        verbo=datos["verbo"]
                    )
                )
                verbo_conjugado_preterite = Conjugacion_preterite.objects.using(
                    "ingles_db"
                ).filter(verbo=datos["verbo"])
                verbo_conjugado_future = Conjugacion_future.objects.using(
                    "ingles_db"
                ).filter(verbo=datos["verbo"])

                return render(
                    request,
                    "ingles/conjugaciones.html",
                    {
                        "dato_present": verbo_conjugado_present,
                        "dato_present_continuous": verbo_conjugado_present_continuous,
                        "dato_preterite": verbo_conjugado_preterite,
                        "dato_future": verbo_conjugado_future,
                    },
                )
