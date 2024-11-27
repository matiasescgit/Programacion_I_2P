# Importacion de bibliotecas
from Biblioteca_Proyecto import *

# Inicializacion Pygame y mixer
pygame.init()
pygame.mixer.init()

# Constantes y variables
TITULO = "Batalla Naval"
ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720

corriendo = True
filas = 10
columnas = 10
mar = 0

color_boton = (0,100,0)

dificultad = 1
puntaje = 0

claves_barcos = ["coordenadas", "destruidos"]
submarinos = 4
destructores = 3
cruceros = 2
acorazados = 1

# Musica y Sonidos
pygame.mixer.music.load("sonidos\Waterworld - Map.mp3")
pygame.mixer.music.set_volume(0.1)

pygame.mixer.music.play(loops=-1)

# Imagenes
icono = pygame.image.load("imagenes/destructor.png")
fondo = pygame.image.load("imagenes/fondo_menu.jpg")
fondo_modificado = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Pantalla y Ventana
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))         # Decidir si hacer reajustable
pygame.display.set_caption(TITULO)
pygame.display.set_icon(icono)

# Eventos Propios:
tiempo_transcurrido = pygame.USEREVENT + 1
un_segundo = 1000  # 1000 Milisegundos = 1 segundo
pygame.time.set_timer(tiempo_transcurrido, un_segundo)

contador_tiempo = 0
contador_minutos = 0
segundos = 0
minutos = entero_zfill(contador_minutos, 2)
segundos = entero_zfill(contador_tiempo, 2)

# TEXTO
fuente = pygame.font.SysFont("Arial", 30, bold=True)
texto_tiempo = fuente.render(f"Tiempo: {minutos}", True, "black")
tamaño_texto_tiempo = texto_tiempo.get_rect().width
puntaje_str = entero_zfill(puntaje, 4)
texto_puntaje = fuente.render(f"puntaje: {puntaje_str}", True, "black")
tamaño_texto_puntaje = texto_puntaje.get_rect().width

texto_records = fuente.render("MEJORES JUGADORES", True, "black")
rect_texto_records_centralizado = texto_records.get_rect(center=(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 6))
texto_nuevo_record = fuente.render("¡NUEVO RECORD!", True, "black")
texto_fin_juego = fuente.render("FIN DEL JUEGO", True, "black")
texto_ingresar_nick = fuente.render("Ingrese su nombre:", True, "black")

nombre_ingresado = ""

boton_nivel = pygame.Rect((ANCHO_PANTALLA / 2) - 75, ALTO_PANTALLA * 20 / 100, 150, 75)
bandera_boton_nivel = False
boton_inicio = pygame.Rect((ANCHO_PANTALLA / 2) - 75, ALTO_PANTALLA * 35 / 100, 150, 75)
bandera_boton_inicio = False
boton_puntaje = pygame.Rect((ANCHO_PANTALLA / 2) - 75, ALTO_PANTALLA * 50 / 100, 150, 75)
bandera_boton_puntaje = False
boton_salir = pygame.Rect((ANCHO_PANTALLA / 2) - 75, ALTO_PANTALLA * 65 / 100, 150, 75)
boton_atras = pygame.Rect((ANCHO_PANTALLA * 85 / 100) - 75, ALTO_PANTALLA * 20 / 100, 150, 75)
boton_reiniciar = pygame.Rect((ANCHO_PANTALLA * 85 / 100) - 75, ALTO_PANTALLA * 40 / 100, 150, 75)

# bandera_estado = False
bandera_ingresar_record = False

