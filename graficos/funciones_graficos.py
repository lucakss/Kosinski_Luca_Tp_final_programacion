import pygame
import csv

from graficos.config import *
from paquete.funciones import convertir_a_tiempo

def calcular_tamano_celdas(tamano_grilla: int, cant_celdas: int) -> float:
    '''
    Calcula el tamaño de cada celda dividiendo el tamaño total de la grilla
    por la cantidad de celdas.

    Retorno: el tamaño de cada celda -> tamano_celdas
    '''
    tamano_celdas = tamano_grilla // cant_celdas
    
    return tamano_celdas

def generar_colisiones(cant_celdas: int, x_inicial: int,
                       y_inicial: int, tamano_celdas: int) -> list:
    '''
    Genera una matriz de rectángulos que representan
    las colisiones de cada celda del nonograma.

    Retorno: matriz de colisión -> matriz_colisiones.
    '''
    matriz_colisiones = []

    for fila in range(cant_celdas):
        fila_col = []
        for columna in range(cant_celdas):
            #Calcula la posicion de la celda
            x = x_inicial + 1 + columna * tamano_celdas
            y = y_inicial + 1 + fila * tamano_celdas
            
            #Se le resta 1 para achicar el rectangulo y aprovechar el fondo
            rect = pygame.Rect(x, y, tamano_celdas - 1, tamano_celdas - 1)
            fila_col.append(rect)
            
        matriz_colisiones.append(fila_col)

    return matriz_colisiones

def dibujar_grilla(ventana: object, colisiones: tuple, x_inicial: int,
                   y_inicial: int, tamano_grilla: int) -> None:
    '''
    Se encarga de dibujar la grilla completa, primero un cuadrado Negro de fondo y
    despues cada celda en blanco en base al tamaño de cada colision 
    
    Retorno: None
    '''
    pygame.draw.rect(ventana, NEGRO, (x_inicial, y_inicial, tamano_grilla, tamano_grilla))

    for fila in colisiones:
        for rect in fila:
            pygame.draw.rect(ventana, BLANCO, rect)

def generar_pistas(ventana: object, fuente: object, tamano_celdas: int,
                   largo_grilla: int, pistas_filas: tuple, pistas_columnas: tuple) -> None:
    '''
    Se encarga de dibujar las pistas del nonogra, primero las de las filas de derecha a izquierda y
    despues la de las columnas de abajo hacia arriba

    Retorno: None
    '''
    #Generar pistas filas
    #fila inicial
    y = largo_grilla + 20
    
    for pistas in pistas_filas:
        x = largo_grilla - 30
        indice = -1
        
        #Recorre las pistas al reves
        for _ in range(len(pistas)):
            texto = fuente.render(str(pistas[indice]), True, NEGRO)
            ventana.blit(texto, (x, y))
            indice -= 1
            #Espacio entre numeros
            x -= 40
            
        #Salta a la siguiente fila
        y += tamano_celdas
    
    #Generar pistas columnas
    #Columna inicial
    x = largo_grilla + 20
    
    for pistas in pistas_columnas:
        y = largo_grilla - 30
        indice = -1
        
        #Recorre las pistas al reves
        for _ in range(len(pistas)):
            texto = fuente.render(str(pistas[indice]), True, NEGRO)
            ventana.blit(texto, (x, y))
            indice -= 1
            #Espacio entre numeros
            y -= 40

        #Salta a la siguiente Columna
        x += tamano_celdas
 
def encontrar_cordenadas_celda(cant_celdas: int, colisiones: list) -> tuple|None:
    '''
    Devuelve las coordenadas de la celda donde el usuario hizo click.
    
    Retorno: posición de la esquina superior izquierda de la colision que clickeo (x, y) -> tuple.
    
             None si el click no cayó en ninguna colision.
    '''
    
    #Obtiene la posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #Recorre las colisiones hasta encontrar donde hizo click
    for i in range(cant_celdas):
        for j in range(cant_celdas):
            #Entra al if si el click del usuario esta dentro del perimetro de las colisiones
            if colisiones[i][j].collidepoint(mouse_x, mouse_y):
                x, y = colisiones[i][j].topleft
                return x, y

def encontrar_posicion_matriz(cant_celdas: int, colisiones: list, cordenadas: tuple) -> list:
    '''
    Encuentra los indices de la matriz_colisiones de las coordenadas (x, y)

    Retorno: Indices de las coordenadas -> [i, j]
    '''
    for i in range(cant_celdas):
        for j in range(cant_celdas):
            #Entra al if si las coordenadas estan dentro del perimetro de las colisiones
            if colisiones[i][j].collidepoint(cordenadas):
                return [i, j]

