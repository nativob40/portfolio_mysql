from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
import pandas as pd
from script.lectura_csv import Verbo
from .forms import Formulario_traduccion, Formulario_conjugacion
from .models import (
    Conjugacion_futuro_semplice,
    Conjugacion_presente_semplice,
    Conjugacion_passato_prossimo,
    Traduccion_de_verbos,
)


df_presente_simple = pd.read_csv("script/csv/presente.csv")
df_passato_prossimo = pd.read_csv("script/csv/passato_prossimo.csv")
df_futuro_semplice = pd.read_csv("script/csv/futuro_semplice.csv")

df_traduccion = pd.read_csv("script/csv/traduccion.csv")
df_traduccion.drop(["Unnamed: 0"], axis="columns", inplace=True)

################################ ESTO SOLO SE USA PARA CARGAR LOS VERBOS A LA BBDD ############################

"""   
############################################ TRADUCCION ########################################################

df_lista_de_verbos = pd.read_csv('script/csv/traduccion.csv')
df_lista_de_verbos.drop(['Unnamed: 0'], axis = 'columns', inplace=True)

for i in range(len(df_lista_de_verbos.columns)):
    datos = Traduccion_de_verbos(verbo = df_lista_de_verbos.columns[i],
                                traduccion_uno = df_lista_de_verbos.iloc[0].values[i],
                                traduccion_dos = df_lista_de_verbos.iloc[1].values[i])
    datos.save()

############################################ PRESENTE SEMPLICE ########################################################

for verbos in range(1,len(df_presente_simple.columns)):
    for i in range(len(df_presente_simple)):
        datos = Conjugacion_presente_semplice(verbo = df_presente_simple.columns[verbos],
                                              persona = df_presente_simple['Unnamed: 0'][i],
                                              conjugacion = df_presente_simple[f'{df_presente_simple.columns[verbos]}'][i])
        datos.save()

############################################ PASSATO PROSSIMO ########################################################

for verbos in range(1,len(df_passato_prossimo.columns)):
    for i in range(len(df_passato_prossimo)):
        aux,verbo_conjugado = df_passato_prossimo[f'{df_passato_prossimo.columns[verbos]}'][i].split(' ')
        datos = Conjugacion_passato_prossimo(verbo = df_passato_prossimo.columns[verbos],
                                              persona = df_passato_prossimo['Unnamed: 0'][i],
                                              auxiliar = aux,
                                              conjugacion = verbo_conjugado)
        datos.save() 

############################################ FUTURO SEMPLICE ########################################################

for verbos in range(1,len(df_futuro_semplice.columns)):
    for i in range(len(df_futuro_semplice)):
        datos = Conjugacion_futuro_semplice(verbo = df_futuro_semplice.columns[verbos],
                                              persona = df_futuro_semplice['Unnamed: 0'][i],
                                              conjugacion = df_futuro_semplice[f'{df_futuro_semplice.columns[verbos]}'][i])
        datos.save()
"""

###############################################################################################################


class Resultados(TemplateView):
    template_name = "italiano/resultados.html"


class Juego(TemplateView):
    template_name = "italiano/juego_traduccion_italiano.html"

    correctas = 0
    incorrectas = 0
    listado_incorrectas = []

    def formulario_traduccion(request):
        if request.method == "POST":
            mi_formulario = Formulario_traduccion(request.POST)

            if mi_formulario.is_valid():
                datos = mi_formulario.cleaned_data
                verbo = Verbo.traduccion(
                    verbo=datos["verbo"],
                    palabra_en_español=datos["verbo_traducido"],
                    idioma="italiano",
                )

                if verbo[2] == "Correcto":
                    Juego.correctas += 1
                    verbo_eliminar = datos["verbo"]
                    df_presente_simple.drop(
                        [f"{verbo_eliminar}"], axis="columns", inplace=True
                    )

                    if df_presente_simple.shape[1] - 1 == 0:  # Fin del Juego
                        Juego.reset()
                    else:
                        return render(
                            request,
                            "italiano/respuesta_correcta.html",
                            {"dato": datos, "significado": verbo[1]},
                        )
                else:
                    Juego.incorrectas += 1
                    Juego.listado_incorrectas.append(verbo)
                    return render(
                        request,
                        "italiano/respuesta_incorrecta.html",
                        {"dato": datos, "significado": verbo[1]},
                    )

        return render(request, "italiano/juego_traduccion_italiano.html")

    def reset(self):
        Juego.correctas = 0
        Juego.incorrectas = 0
        Juego.listado_incorrectas = []

        global df_presente_simple
        df_presente_simple = pd.read_csv("script/csv/presente.csv")

        return HttpResponseRedirect("/italiano/juego")

    def get_context_data(self, **kwargs):
        v_aleatorio = Verbo.verbo_aleatorio(df_presente_simple)[0]
        context = super().get_context_data(**kwargs)

        ########### Cual es el significado del verbo? ###########
        context["etiqueta"] = v_aleatorio.upper()
        context["input_oculto"] = v_aleatorio

        ########### Tabla de Resultados ###########
        context["cantidad_de_verbos"] = df_presente_simple.shape[1] - 1
        context["porcentaje_cantidad_de_verbos"] = (
            (df_presente_simple.shape[1] - 1) * 100 / 250
        )
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
    template_name = "italiano/tabla_de_verbos.html"

    df_lista_de_verbos = pd.read_csv("script/csv/traduccion.csv")
    df_lista_de_verbos.drop(["Unnamed: 0"], axis="columns", inplace=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ###########
        context["lista"] = Traduccion_de_verbos.objects.using("italiano_db").all()

        return context


class Conjugaciones(TemplateView):
    template_name = "italiano/conjugaciones.html"

    def presente(verbo):
        persona = list(df_presente_simple["Unnamed: 0"])
        cant_personas = list(range(len(persona)))
        conjugacion = list(df_presente_simple[f"{verbo}"].values)

        dict_conjugacion = {
            "range": cant_personas,
            "persona": persona,
            "conjugacion": conjugacion,
        }
        print(dict_conjugacion)
        return dict_conjugacion

    def formulario_conjugacion(request):
        if request.method == "POST":
            mi_formulario = Formulario_conjugacion(request.POST)

            if mi_formulario.is_valid():
                datos = mi_formulario.cleaned_data
                verbo_conjugado_presente = Conjugacion_presente_semplice.objects.using(
                    "italiano_db"
                ).filter(verbo=datos["verbo"])
                verbo_conjugado_pasado = Conjugacion_passato_prossimo.objects.using(
                    "italiano_db"
                ).filter(verbo=datos["verbo"])
                verbo_conjugado_futuro = Conjugacion_futuro_semplice.objects.using(
                    "italiano_db"
                ).filter(verbo=datos["verbo"])

                return render(
                    request,
                    "italiano/conjugaciones.html",
                    {
                        "dato_presente_semplice": verbo_conjugado_presente,
                        "dato_passato_prossimo": verbo_conjugado_pasado,
                        "dato_futuro_semplice": verbo_conjugado_futuro,
                    },
                )


def about(request):
    return render(request, "about.html")