rect_tablero = pygame.Rect(ANCHO_PANTALLA * 20 / 100, ALTO_PANTALLA * 5 / 100, 663, 663)
rect_ventana_nick = pygame.Rect(ANCHO_PANTALLA * 50 / 100 - 650 / 2, ALTO_PANTALLA * 50 / 100 - 500 / 2, 650, 500)
#                                   BOTONES DIFICULTAD
boton_facil = pygame.Rect((ANCHO_PANTALLA / 2) - 75, ALTO_PANTALLA * 20 / 100, 150, 75)
boton_normal = pygame.Rect((ANCHO_PANTALLA / 2) - 75, ALTO_PANTALLA * 35 / 100, 150, 75)
boton_dificil = pygame.Rect((ANCHO_PANTALLA / 2) - 75, ALTO_PANTALLA * 50 / 100, 150, 75)
boton_volver_dificultad = pygame.Rect((ANCHO_PANTALLA / 2) - 75, ALTO_PANTALLA * 65 / 100, 150, 75)
#                                   TEXTO BOTONES MENU
texto_boton_dificultad = fuente.render("Niveles", True, "black")
texto_boton_jugar = fuente.render("Jugar", True, "black")
texto_boton_puntaje = fuente.render("Puntaje", True, "black")
texto_boton_salir = fuente.render("Salir", True, "black")
#                                   TEXTO BOTONES DIFICULTAD
texto_boton_facil=fuente.render("Facil", True, "black")
texto_boton_normal=fuente.render("Normal", True, "black")
texto_boton_dificil=fuente.render("Dificil", True, "black")
texto_boton_volver_dificultad=fuente.render("Volver", True, "black")
#                                   TEXTO BOTONES JUEGO
texto_boton_reiniciar=fuente.render("Reiniciar", True, "black")
texto_boton_volver_juego=fuente.render("Volver", True, "black")
#                                   TEXTO BOTONES PUNTAJES
texto_boton_volver_puntajes=fuente.render("Volver", True, "black")

try:
    records = cargar_record_json("archivo_puntajes.json")
    ordenar_records(records)
except:
    records = []
    guardar_record_json("archivo_puntajes.json", records)

