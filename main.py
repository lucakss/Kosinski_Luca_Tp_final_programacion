
import random
import pygame
import pygame.mixer as mixer
from graficos.config import *
from graficos.funciones_graficos import *
from paquete.funciones import extraer_matriz_csv, extraer_pistas_matriz_fila, extraer_pistas_matriz_columna, crear_matriz, verificar_victoria, convertir_a_tiempo, guardar_puntaje
rutas = ["corazon", "escarabajo", "auto", "nave"]


pygame.init()
mixer.init()

sonido_gano = pygame.mixer.Sound("sonidos/Aplausos_del_publico.mp3")
sonido_perdio = pygame.mixer.Sound("sonidos/Sad_Trombone.mp3")

ICONO = pygame.image.load("imagenes\icono_mate.png")

pygame.display.set_caption("Nonograma")
pygame.display.set_icon(ICONO)


activo = True

#Pantalla
ventana = pygame.display.set_mode((ANCHO, ALTO))

#Muestra la ventana para pedir el nombre
nombre = pedir_nombre(ventana)

while activo:
    opcion = menu_principal(ventana)
    
    if opcion == "jugar":
        #Cada vez que entra al if arranca una nueva partida
        
        #Fondo juego
        fondo_juego = pygame.image.load("imagenes\paisaje_fondo.jpg")
        fondo_juego = pygame.transform.scale(fondo_juego, (ANCHO, ALTO))
        
        #Musica de fondo
        mixer.music.load("sonidos/Que Hacemos, Que Hacemos.mp3")
        
        mixer.music.set_volume(0.05)
        mixer.music.play(-1)
        
        dibujo = random.choice(rutas)
        matriz = extraer_matriz_csv("archivos/" + dibujo + ".csv")

        cant_celdas = len(matriz)
        tamano_celdas = calcular_tamano_celdas(TAMANO_GRILLA, cant_celdas)
        
        FUENTE = pygame.font.Font(None, tamano_celdas // 2)
        
        pistas_filas = extraer_pistas_matriz_fila(matriz)
        pistas_columnas = extraer_pistas_matriz_columna(matriz)

        matriz_estado = crear_matriz(cant_celdas, cant_celdas, 0)

        colisiones = generar_colisiones(cant_celdas, LARGO_GRILLA, LARGO_GRILLA, tamano_celdas)

        tiempo_inicio = pygame.time.get_ticks()
        guardado = False
        
        game_over = False
        vidas = 3
        whitelist = set()
        incorrectas = set()
        pendientes = {}
        
        jugando = True
        while jugando:
            tiempo_actual = pygame.time.get_ticks()
            
            for evento in pygame.event.get():
                
                if evento.type == pygame.QUIT:
                    activo = False
                    jugando = False
                    
                if game_over:
                    continue

                #Entra al if solo cuando el usuario da click
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    cordenadas = encontrar_cordenadas_celda(cant_celdas, colisiones)
                    
                    #Si no se marca ninguna celda continua
                    if not cordenadas:
                        continue
                    
                    fila, columna = encontrar_posicion_matriz(cant_celdas, colisiones,
                                                              cordenadas)
                    posicion = fila, columna
                    
                    #Click izquierdo Alternar cuadrado negro
                    if evento.button == 1:
                        
                        #Verifica que la celda no este en la whitelist
                        if (fila, columna) in whitelist:
                            continue
                        
                        #Verifica que la celda no este en incorrectas
                        if (fila, columna) in incorrectas:
                            continue
                        
                        #Verifica que si hay una X no se pueda pintar encima
                        if matriz_estado[fila][columna] == 2:
                            continue
                        
                        if matriz_estado[fila][columna] == 1:
                            matriz_estado[fila][columna] = 0
                            pendientes.pop((fila, columna), None) #Saco la celda de pendientes
                        else:
                            matriz_estado[fila][columna] = 1
                            #Guardamos el tiempo exacto en el que el usuario pinto la celda
                            pendientes[(fila, columna)] = pygame.time.get_ticks()
                            
                    #Click derecho Alternar X
                    elif evento.button == 3:
                        
                        #Verifica que la celda no este en la whitelist
                        if (fila, columna) in whitelist:
                            continue
                        
                        if matriz_estado[fila][columna] == 2:
                            matriz_estado[fila][columna] = 0
                            
                        elif matriz_estado[fila][columna] != 1: #Verifica que no este pintado
                            matriz_estado[fila][columna] = 2
                
                #El primer elemento es la key el segundo el value
                for (fila, columna), tiempo_se_pinto in list(pendientes.items()):
                    if tiempo_actual - tiempo_se_pinto >= DELAY:

                        #Si la celda sigue pintada (el usuario no la desmarcó)
                        if matriz_estado[fila][columna] == 1:

                            if matriz[fila][columna] == 1:
                                #Si es correcta se vuelve permanente
                                whitelist.add((fila, columna))

                            else:
                                #Si es incorrecta se borra y pone una X permanente
                                matriz_estado[fila][columna] = 2
                                incorrectas.add((fila, columna))
                                whitelist.add((fila, columna))
                                
                                vidas -= 1
                                if vidas <= 0:
                                    game_over = True

                        #Una vez que termino de evaluarse la celda, se elimina
                        del pendientes[(fila, columna)]
                        
            #Imgagen de fondo
            ventana.blit(fondo_juego, (0,0))
            
            #Dibuja grilla y colisiones
            dibujar_grilla(ventana, colisiones, LARGO_GRILLA, LARGO_GRILLA, TAMANO_GRILLA)
            
            #Dibuja las pistas
            generar_pistas(ventana, FUENTE, tamano_celdas, LARGO_GRILLA,
                        pistas_filas, pistas_columnas)
            
            #Actualiza lo pintado
            actualizar_pintado(ventana, cant_celdas, colisiones,
                                matriz_estado, tamano_celdas, incorrectas)

            #Mostrar vidas
            texto_vidas = FUENTE.render(f"Vidas: {vidas}", True, BLANCO)
            ventana.blit(texto_vidas, (50, 20))
                
            #Verificar estado de partida
            if game_over:
                mixer.music.stop()
                sonido_perdio.set_volume(0.05)
                sonido_perdio.play()
                mostrar_pantalla_final(ventana, ANCHO, ALTO, FUENTE, False)
                jugando = False
                
            elif verificar_victoria(matriz, matriz_estado, whitelist):
                
                if not guardado:
                    milisegundos = pygame.time.get_ticks() - tiempo_inicio
                    segundos = milisegundos // 1000
                    
                    guardar_puntaje(nombre, dibujo, segundos)
                    guardado = True
                
                mixer.music.stop()
                sonido_gano.set_volume(0.05)
                sonido_gano.play()
                mostrar_pantalla_final(ventana, ANCHO, ALTO, FUENTE, True)
                jugando = False
            
            pygame.display.update()
        
pygame.quit()
