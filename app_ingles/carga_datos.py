########################################################################
#                                                                      #
#           ESTO SOLO SE USA PARA CARGAR LOS VERBOS A LA BBDD          #
#                                                                      #
########################################################################


import pandas as pd

# from script.lectura_csv import Verbo
from models import (
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


############################################ TRADUCCION ########################################################

df_lista_de_verbos = pd.read_csv("script/csv/ingles/traduccion.csv")
df_lista_de_verbos.drop(["Unnamed: 0"], axis="columns", inplace=True)

for i in range(len(df_lista_de_verbos.columns)):
    datos = Traduccion_de_verbos_ingles(
        verbo=df_lista_de_verbos.columns[i],
        traduccion_uno=df_lista_de_verbos.iloc[0].values[i],
        traduccion_dos=df_lista_de_verbos.iloc[1].values[i],
    )
    datos.save()

############################################ PRETERITE ########################################################

for verbos in range(1, len(df_preterite.columns)):
    for i in range(len(df_preterite)):
        datos = Conjugacion_preterite(
            verbo=df_preterite.columns[verbos],
            persona=df_preterite["Unnamed: 0"][i],
            conjugacion=df_preterite[f"{df_preterite.columns[verbos]}"][i],
        )
        datos.save()


############################################ PRESENT ########################################################

for verbos in range(1, len(df_present.columns)):
    for i in range(len(df_present)):
        datos = Conjugacion_present(
            verbo=df_present.columns[verbos],
            persona=df_present["Unnamed: 0"][i],
            conjugacion=df_present[f"{df_present.columns[verbos]}"][i],
        )
        datos.save()


for verbos in range(1, len(df_present_continuous.columns)):
    for i in range(len(df_present_continuous)):
        aux, verbo_conjugado = df_present_continuous[
            f"{df_present_continuous.columns[verbos]}"
        ][i].split(" ")
        datos = Conjugacion_present_continuous(
            verbo=df_present_continuous.columns[verbos],
            persona=df_present_continuous["Unnamed: 0"][i],
            auxiliar=aux,
            conjugacion=df_present_continuous[
                f"{df_present_continuous.columns[verbos]}"
            ][i],
        )
        datos.save()


############################################ FUTURE ########################################################

for verbos in range(1, len(df_future.columns)):
    for i in range(len(df_future)):
        aux, verbo_conjugado = df_future[f"{df_future.columns[verbos]}"][i].split(" ")
        datos = Conjugacion_future(
            verbo=df_future.columns[verbos],
            persona=df_future["Unnamed: 0"][i],
            conjugacion=verbo_conjugado,
        )
        datos.save()


###############################################################################################################
