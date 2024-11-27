import pygame, random, json

def mostrar_matriz(matriz:list)->None:
    '''
    Funcion: Muestra los elementos de una matriz.
    Parametros: Recibe por parametro una matriz.
    Retorno: No devuelve ningun dato.
    '''
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=" ")
        print("")

def obtener_matriz(filas:int, columnas:int, mar:int)->list:
    '''
    Funcion: Genera una matriz con filas y columnas y lo rellena con un entero.
    Parametros: 3 enteros, uno representa las filas de la matriz, otro las columnas y por ultimo
    un entero para rellenar la matriz.
    Retorno: Una matriz rellena de el valor entero pasado.
    '''
    matriz = []
    for y in range(filas):
        matriz.append([])
        for x in range(columnas):
            matriz[y].append(mar)
    return matriz

def obtener_matriz_rectangulo(matriz:list, ancho:int, alto:int, rect_tablero:pygame.Rect)->list[pygame.Rect]:
    '''
    Funcion: Genera una matriz con valores Rect.
    Parametros: 1 Lista de valores del tamaño a generar, 2 enteros con el ancho y el alto de la pantalla
    y 1 el rectangulo donde se va a generar la matriz.
    Retorno: Devuelve una lista con Rectangulos.
    '''
    matriz_rect = []
    ancho_cuadradito = (rect_tablero.width - 3) / len(matriz)
    altura_cuadradito = (rect_tablero.height - 3) / len(matriz)
    separador = (rect_tablero.width - 3) // 100
    for y in range(len(matriz)):
        matriz_rect.append([])
        for x in range(len(matriz[y])):
            casilla = pygame.Rect(ancho * 20 / 100 + 3 + ancho_cuadradito * x, alto * 5 / 100 + 3 + altura_cuadradito * y, ancho_cuadradito - separador / 2, altura_cuadradito - separador / 2)
            matriz_rect[y].append(casilla)
    return matriz_rect

def devolver_color(cord_y:int, cord_x:int, dicc_barcos:list[dict], matriz_valor:list)->str:
    '''
    Funcion: compara la matriz valor con los diccionario para devolver un color: 
    -blanco si aun no se interactuo.
    -azul si es mar.
    -naranja si el barco esta dañado.
    -rojo si el barco fue destruido.
    Parametros: se pasan dos enteros con que representan la coordenada a comparar, la lista con los valores
    y una lista de diccionarios que contiene los barcos.
    Retorno: Devuelve una cadena con un color.
    '''
    bandera = False
    if matriz_valor[cord_y][cord_x] != "X":
        color = "white"
    else:
        for barco in dicc_barcos:
            if bandera == False:
                if (cord_y,cord_x) not in barco["coordenadas"]:
                    color = "blue"
                else:
                    for cord in barco["coordenadas"]:
                        if (cord_y,cord_x) == cord:
                            color = "orange"
                            if barco["destruidos"] == len(barco["coordenadas"]):
                                color = "red"
                            bandera = True
    return color

def dibujar_tablero(matriz_valor:list, matriz_rect:list[pygame.Rect], dicc_barcos:list[dict], pantalla:pygame.surface, rect_tablero:pygame.Rect)->None:
    '''
    Funcion: Dibuja el tablero de juego
    Parametros: 3 listas, una con valores enteros o cadena, otra con rectangulos para las casillas y otra con
    los diccionarios de barcos y una superficie donde dibujar
    Retorno: No devuelve nada
    '''
    pygame.draw.rect(pantalla, (122, 122, 122), rect_tablero)
    for y in range(len(matriz_rect)):
            for x in range(len(matriz_rect[y])):
                color = devolver_color(y, x, dicc_barcos, matriz_valor)
                pygame.draw.rect(pantalla, color, matriz_rect[y][x])


