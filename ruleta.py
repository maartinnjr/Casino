import pygame
import random
import math
import sys
import os
import ctypes

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CONFIGURACIÓN DE LA UI ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (220, 20, 60)
DORADO = (218, 165, 32)
COLOR_SIDEBAR = (18, 18, 18, 235)
ANCHO_SIDEBAR = 210
ANCHO_BOTON, ALTO_BOTON = 150, 60

# Variables de Pygame que se inicializarán más tarde
fuente = None
fuente_titulo = None
fuente_resultado = None
fuente_mediana = None
ventana = None
ANCHO, ALTO = None, None

def crear_resultado(resultado_texto):
    """ Escribe el resultado del juego en 'resultado.txt'. """
    resultado_txt_path = resource_path("resultado.txt")
    with open(resultado_txt_path, "w") as f:
        f.write(resultado_texto)

def dibujar_caja_transparente(superficie, rect, color, radius=15):
    """ Dibuja una caja rectangular semi-transparente con esquinas redondeadas. """
    caja_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(caja_surf, color, caja_surf.get_rect(), border_radius=radius)
    superficie.blit(caja_surf, rect.topleft)

class Boton:
    """ Clase para crear botones interactivos con texto. """
    def __init__(self, x, y, texto, color_normal, color_hover, fuente_boton):
        self.texto = texto
        self.fuente = fuente_boton
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_seleccionado = DORADO
        self.rect = pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON)
        self.clicado = False
        self.seleccionado = False

    def dibujar(self, superficie):
        color_actual = self.color_normal
        if self.seleccionado:
            color_actual = self.color_seleccionado
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            color_actual = self.color_hover
        
        pygame.draw.rect(superficie, color_actual, self.rect, border_radius=10)
        pygame.draw.rect(superficie, BLANCO, self.rect, 2, border_radius=10)

        texto_render = self.fuente.render(self.texto, True, BLANCO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        superficie.blit(texto_render, texto_rect)

    def verificar_clic(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.rect.collidepoint(evento.pos):
            self.clicado = True
            return True
        self.clicado = False
        return False

def dibujar_ruleta(ventana_surf, angulo, centro_ruleta, radio, sectores, angulo_sector):
    """ Dibuja la ruleta en la ventana de Pygame. """
    pygame.draw.circle(ventana_surf, DORADO, centro_ruleta, radio + 10)

    for i in range(sectores):
        start_angle = math.radians(angulo + i * angulo_sector)
        end_angle = math.radians(angulo + (i + 1) * angulo_sector)
        color_sector = ROJO if i % 2 == 0 else NEGRO

        puntos = [centro_ruleta]
        pasos = 30
        for p in range(pasos + 1):
            interp_angle = start_angle + (end_angle - start_angle) * (p / pasos)
            x = centro_ruleta[0] + radio * math.cos(interp_angle)
            y = centro_ruleta[1] + radio * math.sin(interp_angle)
            puntos.append((x, y))
        pygame.draw.polygon(ventana_surf, color_sector, puntos)

    pygame.draw.circle(ventana_surf, NEGRO, centro_ruleta, 30)

def dibujar_flecha_fija_imagen(ventana_surf, flecha_img_val, centro_ruleta, radio):
    """ Dibuja la imagen de la flecha fija sobre la ruleta. """
    flecha_rotada = pygame.transform.rotate(flecha_img_val, 0)
    flecha_pos = (centro_ruleta[0] - flecha_rotada.get_width() // 2, centro_ruleta[1] - radio - flecha_rotada.get_height() - 5)
    ventana_surf.blit(flecha_rotada, flecha_pos)

def juego_ruleta():
    """ Función principal del juego de la ruleta. """
    pygame.init()
    pygame.mixer.init()

    global ANCHO, ALTO, ventana, fuente, fuente_titulo, fuente_resultado, fuente_mediana
    info_local = pygame.display.Info()
    ANCHO, ALTO = info_local.current_w, info_local.current_h
    
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Ruleta - Palacio de la fortuna")

    if os.name == 'nt':
        try:
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.ShowWindow(hwnd, 3)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
        except Exception as e:
            print(f"No se pudo forzar la ventana al frente/maximizar: {e}")

    fuente = pygame.font.SysFont("arial", 24, bold=True)
    fuente_titulo = pygame.font.SysFont("arial", 40, bold=True)
    fuente_resultado = pygame.font.SysFont("arial", 50, bold=True)
    fuente_mediana = pygame.font.SysFont("arial", 28)


    sonido_ganar = pygame.mixer.Sound(resource_path("sounds/winfruit.wav"))
    sonido_perder = pygame.mixer.Sound(resource_path("sounds/lose.wav"))
    sonido_giro = pygame.mixer.Sound(resource_path("sounds/spin.wav"))

    fondo_img = pygame.image.load(resource_path("fondoruleta.jpg")).convert()
    flecha_img = pygame.image.load(resource_path("flecha.png")).convert_alpha()
    flecha_img = pygame.transform.scale(flecha_img, (40, 40))

    x_botones = (ANCHO_SIDEBAR - ANCHO_BOTON) // 2
    y_inicial_botones = 150
    espacio_botones = ALTO_BOTON + 20
    
    boton_rojo = Boton(x_botones, y_inicial_botones, "ROJO", ROJO, (255, 80, 100), fuente)
    boton_negro = Boton(x_botones, y_inicial_botones + espacio_botones, "NEGRO", NEGRO, (80, 80, 80), fuente)
    boton_girar = Boton(x_botones, y_inicial_botones + espacio_botones * 2.5, "GIRAR", (0, 100, 0), (50, 150, 50), fuente)
    boton_salir = Boton(x_botones, ALTO - ALTO_BOTON - 40, "SALIR", (150, 0, 0), (200, 50, 50), fuente)

    corriendo = True
    reloj = pygame.time.Clock()
    seleccion = None
    resultado_texto_final = ""
    color_ganador = None
    estado = "esperando"
    angulo = 0
    velocidad_giro = 0
    deceleracion = 0.15
    tiempo_resultado = None
    boton_volver_rect = None

    while corriendo:
        ancho_actual, alto_actual = ventana.get_size()
        fondo_escalado = pygame.transform.scale(fondo_img, (ancho_actual, alto_actual))
        ventana.blit(fondo_escalado, (0, 0))

        sidebar_surf = pygame.Surface((ANCHO_SIDEBAR, alto_actual), pygame.SRCALPHA)
        sidebar_surf.fill(COLOR_SIDEBAR)
        ventana.blit(sidebar_surf, (0, 0))

        ancho_area_juego = ancho_actual - ANCHO_SIDEBAR
        centro_x_juego = ANCHO_SIDEBAR + ancho_area_juego // 2
        
        titulo_render = fuente_titulo.render("Ruleta - ¡GANA X2!", True, BLANCO)
        ventana.blit(titulo_render, (centro_x_juego - titulo_render.get_width() // 2, 45))

        centro_ruleta = (centro_x_juego, (alto_actual // 2) + 50)
        radio = min(ancho_area_juego, alto_actual) // 2 - 150
        sectores = 10
        angulo_sector = 360 / sectores

        dibujar_ruleta(ventana, angulo, centro_ruleta, radio, sectores, angulo_sector)
        dibujar_flecha_fija_imagen(ventana, flecha_img, centro_ruleta, radio)
        
        boton_rojo.dibujar(ventana)
        boton_negro.dibujar(ventana)
        boton_girar.dibujar(ventana)
        boton_salir.dibujar(ventana)

        if estado == "esperando":
            texto_info = "Elige un color y GIRA"
        elif estado == "girando":
            texto_info = "¡Girando...!"
        else:
            texto_info = f"Ganador: {color_ganador}"
        
        mensaje_info = fuente.render(texto_info, True, DORADO)
        ventana.blit(mensaje_info, (ANCHO_SIDEBAR + 40, alto_actual - 60))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # --- INICIO: CORRECCIÓN SALIDA SIN JUGAR ---
                if estado == "esperando":
                    crear_resultado("empate")
                else:
                    crear_resultado("perdiste")
                # --- FIN: CORRECCIÓN SALIDA SIN JUGAR ---
                corriendo = False

            if estado == "resultado" and evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver_rect and boton_volver_rect.collidepoint(evento.pos):
                    corriendo = False 
            
            if estado != "girando":
                if boton_rojo.verificar_clic(evento):
                    seleccion = "ROJO"
                    boton_rojo.seleccionado = True
                    boton_negro.seleccionado = False
                elif boton_negro.verificar_clic(evento):
                    seleccion = "NEGRO"
                    boton_negro.seleccionado = True
                    boton_rojo.seleccionado = False
                elif boton_girar.verificar_clic(evento) and seleccion:
                    estado = "girando"
                    if sonido_giro: sonido_giro.play()
                    velocidad_giro = random.uniform(20, 30)
                elif boton_salir.verificar_clic(evento):
                    # --- INICIO: CORRECCIÓN SALIDA SIN JUGAR ---
                    if estado == "esperando":
                        crear_resultado("empate")
                    else:
                        crear_resultado("perdiste")
                    # --- FIN: CORRECCIÓN SALIDA SIN JUGAR ---
                    corriendo = False


        if estado == "girando":
            angulo = (angulo + velocidad_giro) % 360
            velocidad_giro -= deceleracion
            if velocidad_giro <= 0:
                velocidad_giro = 0
                angulo_puntero = (270 - angulo) % 360
                sector_ganador = int(angulo_puntero // angulo_sector)
                
                color_ganador = "ROJO" if sector_ganador % 2 == 0 else "NEGRO"

                if seleccion == color_ganador:
                    resultado_texto_final = "¡Ganaste!"
                    crear_resultado("ganaste")
                    if sonido_ganar: sonido_ganar.play()
                else:
                    resultado_texto_final = "Perdiste..."
                    crear_resultado("perdiste")
                    if sonido_perder: sonido_perder.play()

                estado = "resultado"
                tiempo_resultado = pygame.time.get_ticks()

        elif estado == "resultado":
            if pygame.time.get_ticks() - tiempo_resultado >= 1500:
                capa_oscura = pygame.Surface((ancho_actual, alto_actual), pygame.SRCALPHA)
                capa_oscura.fill((0, 0, 0, 200))
                ventana.blit(capa_oscura, (0, 0))

                ancho_caja_res, alto_caja_res = 550, 280
                rect_resultado = pygame.Rect(
                    (ancho_actual - ancho_caja_res) // 2,
                    (alto_actual - alto_caja_res) // 2,
                    ancho_caja_res, alto_caja_res
                )
                dibujar_caja_transparente(ventana, rect_resultado, (20, 20, 20, 230), radius=20)
                pygame.draw.rect(ventana, DORADO, rect_resultado, 3, border_radius=20)

                color_display = DORADO if "Ganaste" in resultado_texto_final else ROJO
                texto_render = fuente_resultado.render(resultado_texto_final, True, color_display)
                texto_color_ganador = fuente.render(f"El color ganador fue: {color_ganador}", True, BLANCO)
                
                ventana.blit(texto_render, (rect_resultado.centerx - texto_render.get_width() // 2, rect_resultado.centery - 80))
                ventana.blit(texto_color_ganador, (rect_resultado.centerx - texto_color_ganador.get_width() // 2, rect_resultado.centery - 20))

                boton_volver_rect = pygame.Rect(rect_resultado.centerx - 150, rect_resultado.centery + 40, 300, 60)
                pygame.draw.rect(ventana, ROJO, boton_volver_rect, border_radius=12)
                texto_boton = fuente_mediana.render("Volver al casino", True, BLANCO)
                ventana.blit(texto_boton, (
                    boton_volver_rect.centerx - texto_boton.get_width() // 2,
                    boton_volver_rect.centery - texto_boton.get_height() // 2
                ))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
