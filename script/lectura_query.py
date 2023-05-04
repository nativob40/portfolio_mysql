def lectura_query(archivo_sql):
    f = open(archivo_sql, "r")
    cadena=''
    lista=[]

    for i in f:
        linea = i.replace('[','').replace(']','').replace('\n','')
        cadena += linea + ' '

    lista = cadena.split('*/')
    query = lista[1]

    f.close()

    return query