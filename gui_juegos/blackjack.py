import pygame
import random
import os
import sys
import ctypes

def resource_path(relative_path):
    """
    Obtiene la ruta absoluta a un recurso, para que funcione en desarrollo y en el ejecutable.

    Args:
        relative_path (str): La ruta relativa del archivo dentro del proyecto.

    Returns:
        str: La ruta absoluta y multiplataforma al recurso.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Constantes de UI y Colores ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE_OSCURO = (0, 100, 0)
DORADO = (218, 165, 32)
ROJO = (255, 0, 0)
COLOR_SIDEBAR = (18, 18, 18, 235) 
ANCHO_SIDEBAR = 210
ANCHO_CARTA, ALTO_CARTA = 140, 210
ANCHO_BOTON, ALTO_BOTON = 90, 90
COLOR_CAJA_TRANSPARENTE = (0, 0, 0, 150)

# --- Variables Globales de Pygame (se inicializan en juego_blackjack) ---
fuente_grande = None
fuente_mediana = None
fuente_chica = None
ventana = None 

def cargar_imagen(nombre, directorio="img"):
    """
    Carga una imagen, la escala y maneja errores si no se encuentra.

    Args:
        nombre (str): El nombre del archivo de la imagen.
        directorio (str, optional): El subdirectorio donde se encuentra la imagen.

    Returns:
        pygame.Surface: La superficie de la imagen cargada o una superficie de error.
    """
    ruta = resource_path(os.path.join(directorio, nombre))
    try:
        return pygame.image.load(ruta)
    except pygame.error as e:
        print(f"Error al cargar imagen '{nombre}': {e}")
        return crear_superficie_error() 

def crear_superficie_error():
    """
    Crea una superficie roja para indicar que una imagen no pudo ser cargada.

    Returns:
        pygame.Surface: Una superficie rectangular de color rojo.
    """
    superficie = pygame.Surface((ANCHO_CARTA, ALTO_CARTA))
    superficie.fill(ROJO)
    pygame.draw.rect(superficie, BLANCO, (0, 0, ANCHO_CARTA, ALTO_CARTA), 2)
    return superficie

def cargar_sonido(nombre):
    """
    Carga un archivo de sonido desde la carpeta 'sounds'.

    Args:
        nombre (str): El nombre del archivo de sonido.

    Returns:
        pygame.mixer.Sound or None: El objeto de sonido cargado o None si hay un error.
    """
    try:
        ruta_sonido = resource_path(os.path.join("sounds", nombre))
        return pygame.mixer.Sound(ruta_sonido)
    except pygame.error as e:
        print(f"Error al cargar sonido '{nombre}': {e}")
        return None

# --- Definición de la Baraja ---
valores = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
palos = ["H", "D", "S", "C"]
cartas = [f"{valor}{palo}.png" for valor in valores for palo in palos]

class Boton:
    """Clase para crear botones interactivos con imágenes en Pygame."""
    def __init__(self, x, y, imagen_normal_subdir_path, imagen_hover_subdir_path):
        """
        Inicializa el botón con sus imágenes normal y de hover.

        Args:
            x (int): Posición X del botón.
            y (int): Posición Y del botón.
            imagen_normal_subdir_path (str): Ruta relativa de la imagen normal.
            imagen_hover_subdir_path (str): Ruta relativa de la imagen cuando el cursor está encima.
        """
        self.imagen_normal = cargar_imagen(imagen_normal_subdir_path)
        self.imagen_hover = cargar_imagen(imagen_hover_subdir_path)
        self.imagen_normal = pygame.transform.scale(self.imagen_normal, (ANCHO_BOTON, ALTO_BOTON))
        self.imagen_hover = pygame.transform.scale(self.imagen_hover, (ANCHO_BOTON, ALTO_BOTON))
        self.rect = self.imagen_normal.get_rect(topleft=(x, y))
        self.clicado = False

    def dibujar(self, superficie):
        """
        Dibuja el botón en la superficie, cambiando la imagen si el mouse está encima.

        Args:
            superficie (pygame.Surface): La superficie donde se dibujará el botón.
        """
        imagen = self.imagen_hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.imagen_normal
        superficie.blit(imagen, self.rect.topleft)

    def verificar_clic(self, evento, sonidos_dict):
        """
        Verifica si el botón ha sido presionado.

        Args:
            evento (pygame.event.Event): El evento a procesar.
            sonidos_dict (dict): Diccionario de sonidos para reproducir el de clic.

        Returns:
            bool: True si el botón fue presionado, False en caso contrario.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.rect.collidepoint(evento.pos):
            if sonidos_dict and "boton" in sonidos_dict and sonidos_dict["boton"]:
                sonidos_dict["boton"].play()
            self.clicado = True
            return True
        self.clicado = False
        return False

