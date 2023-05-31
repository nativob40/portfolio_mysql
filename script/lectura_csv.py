import pandas as pd
import random
import os

################# ITALIANO #################

df_presente_simple = pd.read_csv("script/csv/presente.csv")
df_passato_prossimo = pd.read_csv("script/csv/passato_prossimo.csv")
df_futuro_semplice = pd.read_csv("script/csv/futuro_semplice.csv")

df_traduccion = pd.read_csv("script/csv/traduccion.csv")
df_traduccion.drop(["Unnamed: 0"], axis="columns", inplace=True)

################# INGLES #################

df_present = pd.read_csv("script/csv/ingles/present.csv")
df_present_continuous = pd.read_csv("script/csv/ingles/present_continuous.csv")
df_preterite = pd.read_csv("script/csv/ingles/preterite.csv")
df_future = pd.read_csv("script/csv/ingles/future.csv")

df_traduccion_ingles = pd.read_csv("script/csv/ingles/traduccion.csv")
df_traduccion_ingles.drop(["Unnamed: 0"], axis="columns", inplace=True)


class Verbo:
    def verbo_aleatorio(df):
        resultado = []
        verbo = df.columns[random.randrange(1, df.shape[1], 1)]
        persona = random.randrange(0, len(df[verbo]) - 1, 1)
        dato = df.loc[persona, ["Unnamed: 0", f"{verbo}"]]
        resultado.append(verbo)
        resultado.append(dato[0])
        resultado.append(dato[1])

        return resultado

    def traduccion(verbo, palabra_en_español, idioma):
        if idioma == "ingles":
            traducir = df_traduccion_ingles[f"{verbo}"]
        else:
            traducir = df_traduccion[f"{verbo}"]

        if palabra_en_español in list(traducir):
            resultado = "Correcto"
        else:
            resultado = "Incorrecto"

        return verbo, list(traducir), resultado


##########################################################################################################################
"""
correctas = 0
incorrectas = 0
listado_incorrectas = []

cantidad_verbos = Verbo.df_presente_simple.shape[1]-1

while(cantidad_verbos != 0):
    os.system('clear')
    print(Verbo.df_presente_simple().shape[1]-1)
    verbo = Verbo.verbo_aleatorio(Verbo.df_presente_simple)[0]
    print(f'Que significa la palabra: {verbo.upper()}')

    palabra = input('\nIngresa la traduccion: ') 
    elementos = Verbo.traduccion(verbo,palabra)


    if elementos[2] == 'Correcto':
        correctas += 1
        print(f'{elementos[2].upper()}!!!!\n')
        print(f'Otros resultados posibles son: {elementos[1]}')

        print(f'\nCorrectas = {correctas}\nIncorrectas = {incorrectas}\n')
        Verbo.df_presente_simple.drop([f'{verbo}'], axis = 'columns', inplace=True)

    else:
        incorrectas += 1
        print(f'{elementos[2].upper()}!!!!\n')
        print(f'Palabras correctas son: {elementos[1]}')

        print(f'\nCorrectas = {correctas}\nIncorrectas = {incorrectas}\n')

        listado_incorrectas.append(verbo)
        
    cantidad_verbos -= 1

    salir = input('Desea Salir? S/N\n')  
    
    if salir == 's':
        print(f'\nPALABRAS INCORRECTAS:')
        for i in set(listado_incorrectas):
            print(f"- {i.upper()}, que significa: {list(Verbo.df_traduccion[str(i)])}")
        break
        
print(f'\nFELICITACIONES!!!')
print('EJERCICIO COMPLETADO\n\nRESULTADO:')
print(f'\n- Correctas = {correctas}\n- Incorrectas = {incorrectas}\n') 
"""
