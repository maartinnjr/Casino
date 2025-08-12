import pygame
import random
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
PLATA = (192, 192, 192)
AZUL_REY = (65, 105, 225)
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

def generar_imagenes_moneda(tamano, fuente_simbolo):
    """ Genera las superficies de Pygame para la animación de la moneda. """
    imagenes = []
    radio = tamano // 2
    
    # Marcos de la animación (ancho de la elipse)
    anchos_animacion = [1.0, 0.8, 0.6, 0.4, 0.1, 0.4, 0.6, 0.8, 1.0]

    # Crear cara
    cara_surf = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
    pygame.draw.circle(cara_surf, DORADO, (radio, radio), radio)
    pygame.draw.circle(cara_surf, (255, 223, 0), (radio, radio), radio - 5)
    simbolo_c = fuente_simbolo.render("C", True, NEGRO)
    cara_surf.blit(simbolo_c, simbolo_c.get_rect(center=(radio, radio)))
    
    # Crear sello
    sello_surf = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
    pygame.draw.circle(sello_surf, PLATA, (radio, radio), radio)
    pygame.draw.circle(sello_surf, (220, 220, 220), (radio, radio), radio - 5)
    simbolo_s = fuente_simbolo.render("S", True, NEGRO)
    sello_surf.blit(simbolo_s, simbolo_s.get_rect(center=(radio, radio)))

    # Generar frames de animación
    for i, ancho_rel in enumerate(anchos_animacion):
        frame_surf = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
        color = DORADO if i < len(anchos_animacion) / 2 else PLATA
        pygame.draw.ellipse(frame_surf, color, (radio - radio * ancho_rel, 0, tamano * ancho_rel, tamano))
        imagenes.append(frame_surf)
        
    imagenes.insert(0, cara_surf) # Frame inicial es Cara
    imagenes.insert(5, sello_surf) # Frame intermedio es Sello
    
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
    fuente_simbolo_moneda = pygame.font.SysFont("timesnewroman", 150, bold=True)

    fondo_img = pygame.image.load(resource_path("fondocoinflip.jpg")).convert()
    
    # --- CAMBIO: Moneda más grande ---
    tamano_moneda = 350
    imagenes_moneda = generar_imagenes_moneda(tamano_moneda, fuente_simbolo_moneda)

    x_botones = (ANCHO_SIDEBAR - ANCHO_BOTON) // 2
    y_inicial_botones = 150
    espacio_botones = ALTO_BOTON + 20
    
    boton_cara = Boton(x_botones, y_inicial_botones, "CARA", DORADO, (255, 215, 0), fuente)
    boton_sello = Boton(x_botones, y_inicial_botones + espacio_botones, "SELLO", AZUL_REY, (100, 149, 237), fuente)
    boton_lanzar = Boton(x_botones, y_inicial_botones + espacio_botones * 2.5, "LANZAR", (0, 100, 0), (50, 150, 50), fuente)
    boton_salir = Boton(x_botones, ALTO - ALTO_BOTON - 40, "SALIR", (150, 0, 0), (200, 50, 50), fuente)

    corriendo = True
    reloj = pygame.time.Clock()
    seleccion = None
    estado = "esperando"
    
    frame_animacion = 0
    velocidad_animacion = 0.5
    resultado_final = None
    
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
        
        titulo_render = fuente_titulo.render("Cara o Sello - ¡GANA X2!", True, BLANCO)
        ventana.blit(titulo_render, (centro_x_juego - titulo_render.get_width() // 2, 45))

        boton_cara.dibujar(ventana)
        boton_sello.dibujar(ventana)
        boton_lanzar.dibujar(ventana)
        boton_salir.dibujar(ventana)

        # --- CAMBIO: Cuadro para la moneda ---
        centro_moneda = (centro_x_juego, alto_actual // 2)
        tamano_caja = tamano_moneda + 50
        rect_caja_moneda = pygame.Rect(centro_moneda[0] - tamano_caja // 2, centro_moneda[1] - tamano_caja // 2, tamano_caja, tamano_caja)
        
        dibujar_caja_transparente(ventana, rect_caja_moneda, (0, 0, 0, 150), radius=20)
        pygame.draw.rect(ventana, DORADO, rect_caja_moneda, 2, border_radius=20)


        # Lógica de la moneda
        if estado == "animacion":
            frame_animacion += velocidad_animacion
            if frame_animacion >= len(imagenes_moneda):
                frame_animacion = 0
            imagen_actual = imagenes_moneda[int(frame_animacion)]
            rect_img = imagen_actual.get_rect(center=centro_moneda)
            ventana.blit(imagen_actual, rect_img)
        
        elif estado == "resultado":
            imagen_final = imagenes_moneda[0] if resultado_final == "CARA" else imagenes_moneda[5]
            rect_img = imagen_final.get_rect(center=centro_moneda)
            ventana.blit(imagen_final, rect_img)
        else:
            imagen_espera = imagenes_moneda[0]
            rect_img = imagen_espera.get_rect(center=centro_moneda)
            ventana.blit(imagen_espera, rect_img)

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
                elif boton_sello.verificar_clic(evento):
                    seleccion = "SELLO"
                    boton_sello.seleccionado = True
                    boton_cara.seleccionado = False
                elif boton_lanzar.verificar_clic(evento) and seleccion:
                    estado = "animacion"
                    tiempo_inicio_animacion = pygame.time.get_ticks()
                elif boton_salir.verificar_clic(evento):
                    crear_resultado("perdiste")
                    corriendo = False
        
        if estado == "animacion":
            if pygame.time.get_ticks() - tiempo_inicio_animacion > 3000:
                estado = "resultado"
                resultado_final = random.choice(["CARA", "SELLO"])
                
                if seleccion == resultado_final:
                    resultado_texto_final = "¡Ganaste!"
                    crear_resultado("ganaste")
                else:
                    resultado_texto_final = "Perdiste..."
                    crear_resultado("perdiste")
                
                tiempo_resultado = pygame.time.get_ticks()

        if estado == "resultado" and tiempo_resultado:
            if pygame.time.get_ticks() - tiempo_resultado >= 1000:
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