def validar_mar(matriz:list, cord_y:int, cord_x:int, tamaño:int, direccion:int= 0)->bool:
    '''
    Funcion: Valida que la coordenada pasada y/o sus consecutivos sean 0.
    Parametros: 1 lista de valores enteros y 4 enteros con coordenadas tamaño del barco a validar y su
    direccion.
    Retorno: Devuelve un booleano True en caso de que se cumpla que la coordenada y sus consecutivos
    tengan 0, sino False
    '''
    retorno = False
    if direccion == 0:
        for i in range(0, tamaño):
            if matriz[cord_y][cord_x + i] == 0:
                retorno = True
    else:
        for i in range(0, tamaño):
            if matriz[cord_y+ i][cord_x] == 0:
                retorno = True
    return retorno

def agregar_naval(matriz:list, tamaño:int)->dict:
    '''
    Funcion: Agrega un barco validando que pueda colocarse.
    Parametros: Una matriz de valores enteros y el tamaño del barco.
    Retorno: Devuelve Un diccionario con las coordenadas y el estado del barco.
    '''
    bandera = True
    while bandera == True:
        direccion = random.randint(0, 1)
        cord_y = random.randint(0, len(matriz) - tamaño)
        cord_x = random.randint(0, len(matriz[0]) - tamaño)
        if direccion == 0:
            if validar_mar(matriz, cord_y, cord_x, tamaño, direccion) == True:
                barco = {}
                cord_barco = []
                for i in range(0, tamaño):
                    matriz[cord_y][cord_x + i] = 1
                    cord_barco.append((cord_y, cord_x + i))
                barco.update({"coordenadas": cord_barco})
                barco.update({"destruidos": 0})
                bandera = False
        else:
            if validar_mar(matriz, cord_y, cord_x, tamaño, direccion) == True:
                barco = {}
                cord_barco = []
                for i in range(0, tamaño):
                    matriz[cord_y + i][cord_x] = 1
                    cord_barco.append((cord_y + i, cord_x))
                barco.update({"coordenadas": cord_barco})
                barco.update({"destruidos": 0})
                bandera = False
    return barco

def rellenar_tablero(matriz:list, submarinos:int, destructores:int, cruceros:int, acorazados:int)-> list[dict]:
    '''
    Funcion: Agrega los barcos requeridos en el tablero y almacena sus coordenadas y contador de destruccion.
    Parametros: Una matriz de valores enteros(En principio todo es 0) y 4 enteros con la cantidad de cada tipo
    de barcos requeridos.
    Retorno: Devuelve una lista con los diccionarios de cada barco.
    '''
    dicc_barcos = []
    
    tamaño_submarinos = 1
    tamaño_destructores = 2
    tamaño_cruceros = 3
    tamaño_acorazados = 4
    
    for _ in range(acorazados):
        barco = agregar_naval(matriz, tamaño_acorazados)
        dicc_barcos.append(barco)
    for _ in range(cruceros):
        barco = agregar_naval(matriz, tamaño_cruceros)
        dicc_barcos.append(barco)
    for _ in range(destructores):
        barco = agregar_naval(matriz, tamaño_destructores)
        dicc_barcos.append(barco)
    for _ in range(submarinos):
        barco = agregar_naval(matriz, tamaño_submarinos)
        dicc_barcos.append(barco)
    return dicc_barcos

def impacto_naval(matriz_valor:list, cord_y:int, cord_x:int, dicc_barcos:list[dict])->int:
    '''
    Funcion: Pregunta si la coordenada pasada no fue anteriormente seleccionada. Cuyo caso se pregunta si
    la coordenada corresponde a un barco y suma 5 puntos y 1 a la clave de destruidos de dicho
    barco. Luego se pregunta si este fue destruido y de una bonificacion de 10 puntos por cada casilla
    del barco. Si no es un barco se resta 1 punto.
    Parametro: Se pasa por parametro una lista con valores, un undice de filas, un indice de columnas y una
    lista de diccionarios que representa a los barcos.
    Retorno: Se devuelve un entero con el valor a sumar/restar.
    '''
    bonificacion = 0
    impacto = 0
    if matriz_valor[cord_y][cord_x] != "X":
        if matriz_valor[cord_y][cord_x] == 1:
            for barco in dicc_barcos:
                for cord in barco["coordenadas"]:
                    if (cord_y, cord_x) == cord:
                        impacto = 5
                        contador_destruidos = barco["destruidos"]
                        contador_destruidos += 1
                        barco.update({"destruidos": contador_destruidos})
                        matriz_valor[cord_y][cord_x] = "X"
                        if barco["destruidos"] == len(barco["coordenadas"]):
                            bonificacion = 10 * barco["destruidos"]
        elif matriz_valor[cord_y][cord_x] == 0:
            impacto = -1
            matriz_valor[cord_y][cord_x] = "X"
    retorno = impacto + bonificacion
    return retorno

