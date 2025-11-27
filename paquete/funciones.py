import csv




def extraer_matriz_csv(ruta_archivo: str) -> tuple:
    '''
    Convierte el archivo csv a una matriz.

    Parámetros: ruta_archivo (str): Ruta del archivo CSV a leer.
    
    Retorno: La matriz con el contenido del archivo.
    '''
    with open(ruta_archivo) as archivo:
        matriz = []

        for linea in archivo:
            linea = linea.rstrip("\n")
            fila = []
            valores = linea.split(",")

            for valor in valores:
                if valor.isdigit():
                    fila.append(int(valor))
                else:
                    fila.append(valor)

            matriz.append(fila)

    return tuple(matriz)

def extraer_columnas(matriz: tuple) -> list:
    '''
    Extrae todas las columnas de una matriz.
    
    Parámetros: matriz (tuple): Matriz representada como una tupla de listas.
    
    Retorno: Lista donde cada elemento es una lista que representa una columna.
    '''
    columnas = []
    
    for j in range(len(matriz[0])):
        columna = []
        for i in range(len(matriz)):
            columna.append(matriz[i][j])
        columnas.append(columna)
    return columnas

def extraer_pistas(lista: list) -> list:
    '''
    Extrae de una lista las pistas.
    
    Parámetros: lista (list): Lista compuesta por 0 y 1.
    
    Retorno: Lista con la cantidad de 1s consecutivos encontrados.
    '''
    pistas = []
    contador = 0
    
    for valor in lista:
        if valor == 1:
            contador += 1
        elif contador > 0:
            pistas.append(contador)
            contador = 0
    
    if contador > 0:
        pistas.append(contador)
        
    return pistas

def extraer_pistas_matriz_fila(matriz: tuple) -> tuple:
    '''
    Extrae de cada fila de la matriz las pistas.
    
    Parámetros: matriz (tuple): Matriz representada como una tupla de listas.
    
    Retorno: Tupla donde cada elemento es una tupla con las pistas de una fila.
    '''
    lista_de_pistas = []
    
    for fila in matriz:
        pistas_fila = extraer_pistas(fila)
        lista_de_pistas.append(tuple(pistas_fila))
    return tuple(lista_de_pistas)

def extraer_pistas_matriz_columna(matriz: tuple) -> tuple:
    '''
    Extrae de cada columna de la matriz las pistas.
    
    Parámetros: matriz (tuple): Matriz representada como una tupla de listas.
    
    Retorno: Tupla donde cada elemento es una tupla con las pistas de una columna.
    '''
    lista_de_pistas = []
    columnas = extraer_columnas(matriz)
    
    for columna in columnas:
        pistas_columna = extraer_pistas(columna)
        lista_de_pistas.append(tuple(pistas_columna))
    return tuple(lista_de_pistas)

def crear_matriz(filas: int, columnas: int, valor = False) -> list:
    '''
    Crea una matriz de las dimensiones indicadas.

    Retorno: la matriz creada.
    '''

    matriz= []
    for _ in range(filas):
        fila_creada = [valor] * columnas
        matriz += [fila_creada]

    return matriz

def generar_matriz_usuario(matriz: list) -> list:
    '''
    Genera una matriz del mismo tamaño que matriz, esta sera la que se modifique
    segun lo que haga el usuario

    Retorno: matriz_usuario -> matriz con todos ceros.
    '''
    columnas = len(matriz[0])
    matriz_usuario = []
    
    for _ in range(len(matriz)):
        matriz_usuario.append([0] * columnas)
        
    return matriz_usuario

def guardar_puntaje(nombre: str, dibujo: str, tiempo: str) -> None:
    '''
    Guarda el nombre y el tiempo del usuario en un archivos .csv llamado ranking
    
    Retorno: None
    '''
    with open("archivos/ranking.csv", "a", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([nombre, dibujo, tiempo])

def convertir_a_tiempo(segundos: int) -> str:
    '''
    Convierte los segundos a el tiempo (minutos:segundos)
    
    Retorno: tiempo_formateado -> segundos formateados a tiempo
    '''
    minutos = segundos // 60

    resto_segundos = segundos % 60

    #Se asegura que los segundos tengan dos digitos
    if resto_segundos < 10:
        resto_segundos = "0" + str(resto_segundos)
    else:
        resto_segundos = str(resto_segundos)

    #Se encargar de unir los minutos con los segundos
    tiempo_formateado = str(minutos) + ":" + resto_segundos

    return tiempo_formateado

def verificar_victoria(matriz: tuple, matriz_estado: list, whitelist: set) -> bool:
    '''
    Verifica cuado el usuario gana devolviendo un booleano
    
    Retorno: True -> Si gano | False -> Todavia no gano
    '''
    filas = len(matriz)
    columnas = len(matriz[0])

    for i in range(filas):
        for j in range(columnas):
            
            #Si en la solución va pintado, pero no está en whitelist todavia no gano
            if matriz[i][j] == 1 and (i, j) not in whitelist:
                return False

            #Si en la solución no va pintado, pero el usuario la pinto todavia no gano
            if matriz[i][j] == 0 and matriz_estado[i][j] == 1:
                return False

    return True


# fila = extraer_pistas([0,1,1,0,0,1,1,0])
# print(fila)
        
# matriz = extraer_matriz_csv("archivos/corazon.csv")

# matriz_usuario = generar_matriz_usuario(matriz)


# pistas_filas = extraer_pistas_matriz_fila(matriz)
# print(pistas_filas)

# pistas_columnas = extraer_pistas_matriz_columna(matriz)
# print(pistas_columnas)

# 0,1,1,0,0,0,1,1,0,0
# 1,1,1,1,0,1,1,1,1,0
# 1,1,1,1,1,1,1,1,1,0
# 1,1,1,1,1,1,1,1,1,1
# 0,1,1,1,1,1,1,1,1,0
# 0,0,1,1,1,1,1,1,0,0
# 0,0,0,1,1,1,1,0,0,0
# 0,0,0,0,1,1,0,0,0,0
# 0,0,0,0,0,1,0,0,0,0
# 0,0,0,0,0,1,0,0,0,0