while corriendo:
    #                                           EVENTOS
    if bandera_boton_inicio == False and bandera_boton_puntaje == False and bandera_boton_nivel == False and bandera_ingresar_record == False:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                coordenadas_click = pygame.mouse.get_pos()
                if boton_inicio.collidepoint(coordenadas_click) == True:
                    matriz_valor = obtener_matriz(filas * dificultad, columnas * dificultad, mar)
                    dicc_barcos = rellenar_tablero(matriz_valor, submarinos * dificultad, destructores * dificultad, cruceros * dificultad, acorazados * dificultad)
                    mostrar_matriz(matriz_valor)
                    print(dicc_barcos)
                    matriz_rect = obtener_matriz_rectangulo(matriz_valor, ANCHO_PANTALLA, ALTO_PANTALLA, rect_tablero)
                    bandera_boton_inicio = True
                    puntaje = 0
                    puntaje_str = entero_zfill(puntaje, 4)
                    texto_puntaje = fuente.render(f"Puntaje: {puntaje_str}", True, "black")
                    contador_tiempo = 0
                    contador_minutos = 0
                    texto_tiempo = fuente.render(f"Tiempo: {minutos}:{segundos}", True, "black")
                if boton_puntaje.collidepoint(coordenadas_click) == True:
                    bandera_boton_puntaje = True
                if boton_nivel.collidepoint(coordenadas_click) == True:
                    bandera_boton_nivel = True
                if boton_salir.collidepoint(coordenadas_click) == True:
                    corriendo = False

    if bandera_boton_inicio == True and bandera_ingresar_record == False: #Eventos en la pantalla juego
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == tiempo_transcurrido: # Paso 1 segundo
                contador_tiempo += 1
                if contador_tiempo > 59:
                    contador_tiempo = 0
                    contador_minutos += 1
                segundos = entero_zfill(contador_tiempo, 2)
                minutos = entero_zfill(contador_minutos, 2)
                texto_tiempo = fuente.render(f"Tiempo: {minutos}:{segundos}", True, "black")
            if evento.type == pygame.MOUSEBUTTONDOWN:
                coordenadas_click = pygame.mouse.get_pos()
                print(coordenadas_click)
                for y in range(len(matriz_rect)):
                    for x in range(len(matriz_rect[y])):
                        if matriz_rect[y][x].collidepoint(coordenadas_click) == True:
                            puntaje += impacto_naval(matriz_valor, y, x, dicc_barcos)
                            puntaje_str = entero_zfill(puntaje, 4)
                            texto_puntaje = fuente.render(f"Puntaje: {puntaje_str}", True, "black")
                            mostrar_matriz(matriz_valor)
                            bandera_ingresar_record = estado_juego(matriz_valor)
                if boton_atras.collidepoint(coordenadas_click) == True:
                    bandera_boton_inicio = False
                    contador_tiempo = 0
                if boton_reiniciar.collidepoint(coordenadas_click) == True:
                    matriz_valor = obtener_matriz(filas * dificultad, columnas * dificultad, mar)
                    dicc_barcos = rellenar_tablero(matriz_valor, submarinos * dificultad, destructores * dificultad, cruceros * dificultad, acorazados * dificultad)
                    matriz_rect = obtener_matriz_rectangulo(matriz_valor, ANCHO_PANTALLA, ALTO_PANTALLA, rect_tablero)
                    contador_tiempo = 0
                    contador_minutos = 0
                    texto_tiempo = fuente.render(f"Tiempo: {minutos}:{segundos}", True, "black")
                    texto_tiempo = fuente.render(f"Tiempo: {minutos}:{segundos}", True, "black")
                    puntaje = 0
                    puntaje_str = entero_zfill(puntaje, 4)
                    texto_puntaje = fuente.render(f"Puntaje: {puntaje_str}", True, "black")

    if bandera_ingresar_record == True: # Eventos en la pantalla ingresar record
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if len(records) < 3 or puntaje >= records[-1]["Puntaje"]:
                        guardar_record_lista(records, ["Nick", "Puntaje"], [nombre_ingresado, puntaje])
                        ordenar_records(records)
                        if len(records) > 3:
                            records.pop()
                        guardar_record_json("archivo_puntajes.json", records)
                    nombre_ingresado = ""
                    bandera_ingresar_record = False
                    bandera_boton_inicio = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_ingresado = nombre_ingresado[:-1]
                elif len(nombre_ingresado) < 10:
                    nombre_ingresado += evento.unicode

    if bandera_boton_puntaje == True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                coordenadas_click = pygame.mouse.get_pos()
                if boton_atras.collidepoint(coordenadas_click) == True:
                    bandera_boton_puntaje = False

    if bandera_boton_nivel == True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                coordenadas_click = pygame.mouse.get_pos()
                if boton_facil.collidepoint(coordenadas_click) == True:
                    dificultad = 1
                    bandera_boton_nivel = False
                if boton_normal.collidepoint(coordenadas_click) == True:
                    dificultad = 2
                    bandera_boton_nivel = False
                if boton_dificil.collidepoint(coordenadas_click) == True:
                    dificultad = 4
                    bandera_boton_nivel = False
                if boton_volver_dificultad.collidepoint(coordenadas_click)==True:
                    bandera_boton_nivel = False
    #                                           PANTALLAS
    if bandera_boton_inicio == False and bandera_boton_puntaje == False and bandera_boton_nivel == False and bandera_ingresar_record == False:
        pantalla.blit(fondo_modificado, (0, 0))
        # BOTONES
        pygame.draw.rect(pantalla, color_boton, boton_nivel,border_radius=20)
        pygame.draw.rect(pantalla, color_boton, boton_inicio,border_radius=20)
        pygame.draw.rect(pantalla, color_boton, boton_puntaje,border_radius=20)
        pygame.draw.rect(pantalla, color_boton, boton_salir,border_radius=20)
        # TEXTOS
        pantalla.blit(texto_boton_dificultad,((ANCHO_PANTALLA / 2) - 75+35, ALTO_PANTALLA * 20 / 100 +20))
        pantalla.blit(texto_boton_jugar,((ANCHO_PANTALLA / 2) - 75+35, ALTO_PANTALLA * 35 / 100+20))
        pantalla.blit(texto_boton_puntaje,((ANCHO_PANTALLA / 2) - 75+35, ALTO_PANTALLA * 50 / 100+20))
        pantalla.blit(texto_boton_salir,((ANCHO_PANTALLA / 2) - 75+35, ALTO_PANTALLA * 65 / 100+20))
    
    if bandera_boton_inicio == True:
        # PANTALLA JUEGO
        pantalla.blit(fondo_modificado, (0, 0))
        # BOTONES
        pygame.draw.rect(pantalla, color_boton, boton_atras,border_radius=20)
        pygame.draw.rect(pantalla, color_boton, boton_reiniciar,border_radius=20)
        # TEXTOS
        pantalla.blit(texto_tiempo, (ALTO_PANTALLA * 50 / 100, ALTO_PANTALLA / 100 - 6))
        pantalla.blit(texto_puntaje, (ALTO_PANTALLA * 90 / 100, ALTO_PANTALLA / 100 - 6))
        pantalla.blit(texto_boton_reiniciar,((ANCHO_PANTALLA * 85 / 100) - 75+20, ALTO_PANTALLA * 40 / 100+20))
        pantalla.blit(texto_boton_volver_juego,((ANCHO_PANTALLA * 85 / 100) - 75+35, ALTO_PANTALLA * 20 / 100+20))
        # TABLERO
        dibujar_tablero(matriz_valor, matriz_rect, dicc_barcos, pantalla, rect_tablero)

    if bandera_ingresar_record == True:
        # PANTALLA INGRESAR NOMBRE
        pygame.draw.rect(pantalla, (255, 255, 255), rect_ventana_nick)
        pygame.draw.rect(pantalla, (0, 0, 0), rect_ventana_nick, width=4)
        # MENSAJE
        if len(records) == 0 or puntaje > records[-1]["Puntaje"]:
            pantalla.blit(texto_nuevo_record, (ANCHO_PANTALLA / 2 - texto_nuevo_record.get_width() / 2, ALTO_PANTALLA / 2 - 500 / 3))
        else:
            pantalla.blit(texto_fin_juego, (ANCHO_PANTALLA / 2 - texto_fin_juego.get_width() / 2, ALTO_PANTALLA / 2 - 500 / 3))            
        pantalla.blit(texto_ingresar_nick, (ANCHO_PANTALLA / 2 - texto_ingresar_nick.get_width() / 2, ALTO_PANTALLA / 2 - 500 / 4))
        # CASILLA INGRESAR NOMBRE
        texto_nombre = fuente.render(nombre_ingresado, True, (50, 50, 200))
        pantalla.blit(texto_nombre, (ANCHO_PANTALLA / 2 - texto_nombre.get_width() / 2, ALTO_PANTALLA / 2 - texto_nombre.get_height() / 2))

    if bandera_boton_puntaje == True:
        # PANTALLA DE PUNTAJES
        pantalla.blit(fondo_modificado, (0, 0))
        pygame.draw.rect(pantalla, "gray", (ANCHO_PANTALLA / 6 - 100, ALTO_PANTALLA / 6 - 75, ANCHO_PANTALLA / 2, ALTO_PANTALLA * 4 / 6 + 75))
        pygame.draw.rect(pantalla, "black", (ANCHO_PANTALLA / 6 - 100, ALTO_PANTALLA / 6 - 75, ANCHO_PANTALLA / 2, ALTO_PANTALLA * 4 / 6 + 75), width=4) 
        # BOTON
        pygame.draw.rect(pantalla, color_boton, boton_atras,border_radius=20)
        # TEXTOS
        pantalla.blit(texto_boton_volver_puntajes,((ANCHO_PANTALLA * 85 / 100) - 75+35, ALTO_PANTALLA * 20 / 100+10))
        pantalla.blit(texto_records, (ANCHO_PANTALLA / 2.9 - texto_records.get_width() / 2, ALTO_PANTALLA / 6 - texto_records.get_height() / 2))
        mostrar_records(records, "Puntaje", fuente, "black", pantalla, [ANCHO_PANTALLA / 6, ALTO_PANTALLA / 4], ANCHO_PANTALLA / 3, ALTO_PANTALLA / 5)

    if bandera_boton_nivel == True:
        # PANTALLA DIFICULTAD
        pantalla.blit(fondo_modificado,(0,0))
        # BOTONES
        pygame.draw.rect(pantalla, color_boton,boton_facil,border_radius=20)
        pygame.draw.rect(pantalla, color_boton,boton_normal,border_radius=20)
        pygame.draw.rect(pantalla, color_boton,boton_dificil,border_radius=20)
        pygame.draw.rect(pantalla, color_boton,boton_volver_dificultad,border_radius=20)
        # TEXTOS
        pantalla.blit(texto_boton_facil,((ANCHO_PANTALLA / 2) - 75+35, ALTO_PANTALLA * 20 / 100 +20))
        pantalla.blit(texto_boton_normal,((ANCHO_PANTALLA / 2) - 75+35, ALTO_PANTALLA * 35 / 100+20))
        pantalla.blit(texto_boton_dificil,((ANCHO_PANTALLA / 2) - 75+35, ALTO_PANTALLA * 50 / 100+20))
        pantalla.blit(texto_boton_volver_dificultad,((ANCHO_PANTALLA / 2) - 75+35, ALTO_PANTALLA * 65 / 100+20))
    pygame.display.flip()

pygame.quit()
print("Juego cerrado")