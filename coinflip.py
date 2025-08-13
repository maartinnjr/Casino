import pygame
import random
import sys
import os
import ctypes
import math

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- NUEVO: Función para cargar imágenes ---
def cargar_imagen(nombre_archivo):
    """ Carga una imagen desde la carpeta 'img'. """
    try:
        ruta_imagen = resource_path(os.path.join("img", nombre_archivo))
        return pygame.image.load(ruta_imagen).convert_alpha()
    except pygame.error as e:
        print(f"Error al cargar imagen '{nombre_archivo}': {e}")
        # Devuelve una superficie de error si la imagen no se encuentra
        superficie_error = pygame.Surface((100, 100))
        superficie_error.fill((255, 0, 255)) # Color fucsia para indicar error
        return superficie_error

def cargar_sonido(nombre):
    """ Carga un archivo de sonido desde la carpeta 'sounds'. """
    try:
        ruta_sonido = resource_path(os.path.join("sounds", nombre))
        return pygame.mixer.Sound(ruta_sonido)
    except pygame.error as e:
        print(f"Error al cargar sonido '{nombre}': {e}")
        return None

# --- CONFIGURACIÓN DE LA UI ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (220, 20, 60)
DORADO = (218, 165, 32)
DORADO_CLARO = (255, 215, 0)

COLOR_SIDEBAR = (18, 18, 18, 235)
ANCHO_SIDEBAR = 210
ANCHO_BOTON, ALTO_BOTON = 150, 60

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