def entero_zfill(entero:int, cifras:int)->str:
    '''
    Funcion: Devolver un entero en formato str con ceros a la izquierda y ajustado para mostrar al usuario
    Parametro: Entero (int); cantidad de cifras a mostrar (int)
    Retorno: Entero (str) con el metodo .zfill() aplicado
    '''
    entero_str = str(entero)
    if entero >= 0:
        retorno = " " + entero_str.zfill(cifras)
    else:
        retorno = entero_str.zfill(cifras + 1)
    return retorno

def estado_juego(matriz_valor:list)->bool:
    '''
    Funcion: Revisa que no haya ningun barco(1) en la matriz.
    Parametro: La matriz con los valores del tablero.
    Retorno: Devuelve un booleano True en caso de que ya no haya barcos, sino False.
    '''
    retorno = True
    for x in range(len(matriz_valor)):
        for y in range(len(matriz_valor[x])):
            if matriz_valor[x][y] == 1:
                retorno = False
    return retorno

def guardar_record_json(ruta:str, datos:any)->None:
    '''
    Funcion: Guardar un record dentro de un archivo .json
    Parametros: Ruta del archivo (str), datos a guardar (any)
    Retorno: None. Guardado de datos
    '''
    with open(ruta, "w") as archivo_puntaje:
        json.dump(datos, archivo_puntaje, indent=4)

def cargar_record_json(ruta:str)->list[dict]:
    '''
    Funcion: Cargar los records de un archivo .json
    Parametro: Ruta del archivo (str)
    Retorno: Lista de diccionarios con los datos (list[dict])
    '''
    with open(ruta, "r") as archivo_puntaje:
        records = json.load(archivo_puntaje)
    return records

def ordenar_records(lista:list[dict])->None:
    '''
    Funcion: Ordenar la lista segun los puntajes de los usuarios de manera descendente
    Parametros: Lista de jugadores (list[dict])
    Retorno: None. Ordena la lista recibida
    '''
    lista.sort(key=lambda dicc: dicc["Puntaje"], reverse=True)

def mostrar_records(lista:list[dict], clave_puntaje:str, fuente:pygame.font.Font, color:tuple|str, pantalla:pygame.Surface, ubicacion_inicial:list, paso_x:int, paso_y:int)->None:
    '''
    Funcion: Mostrar los mejores records registrados en el juego.
    Parametro: Datos de los jugadores, clave para acceder a puntajes, fuente de texto, pantalla, ubicacion inicial del primer dato a mostrar.
    Retorno: None. Imprime por pantalla los datos obtenidos
    '''
    if len(lista) != 0:
        ubicacion_pantalla = ubicacion_inicial.copy()
        for jugador in lista:
            ubicacion_pantalla[0] = ubicacion_inicial[0]
            for clave in jugador.keys():
                if clave == clave_puntaje:
                    puntaje_str = entero_zfill(jugador[clave], 4)
                    texto = fuente.render(puntaje_str, True, color)
                else:
                    texto = fuente.render(jugador[clave], True, color)
                rect_texto_centralizado = texto.get_rect(center=ubicacion_pantalla)
                pantalla.blit(texto, rect_texto_centralizado)
                ubicacion_pantalla[0] += paso_x
            ubicacion_pantalla[1] += paso_y

def guardar_record_lista(lista:list[dict], claves:list, valores:list)->None:
    '''
    Funcion: Guardar un record dentro de una lista de diccionarios
    Parametros: La lista donde se guardaran los records (list[dict]), la lista de claves (list), la lista de llaves (list)
    Retorno: None. Se modifica la lista con los datos cargados.
    '''
    dicc = {}
    for i in range(len(claves)):
        dicc.update({claves[i]:valores[i]})
    lista.append(dicc)