def repartir_carta(baraja, mano, sonidos_dict):
    """
    Saca una carta aleatoria de la baraja y la añade a una mano.

    Args:
        baraja (list): La lista de cartas disponibles.
        mano (list): La mano del jugador o crupier a la que se añade la carta.
        sonidos_dict (dict): Diccionario de sonidos para reproducir el de repartir.

    Returns:
        str or None: El nombre del archivo de la carta repartida, o None si la baraja está vacía.
    """
    if baraja:
        carta = random.choice(baraja)
        baraja.remove(carta)
        mano.append(carta)
        if sonidos_dict and "repartir" in sonidos_dict and sonidos_dict["repartir"]:
            sonidos_dict["repartir"].play()
        return carta
    return None

def valor_carta(carta):
    """
    Calcula el valor numérico de una carta de Blackjack.

    Args:
        carta (str): El nombre del archivo de la carta (ej: 'KH.png', '10S.png').

    Returns:
        int: El valor numérico de la carta (As = 11, Figuras = 10).
    """
    valor_str = carta[:-5] 
    if valor_str.startswith('10'): return 10
    elif valor_str in ('J', 'Q', 'K'): return 10
    elif valor_str == 'A': return 11
    else: return int(valor_str)

def calcular_puntaje(mano):
    """
    Calcula el puntaje total de una mano de Blackjack, manejando los Ases.
    Un As puede valer 11 o 1. Se ajusta a 1 si el puntaje total excede 21.

    Args:
        mano (list): La lista de cartas en la mano.

    Returns:
        int: El puntaje total de la mano.
    """
    total = sum(valor_carta(carta) for carta in mano)
    ases = sum(1 for carta in mano if valor_carta(carta) == 11)
    while total > 21 and ases:
        total -= 10
        ases -= 1
    return total

def crear_resultado(resultado_texto):
    """
    Escribe el resultado del juego en 'resultado.txt' para que la GUI principal lo lea.
    Este es el mecanismo de comunicación clave entre el juego Pygame y la GUI Tkinter.

    Args:
        resultado_texto (str): El resultado ('ganaste', 'perdiste', 'empate').
    """
    resultado_txt_path = resource_path("resultado.txt")
    with open(resultado_txt_path, "w") as f:
        f.write(resultado_texto)

def dibujar_caja_transparente(superficie, rect, color, radius=15):
    """
    Dibuja una caja rectangular semi-transparente con esquinas redondeadas para la UI.

    Args:
        superficie (pygame.Surface): Superficie principal donde dibujar.
        rect (pygame.Rect): Posición y tamaño de la caja.
        color (tuple): Color RGBA de la caja.
        radius (int, optional): Radio de las esquinas.
    """
    caja_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(caja_surf, color, caja_surf.get_rect(), border_radius=radius)
    superficie.blit(caja_surf, rect.topleft)

