import pygame

def pedir_nombre(pantalla):
    pygame.font.init()
    ANCHO, ALTO = pantalla.get_width(), pantalla.get_height()

    fuente_titulo = pygame.font.Font(None, 50)
    fuente_input = pygame.font.Font(None, 40)

    #Colores
    COLOR_FONDO = (255, 255, 255)
    COLOR_BORDE_INACTIVO = (0, 0, 0)
    COLOR_BORDE_ACTIVO = (150, 150, 150)
    COLOR_CAJA_FONDO = (255, 255, 255)
    COLOR_TEXTO = (0, 0, 0)

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
                exit()

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

        pantalla.fill(COLOR_FONDO)

        #Titulo centrado
        texto_titulo = fuente_titulo.render("Ingrese su nombre", True, COLOR_TEXTO)
        pantalla.blit(texto_titulo, ((ANCHO - texto_titulo.get_width()) // 2, 150))

        #Caja (formulario)
        pygame.draw.rect(pantalla, COLOR_CAJA_FONDO, input_box)

        color_borde = COLOR_BORDE_ACTIVO if activo else COLOR_BORDE_INACTIVO
        pygame.draw.rect(pantalla, color_borde, input_box, 3)

        #Texto del usuario
        texto_usuario = fuente_input.render(nombre, True, COLOR_TEXTO)
        pantalla.blit(texto_usuario,(input_box.x + 10, input_box.y + (caja_alto - texto_usuario.get_height()) // 2))

        pygame.display.flip()
        #Fps
        clock.tick(60)
        
VENTANA = pygame.display.set_mode((600, 800))

nombre = pedir_nombre(VENTANA)
print(nombre)