def actualizar_pintado(ventana: object, cant_celdas: int, colisiones: tuple,
                       matriz_estado: list, tamano_celdas: int, incorrectas: set) -> None:
    
    for fila in range(cant_celdas):
        for columna in range(cant_celdas):
            x, y = colisiones[fila][columna].topleft
            actual = matriz_estado[fila][columna]
                        
            match actual:
                            
                case 0:
                    pygame.draw.rect(ventana, BLANCO, (x, y, tamano_celdas -1, tamano_celdas -1))
                                
                case 1:
                    pygame.draw.rect(ventana, CELESTE, (x, y, tamano_celdas -1, tamano_celdas -1))
                            
                case 2:
                    if (fila, columna) in incorrectas:
                        pygame.draw.line(ventana, ROJO, (x,y), (x+tamano_celdas, y+tamano_celdas), 3)
                        pygame.draw.line(ventana, ROJO, (x+tamano_celdas,y), (x, y+tamano_celdas), 3)
                    else:
                        pygame.draw.line(ventana, NEGRO, (x,y), (x+tamano_celdas, y+tamano_celdas), 3)
                        pygame.draw.line(ventana, NEGRO, (x+tamano_celdas,y), (x, y+tamano_celdas), 3)
                                    
def pedir_nombre(ventana: object) -> str:
    '''
    Muestra una pantalla donde el usuario puede ingresar su nombre con el teclado.

    - Aparece una caja de texto en el centro
    - El usuario escribe y puede borrar
    - Al presionar Enter se confirma el ingreso

    Retorno: El nombre ingresado por el jugador -> nombre
    '''
    pygame.font.init()
    ANCHO, ALTO = ventana.get_width(), ventana.get_height()

    fuente_titulo = pygame.font.Font(None, 50)
    fuente_input = pygame.font.Font(None, 40)

    #Caja centrada
    caja_ancho = 350
    caja_alto = 50
    input_box = pygame.Rect((ANCHO - caja_ancho) // 2, (ALTO // 2) - 25, caja_ancho, caja_alto)

    activo = False
    nombre = ""

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    activo = True
                else:
                    activo = False

            if event.type == pygame.KEYDOWN and activo:
                if event.key == pygame.K_RETURN:
                    return nombre
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 20:
                        nombre += event.unicode

        ventana.fill(BLANCO)

        #Titulo centrado
        texto_titulo = fuente_titulo.render("Ingrese su nombre", True, NEGRO)
        ventana.blit(texto_titulo, ((ANCHO - texto_titulo.get_width()) // 2, 150))

        #Caja (formulario)
        pygame.draw.rect(ventana, BLANCO, input_box)

        color_borde = GRIS if activo else NEGRO
        pygame.draw.rect(ventana, color_borde, input_box, 3)

        #Texto del usuario
        texto_usuario = fuente_input.render(nombre, True, NEGRO)
        ventana.blit(texto_usuario,(input_box.x + 10, input_box.y + (caja_alto - texto_usuario.get_height()) // 2))

        pygame.display.flip()
        #Fps
        clock.tick(60)

def menu_principal(ventana: object) -> None:
    '''
    Muestra el menú principal del juego con tres botones:
        - JUGAR → devuelve "jugar"
        - RANKING → abre la tabla de puntajes
        - SALIR → cierra el programa

    Retorno:
        si se presiona JUGAR -> "jugar"
        si se entra al ranking -> mostrar_ranking(ventana)
        si se presiona SALIR -> pygame.quit()
    '''
    
    fuente_titulo = pygame.font.Font(None, 80)
    fuente_btn = pygame.font.Font(None, 60)

    clock = pygame.time.Clock()

    #Botones
    btn_jugar = pygame.Rect(0, 0, 300, 80)
    btn_ranking = pygame.Rect(0, 0, 300, 80)
    btn_salir = pygame.Rect(0, 0, 300, 80)

    btn_jugar.center = (ANCHO // 2, ALTO // 2 - 120)
    btn_ranking.center = (ANCHO // 2, ALTO // 2)
    btn_salir.center = (ANCHO // 2, ALTO // 2 + 120)

    activo = True

    while activo:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_jugar.collidepoint(evento.pos):
                    return "jugar"

                if btn_ranking.collidepoint(evento.pos):
                    return mostrar_ranking(ventana)
                
                if btn_salir.collidepoint(evento.pos):
                    return pygame.quit()

        #Fondo
        ventana.fill(BLANCO)

        #Titulo
        titulo = fuente_titulo.render("MENÚ PRINCIPAL", True, NEGRO)
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 120)
        )

        #Boton jugar
        pygame.draw.rect(ventana, NEGRO, btn_jugar, 3)
        txt_jugar = fuente_btn.render("JUGAR", True, NEGRO)
        ventana.blit(txt_jugar, (btn_jugar.centerx - txt_jugar.get_width() // 2,
                                 btn_jugar.centery - txt_jugar.get_height() // 2))

        #Boton ranking
        pygame.draw.rect(ventana, NEGRO, btn_ranking, 3)
        txt_rank = fuente_btn.render("RANKING", True, NEGRO)
        ventana.blit(txt_rank, (btn_ranking.centerx - txt_rank.get_width() // 2,
                                btn_ranking.centery - txt_rank.get_height() // 2))

        #Boton salir
        pygame.draw.rect(ventana, NEGRO, btn_salir, 3)
        txt_salir = fuente_btn.render("SALIR", True, NEGRO)
        ventana.blit(txt_salir, (btn_salir.centerx - txt_salir.get_width() // 2, 
                                 btn_salir.centery - txt_salir.get_height() // 2))
        
        pygame.display.update()
        clock.tick(60)

def mostrar_pantalla_final(ventana: object, ancho: int, alto: int, fuente: object, bandera: True|False) -> bool|None:
    '''
    Muestra la pantalla final cuando el jugador gana o pierde.

    Muestra "GANADOR" si bandera -> True
    Muestra "PERDEDOR" si bandera -> False

    Tiene un botón VOLVER que regresa al menú principal

    Retorno:
        Cuando el jugador pulsa VOLVER → menu_principal(ventana)
        Si se cierra la ventana -> pygame.quit()
    '''
    clock = pygame.time.Clock()

    btn_volver = pygame.Rect(0, 0, 300, 80)
    btn_volver.center = (ancho // 2, alto // 2 + 100)

    if bandera:
        mensaje = "GANADOR"
        color_mensaje = VERDE
    else:
        mensaje = "PERDEDOR"
        color_mensaje = ROJO

    activo = True
    
    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_volver.collidepoint(evento.pos):
                    return menu_principal(ventana)

        #Fondo
        ventana.fill(NEGRO)

        #Texto ganaste
        texto = fuente.render(mensaje, True, color_mensaje)
        ventana.blit(texto, (ancho // 2 - texto.get_width()//2, alto // 2 - 80))

        #Boton volver
        pygame.draw.rect(ventana, BLANCO, btn_volver)
        pygame.draw.rect(ventana, NEGRO, btn_volver, 4)
        txt = fuente.render("VOLVER", True, NEGRO)
        ventana.blit(txt, (btn_volver.centerx - txt.get_width() // 2,
                           btn_volver.centery - txt.get_height() // 2))

        pygame.display.update()
        clock.tick(60)

def mostrar_ranking(ventana: object, ruta_csv: str ="archivos/ranking.csv") -> str:
    '''
    Muestra en pantalla el Ranking de los mejores tiempos registrados en el juego.

    Lee un archivo CSV con registros → (nombre, dibujo resuelto, tiempo en segundos)
    Ordena los puntajes del menor al mayor tiempo
    Muestra únicamente los 10 mejores resultados en una tabla visual
    Permite volver al menú principal mediante un botón

    Retorno:
        Si el jugador presiona VOLVER -> menu_principal(ventana)
        Si se cierra la ventana desde la X -> (pygame.quit)
    '''
    
    pygame.display.set_caption("Ranking")
    clock = pygame.time.Clock()
    
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_tabla = pygame.font.Font(None, 40)
    fuente_boton = pygame.font.Font(None, 45)

    #Leer el csv
    registros = []
    with open(ruta_csv, newline="") as archivo:
        lector = csv.reader(archivo)
        for nombre, dibujo, tiempo in lector:
            registros.append((nombre, dibujo, int(tiempo)))

    #Ordenar por tiempo
    for i in range(len(registros) - 1):
        for j in range(i + 1, len(registros)):
            if registros[j][2] < registros[i][2]:   #Comparamos tiempos
                registros[i], registros[j] = registros[j], registros[i]

    registros = registros[:10] #Solo los 10 primeros

    #Boton para volver
    boton_volver = pygame.Rect(ANCHO // 2 - 100, ALTO - 80, 200, 50)

    activo = True
    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                activo = False
                return pygame.quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return menu_principal(ventana)

        ventana.fill(BLANCO) #Fondo blanco

        #Titulo
        titulo = fuente_titulo.render("RANKING", True, NEGRO)
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 30))

        #Encabezados ranking
        ventana.blit(fuente_tabla.render("Puesto", True, NEGRO), (80, 120))
        ventana.blit(fuente_tabla.render("Nombre", True, NEGRO), (260, 120))
        ventana.blit(fuente_tabla.render("Dibujo", True, NEGRO), (440, 120))
        ventana.blit(fuente_tabla.render("Tiempo", True, NEGRO), (620, 120))

        #Lista el top 10
        y = 165
        puesto = 1
        for nombre, dibujo, tiempo in registros:
            tiempo_formateado = convertir_a_tiempo(tiempo)

            ventana.blit(fuente_tabla.render(str(puesto), True, NEGRO), (100, y))
            ventana.blit(fuente_tabla.render(nombre, True, NEGRO), (260, y))
            ventana.blit(fuente_tabla.render(dibujo, True, NEGRO), (440, y))
            ventana.blit(fuente_tabla.render(tiempo_formateado, True, NEGRO), (620, y))

            puesto += 1
            y += 40  #separacion entre filas

        #Boton volver
        pygame.draw.rect(ventana, NEGRO, boton_volver, 3)
        texto_volver = fuente_boton.render("VOLVER", True, NEGRO)
        ventana.blit(texto_volver, (boton_volver.centerx - texto_volver.get_width() // 2,
                                    boton_volver.centery - texto_volver.get_height() // 2))

        pygame.display.update()
        clock.tick(60)