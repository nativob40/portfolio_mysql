from django.test import TestCase
import pandas as pd
import numpy as np

df_presente_simple = pd.read_csv('script/csv/presente.csv')
df_passato_prossimo = pd.read_csv('script/csv/passato_prossimo.csv')
df_futuro_semplice = pd.read_csv('script/csv/futuro_semplice.csv')


def presente(verbo):
    persona = df_presente_simple['Unnamed: 0']
    cant_personas = list(range(len(persona)+1))
    conjugacion = df_presente_simple[f'{verbo}']

    return {'range':cant_personas,'persona':persona,'conjugacion':conjugacion}

print(df_futuro_semplice)
#for verbos in range(1,len(df_passato_prossimo.columns)):
#    for i in range(len(df_passato_prossimo)):
#        aux,verbo_conjugado = df_passato_prossimo[f'{df_passato_prossimo.columns[verbos]}'][i].split(' ')
#        print(f"{df_passato_prossimo.columns[verbos],df_passato_prossimo['Unnamed: 0'][i],aux,verbo_conjugado}")