def juego_blackjack():
    """
    Función principal que contiene el bucle y la lógica del juego de Blackjack.
    """
    pygame.init()
    pygame.mixer.init()

    global ventana, fuente_grande, fuente_mediana, fuente_chica
    info_local = pygame.display.Info()
    
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Blackjack Premium - Casino Virtual")

    if os.name == 'nt': 
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.ShowWindow(hwnd, 3)

    fuente_grande = pygame.font.SysFont("arial", 40)
    fuente_mediana = pygame.font.SysFont("arial", 28)
    fuente_chica = pygame.font.SysFont("arial", 18, bold=True)

    sonidos_locales = {
        "repartir": cargar_sonido("card_flip.wav"),
        "ganar": cargar_sonido("winfruit.wav"),
        "empate": cargar_sonido("win.wav"),
        "perder": cargar_sonido("lose.wav"),
        "boton": cargar_sonido("button.wav")
    }

    fondo_img = pygame.image.load(resource_path(os.path.join("img", "Fondos", "fondoblackjack.jpg"))).convert()
    baraja = cartas.copy()
    random.shuffle(baraja)

    cartas_jugador = []
    cartas_crupier = []

    for _ in range(2):
        repartir_carta(baraja, cartas_jugador, sonidos_locales)
        repartir_carta(baraja, cartas_crupier, sonidos_locales)

    ancho_actual, alto_actual = ventana.get_size()
    
    x_botones = (ANCHO_SIDEBAR - ANCHO_BOTON) // 2
    espacio_botones_juego = 60 
    altura_total_botones_juego = (2 * ALTO_BOTON) + espacio_botones_juego
    y_pedir = (alto_actual - altura_total_botones_juego) // 2 - 50
    y_plantarse = y_pedir + ALTO_BOTON + espacio_botones_juego
    y_salir = alto_actual - ALTO_BOTON - 30
    
    boton_pedir = Boton(x_botones, y_pedir, os.path.join("Blackjack", "botones", "pedir.png"), os.path.join("Blackjack", "botones", "pedir_hover.png"))
    boton_plantarse = Boton(x_botones, y_plantarse, os.path.join("Blackjack", "botones", "plantarse.png"), os.path.join("Blackjack", "botones", "plantarse_hover.png"))
    boton_salir = Boton(x_botones, y_salir, os.path.join("Blackjack", "botones", "salir.png"), os.path.join("Blackjack", "botones", "salir_hover.png"))

    reloj = pygame.time.Clock()
    corriendo = True
    juego_terminado = False
    resultado = ""
    tiempo_resultado = None

    while corriendo:
        fondo_escalado = pygame.transform.scale(fondo_img, (ancho_actual, alto_actual))
        ventana.blit(fondo_escalado, (0, 0))

        sidebar_surf = pygame.Surface((ANCHO_SIDEBAR, alto_actual), pygame.SRCALPHA)
        sidebar_surf.fill(COLOR_SIDEBAR)
        ventana.blit(sidebar_surf, (0, 0))
        
        ancho_area_juego = ancho_actual - ANCHO_SIDEBAR
        margen_horizontal_area = 40
        ancho_caja = ancho_area_juego - (margen_horizontal_area * 2)
        alto_caja = ALTO_CARTA + 120
        radio_borde = 15
        espacio_vertical_cajas = 40

        altura_total_bloque = (alto_caja * 2) + espacio_vertical_cajas
        y_caja_crupier = (alto_actual - altura_total_bloque) // 2
        y_caja_jugador = y_caja_crupier + alto_caja + espacio_vertical_cajas

        rect_area_crupier = pygame.Rect(ANCHO_SIDEBAR + margen_horizontal_area, y_caja_crupier, ancho_caja, alto_caja)
        dibujar_caja_transparente(ventana, rect_area_crupier, COLOR_CAJA_TRANSPARENTE, radius=radio_borde)
        pygame.draw.rect(ventana, DORADO, rect_area_crupier, 2, border_radius=radio_borde)

        rect_area_jugador = pygame.Rect(ANCHO_SIDEBAR + margen_horizontal_area, y_caja_jugador, ancho_caja, alto_caja)
        dibujar_caja_transparente(ventana, rect_area_jugador, COLOR_CAJA_TRANSPARENTE, radius=radio_borde)
        pygame.draw.rect(ventana, BLANCO, rect_area_jugador, 2, border_radius=radio_borde)

        puntaje_jugador = calcular_puntaje(cartas_jugador)
        puntaje_crupier_visible = calcular_puntaje(cartas_crupier[1:])
        puntaje_crupier_total = calcular_puntaje(cartas_crupier)

        texto_crupier_render = fuente_mediana.render(
            f"La Máquina: {puntaje_crupier_total}" if juego_terminado else f"La Máquina: {puntaje_crupier_visible}", True, BLANCO
        )
        ventana.blit(texto_crupier_render, (rect_area_crupier.left + 25, rect_area_crupier.top + 15))

        cartas_crupier_y = rect_area_crupier.top + texto_crupier_render.get_height() + 25
        num_cartas_crupier = len(cartas_crupier)
        ancho_total_cartas_crupier = num_cartas_crupier * (ANCHO_CARTA + 10) - 10
        inicio_x_crupier = rect_area_crupier.centerx - ancho_total_cartas_crupier / 2

        for i, carta in enumerate(cartas_crupier):
            img_x = inicio_x_crupier + i * (ANCHO_CARTA + 10)
            if i == 0 and not juego_terminado:
                card_rect = pygame.Rect(img_x, cartas_crupier_y, ANCHO_CARTA, ALTO_CARTA)
                pygame.draw.rect(ventana, ROJO, card_rect, border_radius=12)
                pygame.draw.rect(ventana, (150, 0, 0), card_rect, 5, border_radius=12)
            else:
                carta_img = cargar_imagen(os.path.join("Blackjack", "cartas", carta))
                carta_img = pygame.transform.scale(carta_img, (ANCHO_CARTA, ALTO_CARTA))
                ventana.blit(carta_img, (img_x, cartas_crupier_y))

        texto_jugador_render = fuente_mediana.render(f"Tú: {puntaje_jugador}", True, BLANCO)
        ventana.blit(texto_jugador_render, (rect_area_jugador.left + 25, rect_area_jugador.top + 15))

        cartas_jugador_y = rect_area_jugador.top + texto_jugador_render.get_height() + 25
        num_cartas_jugador = len(cartas_jugador)
        ancho_total_cartas_jugador = num_cartas_jugador * (ANCHO_CARTA + 10) - 10
        inicio_x_jugador = rect_area_jugador.centerx - ancho_total_cartas_jugador / 2

        for i, carta in enumerate(cartas_jugador):
            img_x = inicio_x_jugador + i * (ANCHO_CARTA + 10)
            carta_img = cargar_imagen(os.path.join("Blackjack", "cartas", carta))
            carta_img = pygame.transform.scale(carta_img, (ANCHO_CARTA, ALTO_CARTA))
            ventana.blit(carta_img, (img_x, cartas_jugador_y))

        boton_pedir.dibujar(ventana)
        boton_plantarse.dibujar(ventana)
        
        texto_pedir = fuente_chica.render("Pedir", True, BLANCO)
        ventana.blit(texto_pedir, (boton_pedir.rect.centerx - texto_pedir.get_width() // 2, boton_pedir.rect.bottom + 10))
        
        texto_plantarse = fuente_chica.render("Plantarse", True, BLANCO)
        ventana.blit(texto_plantarse, (boton_plantarse.rect.centerx - texto_plantarse.get_width() // 2, boton_plantarse.rect.bottom + 10))

        boton_salir.dibujar(ventana)

        if juego_terminado:
            if tiempo_resultado is None:
                tiempo_resultado = pygame.time.get_ticks()
            
            if pygame.time.get_ticks() - tiempo_resultado >= 1000:
                capa_oscura = pygame.Surface((ancho_actual, alto_actual), pygame.SRCALPHA)
                capa_oscura.fill((0, 0, 0, 200))
                ventana.blit(capa_oscura, (0, 0))

                ancho_caja_res, alto_caja_res = 550, 280
                rect_resultado = pygame.Rect(
                    (ancho_actual - ancho_caja_res) // 2,
                    (alto_actual - alto_caja_res) // 2,
                    ancho_caja_res,
                    alto_caja_res
                )
                dibujar_caja_transparente(ventana, rect_resultado, (20, 20, 20, 230), radius=20)
                pygame.draw.rect(ventana, DORADO, rect_resultado, 3, border_radius=20)

                color_resultado = DORADO if "ganaste" in resultado.lower() else ROJO if "perdiste" in resultado.lower() else BLANCO
                texto_resultado_render = fuente_grande.render(resultado, True, color_resultado)
                pos_y_resultado_texto = rect_resultado.centery - 60
                ventana.blit(texto_resultado_render, (rect_resultado.centerx - texto_resultado_render.get_width() // 2, pos_y_resultado_texto))

                boton_volver_rect = pygame.Rect(rect_resultado.centerx - 150, rect_resultado.centery + 20, 300, 60)
                pygame.draw.rect(ventana, ROJO, boton_volver_rect, border_radius=12)
                texto_boton = fuente_mediana.render("Volver al casino", True, BLANCO)
                ventana.blit(texto_boton, (
                    boton_volver_rect.centerx - texto_boton.get_width() // 2,
                    boton_volver_rect.centery - texto_boton.get_height() // 2
                ))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if not juego_terminado: crear_resultado("empate")
                corriendo = False
            
            if juego_terminado and tiempo_resultado is not None and (pygame.time.get_ticks() - tiempo_resultado >= 1000):
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if 'boton_volver_rect' in locals() and boton_volver_rect.collidepoint(evento.pos):
                        corriendo = False

            if not juego_terminado:
                if boton_pedir.verificar_clic(evento, sonidos_locales):
                    repartir_carta(baraja, cartas_jugador, sonidos_locales)
                    if calcular_puntaje(cartas_jugador) > 21:
                        resultado = "Perdiste! Te pasaste de 21."
                        juego_terminado = True
                        crear_resultado("perdiste")
                        if sonidos_locales.get("perder"): sonidos_locales["perder"].play()

                elif boton_plantarse.verificar_clic(evento, sonidos_locales):
                    while calcular_puntaje(cartas_crupier) < 17 and baraja:
                        repartir_carta(baraja, cartas_crupier, sonidos_locales)

                    puntaje_final_crupier = calcular_puntaje(cartas_crupier)
                    puntaje_final_jugador = calcular_puntaje(cartas_jugador)

                    if puntaje_final_crupier > 21 or puntaje_final_jugador > puntaje_final_crupier:
                        resultado = "Ganaste! Tienes mejor mano."
                        crear_resultado("ganaste")
                        if sonidos_locales.get("ganar"): sonidos_locales["ganar"].play()
                    elif puntaje_final_crupier > puntaje_final_jugador:
                        resultado = "Perdiste! La máquina tiene mejor mano."
                        crear_resultado("perdiste")
                        if sonidos_locales.get("perder"): sonidos_locales["perder"].play()
                    else:
                        resultado = "Empate!"
                        crear_resultado("empate")
                        if sonidos_locales.get("empate"): sonidos_locales["empate"].play()
                    
                    juego_terminado = True

            if boton_salir.verificar_clic(evento, sonidos_locales):
                if not juego_terminado: crear_resultado("empate")
                corriendo = False

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