# --- FUNCIÓN DE MONEDA MODIFICADA PARA USAR IMÁGENES ---
def generar_animacion_desde_imagenes(tamano, cara_img, sello_img):
    """ Genera la animación de giro a partir de dos imágenes cargadas. """
    imagenes = []
    num_frames_por_lado = 15 # Aumentar frames para suavidad
    
    # Redimensionar las imágenes base al tamaño deseado
    cara_base = pygame.transform.smoothscale(cara_img, (tamano, tamano))
    sello_base = pygame.transform.smoothscale(sello_img, (tamano, tamano))

    for i in range(num_frames_por_lado * 2):
        frame_surf = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
        
        progreso = i / (num_frames_por_lado - 1)
        if i >= num_frames_por_lado:
            progreso = 2 - progreso

        # Usar coseno para una transición de tamaño más suave (ease-in, ease-out)
        ancho_rel = abs(math.cos(progreso * math.pi / 2))
        ancho_actual = int(tamano * ancho_rel)
        if ancho_actual < 1: ancho_actual = 1

        # Seleccionar la textura (cara o sello) y escalarla
        textura_actual = cara_base if i < num_frames_por_lado else sello_base
        textura_escalada = pygame.transform.smoothscale(textura_actual, (ancho_actual, tamano))
        
        rect_textura = textura_escalada.get_rect(center=(tamano // 2, tamano // 2))
        frame_surf.blit(textura_escalada, rect_textura)
        
        imagenes.append(frame_surf)
        
    return imagenes


class Boton:
    """ Clase para crear botones interactivos con texto. """
    def __init__(self, x, y, texto, color_normal, color_hover, fuente_boton):
        self.texto = texto
        self.fuente = fuente_boton
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_seleccionado = DORADO
        self.rect = pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON)
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
            return True
        return False

def juego_coinflip():
    """ Función principal del juego de Coinflip. """
    pygame.init()
    pygame.mixer.init()

    info_local = pygame.display.Info()
    ANCHO, ALTO = info_local.current_w, info_local.current_h
    
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Cara o Sello - Palacio de la fortuna")

    if os.name == 'nt':
        try:
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.ShowWindow(hwnd, 3)
        except Exception as e:
            print(f"No se pudo forzar la ventana al frente/maximizar: {e}")

    fuente = pygame.font.SysFont("arial", 24, bold=True)
    fuente_titulo = pygame.font.SysFont("arial", 40, bold=True)
    fuente_resultado = pygame.font.SysFont("arial", 50, bold=True)
    fuente_mediana = pygame.font.SysFont("arial", 28)

    sonidos = {
        # "lanzar": cargar_sonido("coin_flip.wav"), # SONIDO DE LANZAMIENTO DESACTIVADO
        "ganar": cargar_sonido("winfruit.wav"),
        "perder": cargar_sonido("lose.wav")
    }

    fondo_img = pygame.image.load(resource_path("fondocoinflip.jpg")).convert()
    
    # --- CARGA DE IMÁGENES DE LA MONEDA ---
    cara_img_original = cargar_imagen("cara.png")
    sello_img_original = cargar_imagen("sello.png")
    
    tamano_moneda = 300
    imagenes_moneda = generar_animacion_desde_imagenes(tamano_moneda, cara_img_original, sello_img_original)
    # Guardar una copia redimensionada para mostrarla estática
    cara_img = pygame.transform.smoothscale(cara_img_original, (tamano_moneda, tamano_moneda))
    sello_img = pygame.transform.smoothscale(sello_img_original, (tamano_moneda, tamano_moneda))

    x_botones = (ANCHO_SIDEBAR - ANCHO_BOTON) // 2
    y_inicial_botones = 150
    espacio_botones = ALTO_BOTON + 20
    
    boton_cara = Boton(x_botones, y_inicial_botones, "CARA", (200, 150, 0), (255, 215, 0), fuente)
    boton_sello = Boton(x_botones, y_inicial_botones + espacio_botones, "SELLO", (100, 100, 150), (150, 150, 200), fuente)
    boton_lanzar = Boton(x_botones, y_inicial_botones + espacio_botones * 2.5, "LANZAR", (0, 100, 0), (50, 150, 50), fuente)
    boton_salir = Boton(x_botones, ALTO - ALTO_BOTON - 40, "SALIR", (150, 0, 0), (200, 50, 50), fuente)

    corriendo = True
    reloj = pygame.time.Clock()
    seleccion = None
    estado = "esperando"
    
    frame_animacion = 0
    resultado_final = None
    
    altura_moneda_y = 0
    velocidad_y = 0
    gravedad = -0.8
    
    tiempo_resultado = None
    boton_volver_rect = None
    
    imagen_mostrada = cara_img
    tiempo_inicio_animacion = 0

    while corriendo:
        ancho_actual, alto_actual = ventana.get_size()
        fondo_escalado = pygame.transform.scale(fondo_img, (ancho_actual, alto_actual))
        ventana.blit(fondo_escalado, (0, 0))

        sidebar_surf = pygame.Surface((ANCHO_SIDEBAR, alto_actual), pygame.SRCALPHA)
        sidebar_surf.fill(COLOR_SIDEBAR)
        ventana.blit(sidebar_surf, (0, 0))

        ancho_area_juego = ancho_actual - ANCHO_SIDEBAR
        centro_x_juego = ANCHO_SIDEBAR + ancho_area_juego // 2
        
        titulo_render = fuente_titulo.render("Cara o Sello - ¡GANA X2!", True, BLANCO)
        ventana.blit(titulo_render, (centro_x_juego - titulo_render.get_width() // 2, 45))

        boton_cara.dibujar(ventana)
        boton_sello.dibujar(ventana)
        boton_lanzar.dibujar(ventana)
        boton_salir.dibujar(ventana)

        centro_moneda_base = (centro_x_juego, alto_actual // 2 + 50)
        
        sombra_rect = pygame.Rect(0, 0, tamano_moneda * 0.8, 20)
        sombra_rect.center = (centro_moneda_base[0], centro_moneda_base[1] + tamano_moneda // 2 + 20)
        sombra_surf = pygame.Surface(sombra_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_surf, (0, 0, 0, 80), sombra_surf.get_rect())
        ventana.blit(sombra_surf, sombra_rect)

        centro_moneda_actual = (centro_moneda_base[0], centro_moneda_base[1] - altura_moneda_y)
        
        tamano_caja = tamano_moneda + 60
        rect_caja_moneda = pygame.Rect(0, 0, tamano_caja, tamano_caja)
        rect_caja_moneda.center = centro_moneda_base
        dibujar_caja_transparente(ventana, rect_caja_moneda, (0, 0, 0, 150), radius=20)
        pygame.draw.rect(ventana, DORADO, rect_caja_moneda, 2, border_radius=20)

        if estado == "animacion":
            duracion_animacion = 3500
            if pygame.time.get_ticks() - tiempo_inicio_animacion > duracion_animacion:
                estado = "resultado"
                altura_moneda_y = 0
                resultado_final = random.choice(["CARA", "SELLO"])
                
                imagen_mostrada = cara_img if resultado_final == "CARA" else sello_img

                if seleccion == resultado_final:
                    resultado_texto_final = "¡Ganaste!"
                    crear_resultado("ganaste")
                    if sonidos.get("ganar"): sonidos["ganar"].play()
                else:
                    resultado_texto_final = "Perdiste..."
                    crear_resultado("perdiste")
                    if sonidos.get("perder"): sonidos["perder"].play()
                
                tiempo_resultado = pygame.time.get_ticks()
            else:
                velocidad_animacion = 0.9
                frame_animacion = (frame_animacion + velocidad_animacion) % len(imagenes_moneda)
                
                altura_moneda_y += velocidad_y
                velocidad_y += gravedad
                if altura_moneda_y < 0:
                    altura_moneda_y = 0
                    velocidad_y = 0

                imagen_actual = imagenes_moneda[int(frame_animacion)]
                rect_img = imagen_actual.get_rect(center=centro_moneda_actual)
                ventana.blit(imagen_actual, rect_img)
        
        else:
            rect_img = imagen_mostrada.get_rect(center=centro_moneda_actual)
            ventana.blit(imagen_mostrada, rect_img)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                crear_resultado("perdiste")
                corriendo = False

            if estado == "resultado" and evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver_rect and boton_volver_rect.collidepoint(evento.pos):
                    corriendo = False
            
            if estado == "esperando":
                if boton_cara.verificar_clic(evento):
                    seleccion = "CARA"
                    boton_cara.seleccionado = True
                    boton_sello.seleccionado = False
                    imagen_mostrada = cara_img
                elif boton_sello.verificar_clic(evento):
                    seleccion = "SELLO"
                    boton_sello.seleccionado = True
                    boton_cara.seleccionado = False
                    imagen_mostrada = sello_img
                elif boton_lanzar.verificar_clic(evento) and seleccion:
                    estado = "animacion"
                    velocidad_y = 25
                    tiempo_inicio_animacion = pygame.time.get_ticks()
                    if sonidos.get("lanzar"): sonidos["lanzar"].play()
                elif boton_salir.verificar_clic(evento):
                    crear_resultado("perdiste")
                    corriendo = False
        
        if estado == "resultado" and tiempo_resultado:
            if pygame.time.get_ticks() - tiempo_resultado >= 2500:
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

                color_display = DORADO_CLARO if "Ganaste" in resultado_texto_final else ROJO
                texto_render = fuente_resultado.render(resultado_texto_final, True, color_display)
                texto_lado_ganador = fuente.render(f"El resultado fue: {resultado_final}", True, BLANCO)
                
                ventana.blit(texto_render, (rect_resultado.centerx - texto_render.get_width() // 2, rect_resultado.centery - 80))
                ventana.blit(texto_lado_ganador, (rect_resultado.centerx - texto_lado_ganador.get_width() // 2, rect_resultado.centery - 20))

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
