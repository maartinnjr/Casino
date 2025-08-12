import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
import pygame
from PIL import Image, ImageTk, ImageOps, ImageEnhance
import mysql.connector

from datetime import datetime

# --- IMPORTACIONES DE JUEGOS ---
import blackjack
import ruleta
import tragamonedas
import coinflip # <-- NUEVA IMPORTACIÓN

# --- CONFIGURACIÓN DE LA CONEXIÓN A LA BASE DE DATOS MYSQL ---
db_config = {
    'host': 'shinkansen.proxy.rlwy.net',
    'user': 'root',
    'password': 'wEWnpjufrkFVWvhNcMnoKCPXtfJEgrMD',
    'database': 'railway',
    'port': 53316
}

db_connection = None

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos."""
    global db_connection
    try:
        if db_connection is None or not db_connection.is_connected():
            db_connection = mysql.connector.connect(**db_config)
        else:
            db_connection.ping(reconnect=True)
        return db_connection
    except mysql.connector.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a la base de datos MySQL: {e}")
        sys.exit()
        return None

# --- AÑADIR COINFLIP AL MAPA DE JUEGOS ---
GAME_ID_MAP = {"Blackjack": 1, "Ruleta": 2, "Tragamonedas": 3, "Coinflip": 4}

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

SALDO_INICIAL = 2000

# --- PALETA DE COLORES ELEGANTE: ROJOS, DORADOS Y BLANCOS ---
# Se ha modificado esta sección para reflejar el nuevo estilo visual.
ELEGANT_COLORS = {
    "dark": {
        "bg": "#1A1A1A",                 # Fondo principal: Gris muy oscuro, casi negro
        "fg": "#FFFFFF",                 # Texto principal: Blanco puro
        "btn_bg": "#A62639",             # Botones principales: Rojo carmesí oscuro
        "btn_active": "#C43B4E",         # Botones activos/hover: Rojo más brillante
        "frame_bg": "#2C2C2C",           # Fondo de frames: Gris carbón
        "label_fg": "#FFD700",           # Etiquetas destacadas: Dorado brillante
        "tree_bg": "#2C2C2C",            # Fondo de Treeview: Gris carbón
        "tree_fg": "#FFFFFF",            # Texto de Treeview: Blanco
        "tree_heading_bg": "#A62639",    # Cabecera de Treeview: Rojo carmesí
        "tree_heading_fg": "#FFFFFF",    # Texto de cabecera de Treeview: Blanco
        "sidebar_bg": "#212121",         # Fondo de la barra lateral: Un poco más oscuro que los frames
        # Colores adicionales para consistencia
        "gold": "#FFD700",               # Dorado brillante
        "danger": "#C62828",
        "neutral": "#6c757d"
    },
    "light": { # No se modifica el tema claro
        "bg": "white", "fg": "black", "btn_bg": "#2980b9", "btn_active": "#3498db",
        "frame_bg": "#F5F5F5",
        "label_fg": "black", "tree_bg": "#EAEAEA",
        "tree_fg": "black", "tree_heading_bg": "#2980b9", "tree_heading_fg": "white",
        "sidebar_bg": "#DDDDDD"
    }
}

COLORES = ELEGANT_COLORS


class RoundButton(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, color, bg, command=None, text="", font=None, text_color="white", border_color="#666666", border_width=2):
        tk.Canvas.__init__(self, parent, borderwidth=0, relief="flat", highlightthickness=0, bg=bg)
        self.command = command
        self.width = width
        self.height = height
        self.cornerradius = cornerradius
        self.color = color
        self.hover_color = self._calculate_hover_color(color)
        self.press_color = self._calculate_press_color(color)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self._redraw(self.color)

    def _calculate_hover_color(self, color):
        r, g, b = self.winfo_rgb(color)
        r, g, b = int(r/256 * 1.15), int(g/256 * 1.15), int(b/256 * 1.15)
        return f'#{min(r, 255):02x}{min(g, 255):02x}{min(b, 255):02x}'

    def _calculate_press_color(self, color):
        r, g, b = self.winfo_rgb(color)
        r, g, b = int(r/256 * 0.85), int(g/256 * 0.85), int(b/256 * 0.85)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _draw_button(self, color):
        self.delete("button")
        r, w, h, bw, bc = self.cornerradius, self.width, self.height, self.border_width, self.border_color
        self.create_rectangle(r, 0, w - r, h, fill=bc, outline="", tags="button")
        self.create_rectangle(0, r, w, h - r, fill=bc, outline="", tags="button")
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, fill=bc, outline="", tags="button")
        self.create_arc(w - 2*r, 0, w, 2*r, start=0, extent=90, fill=bc, outline="", tags="button")
        self.create_arc(0, h - 2*r, 2*r, h, start=180, extent=90, fill=bc, outline="", tags="button")
        self.create_arc(w - 2*r, h - 2*r, w, h, start=270, extent=90, fill=bc, outline="", tags="button")
        inner_r = r - bw if r > bw else 0
        x0, y0, x1, y1 = bw, bw, w - bw, h - bw
        if x1 > x0 and y1 > y0:
            self.create_rectangle(x0 + inner_r, y0, x1 - inner_r, y1, fill=color, outline="", tags="button")
            self.create_rectangle(x0, y0 + inner_r, x1, y1 - inner_r, fill=color, outline="", tags="button")
            self.create_arc(x0, y0, x0 + 2*inner_r, y0 + 2*inner_r, start=90, extent=90, fill=color, outline="", tags="button")
            self.create_arc(x1 - 2*inner_r, y0, x1, y0 + 2*inner_r, start=0, extent=90, fill=color, outline="", tags="button")
            self.create_arc(x0, y1 - 2*inner_r, x0 + 2*inner_r, y1, start=180, extent=90, fill=color, outline="", tags="button")
            self.create_arc(x1 - 2*inner_r, y1 - 2*inner_r, x1, y1, start=270, extent=90, fill=color, outline="", tags="button")

    def _draw_text(self):
        self.delete("text")
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=self.font, fill=self.text_color, tags="text")

    def _redraw(self, color):
        self._draw_button(color)
        self._draw_text()

    def _on_press(self, event):
        self._redraw(self.press_color)

    def _on_release(self, event):
        if 0 < event.x < self.width and 0 < event.y < self.height and self.command:
            self.command()
        if self.winfo_exists():
            if self.winfo_containing(event.x_root, event.y_root) == self:
                self._redraw(self.hover_color)
            else:
                self._redraw(self.color)

    def _on_enter(self, event):
        self._redraw(self.hover_color)

    def _on_leave(self, event):
        self._redraw(self.color)

# --- FUNCIONES DE BASE DE DATOS ---

def get_dropdown_data(table_name):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        id_col = f"id_{table_name[:-1]}"
        name_col = f"nombre_{table_name[:-1]}"
        query = f"SELECT {id_col}, {name_col} FROM {table_name} ORDER BY {name_col}"
        cursor.execute(query)
        return sorted(cursor.fetchall(), key=lambda x: x[1])
    except Exception as e:
        print(f"Error al obtener datos de '{table_name}': {e}")
        return []
    finally:
        cursor.close()

def add_history(user_id, bet, result, game_name):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        id_juego = GAME_ID_MAP.get(game_name)
        if id_juego:
            query = "INSERT INTO historial_partidas (id_usuario, id_juego, apuesta, resultado, fecha) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id, id_juego, bet, result, datetime.now()))
            conn.commit()
    except Exception as e:
        print(f"Error al añadir al historial: {e}")
    finally:
        cursor.close()

def register_user(user, password, rut, address, currency, id_comuna, id_banco):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO usuarios (usuario, contrasena, saldo, rut, direccion, tipo_moneda, id_comuna, id_banco, dulces)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (user, password, SALDO_INICIAL, rut, address, currency, id_comuna, id_banco, 0)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Error de Registro", f"No se pudo registrar el usuario: {e}")
    finally:
        cursor.close()

def rut_exists(rut):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        query = "SELECT 1 FROM usuarios WHERE rut = %s LIMIT 1"
        cursor.execute(query, (rut,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar RUT: {e}")
        return False
    finally:
        cursor.close()

def authenticate_user(user, password, rut):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    try:
        query = "SELECT id_usuario, usuario, saldo FROM usuarios WHERE usuario = %s AND contrasena = %s AND rut = %s"
        cursor.execute(query, (user, password, rut))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error de autenticación: {e}")
        return None
    finally:
        cursor.close()

def authenticate_admin(user, password):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    try:
        query = "SELECT id_admin FROM administradores WHERE usuario = %s AND contrasena = %s"
        cursor.execute(query, (user, password))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error de autenticación de admin: {e}")
        return None
    finally:
        cursor.close()

def update_balance(user_id, balance):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        query = "UPDATE usuarios SET saldo = %s WHERE id_usuario = %s"
        cursor.execute(query, (balance, user_id))
        conn.commit()
    except Exception as e:
        print(f"Error al actualizar saldo: {e}")
    finally:
        cursor.close()

def get_all_users_for_admin():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = "SELECT id_usuario, usuario, rut, saldo, dulces FROM usuarios ORDER BY usuario"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener usuarios para admin: {e}")
        return []
    finally:
        cursor.close()

def get_user_balance(user_id):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    try:
        query = "SELECT saldo FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        conn.commit() 
        return result[0] if result else None
    except Exception as e:
        print(f"Error al obtener saldo: {e}")
        return None
    finally:
        cursor.close()

def get_top_10_ranking():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT usuario, saldo FROM usuarios ORDER BY saldo DESC LIMIT 10"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener el top 10 del ranking: {e}")
        return []
    finally:
        cursor.close()

def get_all_other_users(current_user_id):
    """Obtiene todos los usuarios excepto el actual para la lista de transferencia."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT id_usuario, usuario FROM usuarios WHERE id_usuario != %s ORDER BY usuario"
        cursor.execute(query, (current_user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener otros usuarios: {e}")
        return []
    finally:
        cursor.close()

def perform_candy_exchange(admin_id, user_id, saldo_cost, dulces_gain):
    conn = get_db_connection()
    if not conn:
        return False, "Sin conexión a la base de datos."
    
    cursor = conn.cursor()
    
    try:
        conn.start_transaction()

        query_saldo = "SELECT saldo, dulces FROM usuarios WHERE id_usuario = %s FOR UPDATE"
        cursor.execute(query_saldo, (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            raise ValueError("Usuario no encontrado.")
            
        current_balance, current_dulces = user_data
        
        if current_balance < saldo_cost:
            raise ValueError("El usuario no tiene saldo suficiente.")

        new_balance = current_balance - saldo_cost
        new_dulces = current_dulces + dulces_gain
        update_query = "UPDATE usuarios SET saldo = %s, dulces = %s WHERE id_usuario = %s"
        cursor.execute(update_query, (new_balance, new_dulces, user_id))

        canje_query = """
            INSERT INTO canjes_dulces 
            (id_admin, id_usuario, dulces_canjeados, costo_saldo, fecha) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(canje_query, (admin_id, user_id, dulces_gain, saldo_cost, datetime.now()))
        
        id_canje_nuevo = cursor.lastrowid

        transaccion_query = """
            INSERT INTO transacciones 
            (id_usuario, tipo_transaccion, monto, fecha, id_canje) 
            VALUES (%s, 'retiro', %s, %s, %s)
        """
        cursor.execute(transaccion_query, (user_id, saldo_cost, datetime.now(), id_canje_nuevo))

        conn.commit()
        
        return True, f"Canje exitoso. Nuevo saldo: ${new_balance}"

    except Exception as e:
        conn.rollback()
        return False, f"Error en la transacción: {e}"
        
    finally:
        cursor.close()

def perform_transfer(sender_id, recipient_id, amount, password):
    """Realiza la transferencia de saldo entre usuarios."""
    conn = get_db_connection()
    if not conn: return False, "Sin conexión a la base de datos."
    cursor = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()

        cursor.execute("SELECT contrasena, saldo FROM usuarios WHERE id_usuario = %s FOR UPDATE", (sender_id,))
        sender = cursor.fetchone()
        if not sender or sender['contrasena'] != password:
            return False, "Contraseña incorrecta."
        if sender['saldo'] < amount:
            return False, "Saldo insuficiente para realizar la transferencia."

        cursor.execute("UPDATE usuarios SET saldo = saldo - %s WHERE id_usuario = %s", (amount, sender_id))
        cursor.execute("UPDATE usuarios SET saldo = saldo + %s WHERE id_usuario = %s", (amount, recipient_id))

        now = datetime.now()
        cursor.execute("INSERT INTO transacciones (id_usuario, tipo_transaccion, monto, fecha) VALUES (%s, 'abono', %s, %s)", (sender_id, amount, now))
        cursor.execute("INSERT INTO transacciones (id_usuario, tipo_transaccion, monto, fecha) VALUES (%s, 'deposito', %s, %s)", (recipient_id, amount, now))
        
        conn.commit()
        return True, f"Transferencia de ${amount:,.0f} realizada con éxito.".replace(",", ".")
    except Exception as e:
        conn.rollback()
        return False, f"Error en la transacción: {e}"
    finally:
        cursor.close()

class CasinoApp:
    def __init__(self, root):
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(resource_path("musica_ambiente.mp3"))
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"No se pudo cargar la música: {e}")

        self.root = root
        self.current_mode = "dark"
        self.apply_theme()
        self.root.title("🎰 Casino Virtual 🎰")
        self.root.attributes('-fullscreen', True)

        self.current_user_id = None
        self.current_username = None
        self.current_balance = 0
        self.current_admin_id = None
        
        self.logo_casino_img = None
        self.logo_empresa_img = None
        
        self.slide_pil_images = []
        self.slide_tk_images = []
        self.dark_slide_tk_images = []
        self.current_slide_index = 0
        self.slide_label = None
        self.main_menu_bg_label = None
        self.after_id = None
        self.faded_image = None
        self.center_content_frame = None

        self.show_start_screen()

    def apply_theme(self):
        c = COLORES[self.current_mode]
        self.root.configure(bg=c["bg"])

    def animate_title(self, widget, colors, index=0):
        if widget.winfo_exists():
            widget.config(fg=colors[index])
            next_index = (index + 1) % len(colors)
            self.root.after(600, lambda: self.animate_title(widget, colors, next_index))

    def load_slides(self, size, darken=False, factor=0.3):
        self.slide_pil_images = []
        self.slide_tk_images = []
        self.dark_slide_tk_images = []
        slide_names = [f"slide{i}.png" for i in range(1, 6)]
        
        for name in slide_names:
            try:
                img = Image.open(resource_path(name)).convert("RGBA")
                img_fitted = ImageOps.fit(img, size, Image.LANCZOS)
                self.slide_pil_images.append(img_fitted)
                self.slide_tk_images.append(ImageTk.PhotoImage(img_fitted))
                
                enhancer = ImageEnhance.Brightness(img_fitted)
                dark_img = enhancer.enhance(factor)
                self.dark_slide_tk_images.append(ImageTk.PhotoImage(dark_img))

            except Exception as e:
                print(f"Error al cargar slide '{name}': {e}")
        
        if not self.slide_pil_images:
             fallback_img = Image.new('RGBA', size, color='black')
             self.slide_pil_images.append(fallback_img)
             self.slide_tk_images.append(ImageTk.PhotoImage(fallback_img))
             self.dark_slide_tk_images.append(ImageTk.PhotoImage(fallback_img))

    def start_slideshow(self, right_frame):
        if self.after_id: self.root.after_cancel(self.after_id)
        
        w, h = int(self.root.winfo_width() * 0.55), self.root.winfo_height()
        if w <= 1 or h <= 1:
            self.after_id = self.root.after(100, lambda: self.start_slideshow(right_frame))
            return
            
        self.load_slides((w, h))
        if not self.slide_tk_images: return

        if self.slide_label is None or not self.slide_label.winfo_exists():
            self.slide_label = tk.Label(right_frame, bg=COLORES[self.current_mode]["bg"])
            self.slide_label.pack(fill="both", expand=True)
            
        self.current_slide_index = 0
        self.slide_label.config(image=self.slide_tk_images[0])
        self.after_id = self.root.after(5000, self.change_slide)

    def change_slide(self, for_main_menu=False):
        if len(self.slide_pil_images) < 2: return

        from_idx = self.current_slide_index
        self.current_slide_index = (self.current_slide_index + 1) % len(self.slide_pil_images)
        
        if for_main_menu:
            if self.main_menu_bg_label and self.main_menu_bg_label.winfo_exists():
                self.main_menu_bg_label.config(image=self.dark_slide_tk_images[self.current_slide_index])
            self.after_id = self.root.after(5000, lambda: self.change_slide(for_main_menu=True))
        else:
            self._animate_fade(self.slide_pil_images[from_idx], self.slide_pil_images[self.current_slide_index])

    def _animate_fade(self, from_img, to_img, step=0):
        if step > 20:
            self.after_id = self.root.after(4500, self.change_slide)
            return
        blended_img = Image.blend(from_img, to_img, step / 20.0)
        self.faded_image = ImageTk.PhotoImage(blended_img)
        if self.slide_label.winfo_exists():
            self.slide_label.config(image=self.faded_image)
            self.root.after(25, lambda: self._animate_fade(from_img, to_img, step + 1))

    def _create_split_layout(self):
        self.clear_window()
        c = COLORES[self.current_mode]
        main_frame = tk.Frame(self.root, bg=c["bg"])
        main_frame.pack(fill="both", expand=True)
        left_frame = tk.Frame(main_frame, bg=c["bg"])
        left_frame.place(relx=0, rely=0, relwidth=0.45, relheight=1)
        right_frame = tk.Frame(main_frame, bg=c["bg"])
        right_frame.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)
        self.start_slideshow(right_frame)
        return left_frame

    def _toggle_password_visibility(self, entry, button):
        """Helper function to toggle password visibility."""
        if entry.cget('show') == '*':
            entry.config(show='')
            button.config(text='🔐')
        else:
            entry.config(show='*')
            button.config(text='🔓')

    def confirm_quit(self):
        """Shows a confirmation dialog before quitting the application."""
        if messagebox.askyesno("Confirmar Salida", "¿Está seguro de que desea salir del casino?"):
            self.root.quit()

    def show_start_screen(self):
        left_frame = self._create_split_layout()
        c = COLORES[self.current_mode]
        content_container = tk.Frame(left_frame, bg=c["bg"])
        content_container.pack(expand=True)
        try:
            img_casino = Image.open(resource_path("logo_casino.png"))
            img_casino.thumbnail((250, 250), Image.LANCZOS)
            self.logo_casino_img = ImageTk.PhotoImage(img_casino)
            logo_casino_label = tk.Label(content_container, image=self.logo_casino_img, bg=c["bg"])
            logo_casino_label.pack(pady=(50, 20))
        except Exception as e:
            print(f"No se pudo cargar logo_casino.png: {e}")
        title = tk.Label(content_container, text="💰🏆 ¡Bienvenido/a! 🎲👑", font=("Helvetica", 28, "bold"), bg=c["bg"], fg=c["fg"])
        title.pack(pady=(0, 20))
        self.animate_title(title, [c["gold"], c["fg"], "#E6C200"]) # Animación dorada
        button_frame = tk.Frame(content_container, bg=c["bg"])
        button_frame.pack(pady=20)
        btn_w, btn_h, btn_radius, btn_font = 300, 60, 6, ("Arial", 18, "bold")
        RoundButton(button_frame, btn_w, btn_h, btn_radius, c["btn_bg"], c["bg"], self.show_register_screen, "📝 Registrarse", btn_font).pack(pady=10)
        RoundButton(button_frame, btn_w, btn_h, btn_radius, c["gold"], c["bg"], self.show_login_screen, "🔐 Iniciar Sesión", btn_font).pack(pady=10)
        RoundButton(button_frame, btn_w, btn_h, btn_radius, c["danger"], c["bg"], self.confirm_quit, "❌ Salir", btn_font).pack(pady=10)
        try:
            img_empresa = Image.open(resource_path("logo_empresa.png"))
            img_empresa.thumbnail((200, 100), Image.LANCZOS)
            self.logo_empresa_img = ImageTk.PhotoImage(img_empresa)
            logo_empresa_label = tk.Label(content_container, image=self.logo_empresa_img, bg=c["bg"])
            logo_empresa_label.pack(side="bottom", pady=(20, 40))
        except Exception as e:
            print(f"No se pudo cargar logo_empresa.png: {e}")

    def show_register_screen(self):
        left_frame = self._create_split_layout()
        c = COLORES[self.current_mode]
        content_container = tk.Frame(left_frame, bg=c["bg"])
        content_container.pack(expand=True, fill="both")

        try:
            img_empresa = Image.open(resource_path("logo_empresa.png"))
            img_empresa.thumbnail((180, 90), Image.LANCZOS)
            self.logo_empresa_img = ImageTk.PhotoImage(img_empresa)
            logo_empresa_label = tk.Label(content_container, image=self.logo_empresa_img, bg=c["bg"])
            logo_empresa_label.pack(side="bottom", pady=(10, 20))
        except Exception as e:
            print(f"No se pudo cargar logo_empresa.png: {e}")

        center_frame = tk.Frame(content_container, bg=c["bg"])
        center_frame.pack(expand=True)

        try:
            img_casino = Image.open(resource_path("logo_casino.png"))
            img_casino.thumbnail((180, 180), Image.LANCZOS)
            self.logo_casino_img = ImageTk.PhotoImage(img_casino)
            logo_casino_label = tk.Label(center_frame, image=self.logo_casino_img, bg=c["bg"])
            logo_casino_label.pack(pady=(15, 10))
        except Exception as e:
            print(f"No se pudo cargar logo_casino.png: {e}")

        tk.Label(center_frame, text="📑  Registrarse  📑", font=("Helvetica", 24, "bold"), fg=c["label_fg"], bg=c["bg"]).pack(pady=(0, 20))
        
        form_frame = tk.Frame(center_frame, bg=c["frame_bg"], bd=5, relief="ridge", padx=25, pady=20)
        form_frame.pack(padx=30, pady=15)
        field_font, label_font = ("Arial", 14), ("Arial", 14)
        
        entries = {}
        row_num = 1

        tk.Label(form_frame, text="Usuario:", font=label_font, bg=c["frame_bg"], fg=c["fg"]).grid(row=row_num, column=0, sticky="w", pady=4, padx=5)
        user_entry = tk.Entry(form_frame, font=field_font, width=25)
        user_entry.grid(row=row_num, column=1, columnspan=2, sticky="we", pady=4, padx=5)
        entries["Usuario"] = user_entry
        row_num += 1

        tk.Label(form_frame, text="Contraseña:", font=label_font, bg=c["frame_bg"], fg=c["fg"]).grid(row=row_num, column=0, sticky="w", pady=4, padx=5)
        pass_frame = tk.Frame(form_frame, bg=c["frame_bg"])
        password_entry = tk.Entry(pass_frame, font=field_font, width=22, show="*")
        password_entry.pack(side="left", fill="x", expand=True)
        toggle_btn = tk.Button(pass_frame, text="🔓", font=("Arial", 10), relief="flat", bg=c["frame_bg"], fg=c["fg"], borderwidth=0, highlightthickness=0)
        toggle_btn.config(command=lambda e=password_entry, b=toggle_btn: self._toggle_password_visibility(e, b))
        toggle_btn.pack(side="left", padx=(5,0))
        pass_frame.grid(row=row_num, column=1, columnspan=2, sticky="we", pady=4, padx=5)
        entries["Contraseña"] = password_entry
        row_num += 1

        tk.Label(form_frame, text="RUT:", font=label_font, bg=c["frame_bg"], fg=c["fg"]).grid(row=row_num, column=0, sticky="w", pady=4, padx=5)
        rut_entry = tk.Entry(form_frame, font=field_font, width=25)
        rut_entry.grid(row=row_num, column=1, columnspan=2, sticky="we", pady=4, padx=5)
        entries["RUT"] = rut_entry
        row_num += 1

        tk.Label(form_frame, text="Dirección:", font=label_font, bg=c["frame_bg"], fg=c["fg"]).grid(row=row_num, column=0, sticky="w", pady=4, padx=5)
        address_entry = tk.Entry(form_frame, font=field_font, width=25)
        address_entry.grid(row=row_num, column=1, columnspan=2, sticky="we", pady=4, padx=5)
        entries["Dirección"] = address_entry
        row_num += 1
        
        comunas_data = get_dropdown_data('comunas')
        self.comunas_map = {name: id_ for id_, name in comunas_data}
        comuna_combo = ttk.Combobox(form_frame, values=[name for _, name in comunas_data], font=field_font, state="readonly")
        tk.Label(form_frame, text="Comuna:", font=label_font, bg=c["frame_bg"], fg=c["fg"]).grid(row=row_num, column=0, sticky="w", pady=4, padx=5)
        comuna_combo.grid(row=row_num, column=1, columnspan=2, sticky="we", pady=4, padx=5)
        entries["Comuna"] = comuna_combo
        row_num += 1

        bancos_data = get_dropdown_data('bancos')
        self.bancos_map = {name: id_ for id_, name in bancos_data}
        banco_combo = ttk.Combobox(form_frame, values=[name for _, name in bancos_data], font=field_font, state="readonly")
        tk.Label(form_frame, text="Banco:", font=label_font, bg=c["frame_bg"], fg=c["fg"]).grid(row=row_num, column=0, sticky="w", pady=4, padx=5)
        banco_combo.grid(row=row_num, column=1, columnspan=2, sticky="we", pady=4, padx=5)
        entries["Banco"] = banco_combo
        row_num += 1

        moneda_combo = ttk.Combobox(form_frame, values=['CLP', 'USD', 'EUR'], font=field_font, state="readonly")
        moneda_combo.set('CLP')
        tk.Label(form_frame, text="Moneda:", font=label_font, bg=c["frame_bg"], fg=c["fg"]).grid(row=row_num, column=0, sticky="w", pady=4, padx=5)
        moneda_combo.grid(row=row_num, column=1, columnspan=2, sticky="we", pady=4, padx=5)
        entries["Moneda"] = moneda_combo
        row_num += 1

        def register():
            values = {key: entry.get() for key, entry in entries.items()}
            if not all(values.values()):
                messagebox.showerror("Error de Validación", "Por favor, complete todos los campos.")
                return
            if rut_exists(values["RUT"]):
                messagebox.showerror("Error de Validación", "El RUT ingresado ya está registrado.")
                return
            id_comuna = self.comunas_map.get(values["Comuna"])
            id_banco = self.bancos_map.get(values["Banco"])
            register_user(values["Usuario"], values["Contraseña"], values["RUT"], values["Dirección"], values["Moneda"], id_comuna, id_banco)
            messagebox.showinfo("Registro Exitoso", f"Usuario '{values['Usuario']}' registrado con éxito.")
            self.show_start_screen()

        button_container = tk.Frame(center_frame, bg=c["bg"])
        button_container.pack(pady=(15, 5))
        btn_w, btn_h, btn_radius, btn_font = 260, 45, 6, ("Arial", 14, "bold")
        RoundButton(button_container, btn_w, btn_h, btn_radius, c["btn_bg"], c["bg"], register, "Registrar Cuenta", btn_font).pack(pady=5)
        RoundButton(button_container, btn_w, btn_h, btn_radius, c["neutral"], c["bg"], self.show_start_screen, "⬅ Volver", btn_font).pack(pady=5)

    def show_login_screen(self):
        left_frame = self._create_split_layout()
        c = COLORES[self.current_mode]
        content_container = tk.Frame(left_frame, bg=c["bg"])
        content_container.pack(expand=True, fill="both")
        
        try:
            img_empresa = Image.open(resource_path("logo_empresa.png"))
            img_empresa.thumbnail((200, 100), Image.LANCZOS)
            self.logo_empresa_img = ImageTk.PhotoImage(img_empresa)
            logo_empresa_label = tk.Label(content_container, image=self.logo_empresa_img, bg=c["bg"])
            logo_empresa_label.pack(side="bottom", pady=(15, 30))
        except Exception as e:
            print(f"No se pudo cargar logo_empresa.png: {e}")

        center_frame = tk.Frame(content_container, bg=c["bg"])
        center_frame.pack(expand=True)

        try:
            img_casino = Image.open(resource_path("logo_casino.png"))
            img_casino.thumbnail((200, 200), Image.LANCZOS)
            self.logo_casino_img = ImageTk.PhotoImage(img_casino)
            logo_casino_label = tk.Label(center_frame, image=self.logo_casino_img, bg=c["bg"])
            logo_casino_label.pack(pady=(20, 15))
        except Exception as e:
            print(f"No se pudo cargar logo_casino.png: {e}")
        
        tk.Label(center_frame, text="📑  Iniciar Sesión  �", font=("Helvetica", 26, "bold"), fg=c["label_fg"], bg=c["bg"]).pack(pady=(0, 20))
        
        form_frame = tk.Frame(center_frame, bg=c["frame_bg"], bd=5, relief="ridge", padx=30, pady=25)
        form_frame.pack(pady=15)
        
        tk.Label(form_frame, text="Usuario:", font=("Arial", 16), bg=c["frame_bg"], fg=c["fg"]).pack(pady=(8, 4))
        user_entry = tk.Entry(form_frame, font=("Arial", 16), width=25)
        user_entry.pack(pady=(0, 8), ipady=4)
        
        tk.Label(form_frame, text="Contraseña:", font=("Arial", 16), bg=c["frame_bg"], fg=c["fg"]).pack(pady=4)
        pass_frame = tk.Frame(form_frame, bg=c["frame_bg"])
        password_entry = tk.Entry(pass_frame, font=("Arial", 16), show="*", width=22)
        password_entry.pack(side="left", ipady=4)
        toggle_btn = tk.Button(pass_frame, text="🔓", font=("Arial", 10), relief="flat", bg=c["frame_bg"], fg=c["fg"], borderwidth=0, highlightthickness=0)
        toggle_btn.config(command=lambda e=password_entry, b=toggle_btn: self._toggle_password_visibility(e, b))
        toggle_btn.pack(side="left", padx=(5,0), fill="y")
        pass_frame.pack(pady=(0, 8))

        tk.Label(form_frame, text="RUT:", font=("Arial", 16), bg=c["frame_bg"], fg=c["fg"]).pack(pady=4)
        rut_entry = tk.Entry(form_frame, font=("Arial", 16), width=25)
        rut_entry.pack(pady=(0, 12), ipady=4)

        def login():
            user = user_entry.get()
            password = password_entry.get()
            rut = rut_entry.get()
            if not user or not password or not rut:
                messagebox.showerror("Error", "Complete todos los campos.")
                return
            user_data = authenticate_user(user, password, rut)
            if user_data:
                self.current_user_id, self.current_username, self.current_balance = user_data
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "Usuario, contraseña o RUT incorrectos.")

        button_container = tk.Frame(center_frame, bg=c["bg"])
        button_container.pack(pady=15)
        btn_w, btn_h, btn_radius, btn_font = 260, 45, 6, ("Arial", 14, "bold")
        RoundButton(button_container, btn_w, btn_h, btn_radius, c["btn_bg"], c["bg"], login, "Ingresar", btn_font).pack(pady=5)
        RoundButton(button_container, btn_w, btn_h, btn_radius, c["neutral"], c["bg"], self.show_start_screen, "⬅ Volver", btn_font).pack(pady=5)

    def refresh_balance_display(self):
        if self.current_user_id and hasattr(self, 'balance_label') and self.balance_label.winfo_exists():
            latest_balance = get_user_balance(self.current_user_id)
            if latest_balance is not None:
                self.current_balance = latest_balance
                self.balance_label.config(text=f"🃏 Saldo: ${self.current_balance:,.0f}".replace(",", "."))

    def refresh_ranking_display(self):
        if hasattr(self, 'ranking_tree') and self.ranking_tree.winfo_exists():
            for item in self.ranking_tree.get_children():
                self.ranking_tree.delete(item)
            top_10_data = get_top_10_ranking()
            for i, user_data in enumerate(top_10_data, 1):
                saldo_formateado = f"${user_data['saldo']:,.0f}".replace(",", ".")
                self.ranking_tree.insert("", "end", values=(f"{i}", user_data['usuario'], saldo_formateado))

    def show_main_menu(self):
        if self.after_id: self.root.after_cancel(self.after_id)
        self.clear_window()
        c = COLORES[self.current_mode]

        main_container = tk.Frame(self.root, bg=c["bg"])
        main_container.pack(fill="both", expand=True)

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.load_slides((w, h), darken=True)
        
        self.main_menu_bg_label = tk.Label(main_container, bg=c["bg"])
        self.main_menu_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        if self.dark_slide_tk_images:
            self.main_menu_bg_label.config(image=self.dark_slide_tk_images[0])
            self.after_id = self.root.after(5000, lambda: self.change_slide(for_main_menu=True))

        sidebar_frame = tk.Frame(main_container, bg=c["sidebar_bg"], width=280, relief="raised", bd=2)
        sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        sidebar_frame.pack_propagate(False)

        tk.Label(sidebar_frame, text="Acciones", font=("Helvetica", 20, "bold"), bg=c["sidebar_bg"], fg=c["btn_bg"]).pack(pady=25, padx=10)
        
        top_buttons_frame = tk.Frame(sidebar_frame, bg=c["sidebar_bg"])
        top_buttons_frame.pack(pady=10, padx=20, fill="x")

        sidebar_btn_font = ("Arial", 14, "bold")
        # Botones de la barra lateral ahora son rojos
        RoundButton(top_buttons_frame, 220, 55, 6, c["btn_bg"], c["sidebar_bg"], self.show_transfer_window, "💸 Transferir Saldo", sidebar_btn_font, text_color=c["fg"]).pack(pady=10)
        RoundButton(top_buttons_frame, 220, 55, 6, c["btn_bg"], c["sidebar_bg"], self.show_ranking, "🏆 Ver Ranking", sidebar_btn_font, text_color=c["fg"]).pack(pady=10)
        RoundButton(top_buttons_frame, 220, 55, 6, c["btn_bg"], c["sidebar_bg"], self.show_user_history, "📜 Ver Historial", sidebar_btn_font, text_color=c["fg"]).pack(pady=10)
        RoundButton(top_buttons_frame, 220, 55, 6, c["btn_bg"], c["sidebar_bg"], self.open_admin_login, "🍬 Canjear Dulces", sidebar_btn_font, text_color=c["fg"]).pack(pady=10)

        bottom_button_frame = tk.Frame(sidebar_frame, bg=c["sidebar_bg"])
        bottom_button_frame.pack(side="bottom", pady=25, padx=20, fill="x")
        # Botón de cerrar sesión ahora es rojo
        RoundButton(bottom_button_frame, 220, 55, 6, c["danger"], c["sidebar_bg"], self.logout, "🚪 Cerrar Sesión", sidebar_btn_font).pack(pady=10)

        right_sidebar_frame = tk.Frame(main_container, bg=c["sidebar_bg"], width=380, relief="raised", bd=2)
        right_sidebar_frame.pack(side="right", fill="y", padx=0, pady=0)
        right_sidebar_frame.pack_propagate(False)

        prizes_frame = tk.Frame(right_sidebar_frame, bg=c["sidebar_bg"])
        prizes_frame.pack(pady=(25, 15), padx=15, fill="x")

        self.prizes_title_label = tk.Label(prizes_frame, text="🏆 Tabla de Premios 🍬", font=("Helvetica", 20, "bold"), bg=c["sidebar_bg"], fg=c["gold"])
        self.prizes_title_label.pack()
        self.animate_title(self.prizes_title_label, [c["gold"], c["btn_bg"], c["fg"]])
        
        style = ttk.Style()
        style.theme_use('default')
        # Cabeceras de la tabla de premios ahora son doradas con texto oscuro
        style.configure("Prizes.Treeview", background=c["tree_bg"], foreground=c["tree_fg"], fieldbackground=c["tree_bg"], font=("Arial", 12), rowheight=30)
        style.map('Prizes.Treeview', background=[('selected', c["btn_bg"])])
        style.configure("Prizes.Treeview.Heading", background=c["gold"], foreground=c["bg"], font=("Arial", 14, "bold"))
        
        prizes_tree_frame = tk.Frame(prizes_frame, bd=2, relief="groove")
        prizes_tree_frame.pack(pady=10, fill="x")
        
        prizes_columns = ("premio", "costo")
        prizes_tree = ttk.Treeview(prizes_tree_frame, columns=prizes_columns, show="headings", style="Prizes.Treeview", height=4)
        prizes_tree.pack(fill="x")
        
        prizes_tree.heading("premio", text="Premio")
        prizes_tree.heading("costo", text="Costo")
        prizes_tree.column("premio", anchor="w", width=160)
        prizes_tree.column("costo", anchor="e", width=160)

        premios = [("🍬 2 Dulces", "$10.000"), ("🍬 3 Dulces", "$15.000"), ("🍬 4 Dulces", "$20.000"), ("🍬 6 Dulces", "$30.000")]
        for premio, costo in premios:
            prizes_tree.insert("", "end", values=(premio, costo))

        ranking_frame = tk.Frame(right_sidebar_frame, bg=c["sidebar_bg"])
        ranking_frame.pack(pady=15, padx=15, fill="both", expand=True)

        self.ranking_title_label = tk.Label(ranking_frame, text="⭐ Top 10 Jugadores ⭐", font=("Helvetica", 20, "bold"), bg=c["sidebar_bg"], fg=c["gold"])
        self.ranking_title_label.pack()
        self.animate_title(self.ranking_title_label, [c["gold"], c["btn_bg"], c["fg"]])

        ranking_tree_frame = tk.Frame(ranking_frame, bd=2, relief="groove")
        ranking_tree_frame.pack(pady=10, fill="both", expand=True)

        ranking_columns = ("pos", "usuario", "saldo")
        self.ranking_tree = ttk.Treeview(ranking_tree_frame, columns=ranking_columns, show="headings", style="Prizes.Treeview")
        self.ranking_tree.pack(fill="both", expand=True)

        self.ranking_tree.heading("pos", text="#")
        self.ranking_tree.heading("usuario", text="Usuario")
        self.ranking_tree.heading("saldo", text="Saldo")
        self.ranking_tree.column("pos", anchor="center", width=40)
        self.ranking_tree.column("usuario", anchor="w", width=150)
        self.ranking_tree.column("saldo", anchor="e", width=150)
        
        center_wrapper = tk.Frame(main_container, bg=c["bg"])
        center_wrapper.place(relx=0.5, rely=0.5, anchor="center")

        self.center_content_frame = tk.Frame(center_wrapper, bg=c["frame_bg"], bd=5, relief="sunken")
        self.center_content_frame.pack(padx=20, pady=20)

        title = tk.Label(self.center_content_frame, text=f"🎰 Bienvenido/a, {self.current_username} 🎰", font=("Helvetica", 30, "bold"), bg=c["frame_bg"], fg=c["gold"])
        title.pack(pady=(30, 20), padx=50)
        self.animate_title(title, [c["gold"], c["fg"], "#E6C200"])

        games_frame = tk.Frame(self.center_content_frame, bg=c["frame_bg"])
        games_frame.pack(pady=20, padx=20, ipady=10, ipadx=10)

        tk.Label(games_frame, text="SELECCIONA UN JUEGO", font=("Helvetica", 18, "bold"), bg=c["frame_bg"], fg=c["fg"]).pack(pady=(15, 25))

        game_btn_font = ("Arial", 18, "bold")
        # Botones de juego ahora son dorados con texto oscuro
        RoundButton(games_frame, 320, 75, 8, c["gold"], c["frame_bg"], lambda: self.run_game("Blackjack"), "🎲 Jugar Blackjack", game_btn_font, text_color=c["bg"]).pack(pady=12)
        RoundButton(games_frame, 320, 75, 8, c["gold"], c["frame_bg"], lambda: self.run_game("Ruleta"), "🎡 Jugar Ruleta", game_btn_font, text_color=c["bg"]).pack(pady=12)
        RoundButton(games_frame, 320, 75, 8, c["gold"], c["frame_bg"], lambda: self.run_game("Tragamonedas"), "🎰 Jugar Tragamonedas", game_btn_font, text_color=c["bg"]).pack(pady=12)
        RoundButton(games_frame, 320, 75, 8, c["gold"], c["frame_bg"], lambda: self.run_game("Coinflip"), "🪙 Jugar Cara o Sello", game_btn_font, text_color=c["bg"]).pack(pady=12)

        
        balance_frame = tk.Frame(self.center_content_frame, bg=c["frame_bg"])
        balance_frame.pack(pady=(30, 30))

        # Botón de refresco y saldo ahora son blancos
        refresh_button = tk.Button(balance_frame, text="🔄", font=("Arial", 14, "bold"), bg=c["fg"], fg=c["bg"], command=self.refresh_balance_display, relief="raised", bd=3)
        refresh_button.pack(side="left", padx=(0, 10))

        self.balance_label = tk.Label(balance_frame, text=f"🃏 Saldo: ${self.current_balance:,.0f}".replace(",", "."), font=("Arial", 24, "bold"), fg=c["fg"], bg=c["frame_bg"])
        self.balance_label.pack(side="left")
        
        self.refresh_balance_display()
        self.refresh_ranking_display()

    def show_transfer_window(self):
        c = COLORES[self.current_mode]
        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Transferir Saldo")
        transfer_window.configure(bg=c["bg"])
        transfer_window.grab_set()
        transfer_window.transient(self.root)

        frame = tk.Frame(transfer_window, bg=c["frame_bg"], padx=30, pady=30)
        frame.pack(expand=True, padx=20, pady=20)

        tk.Label(frame, text="Transferir Saldo a otro Usuario", font=("Helvetica", 18, "bold"), bg=c["frame_bg"], fg=c["fg"]).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(frame, text="Seleccionar Usuario:", font=("Arial", 14), bg=c["frame_bg"], fg=c["fg"]).grid(row=1, column=0, sticky="w", pady=5)
        
        other_users = get_all_other_users(self.current_user_id)
        self.users_map = {user['usuario']: user['id_usuario'] for user in other_users}
        user_list = list(self.users_map.keys())
        
        recipient_combo = ttk.Combobox(frame, values=user_list, font=("Arial", 12), state="readonly", width=30)
        recipient_combo.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Monto a Transferir:", font=("Arial", 14), bg=c["frame_bg"], fg=c["fg"]).grid(row=2, column=0, sticky="w", pady=5)
        amount_entry = tk.Entry(frame, font=("Arial", 14), justify="center")
        amount_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Tu Contraseña:", font=("Arial", 14), bg=c["frame_bg"], fg=c["fg"]).grid(row=3, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(frame, font=("Arial", 14), show="*", justify="center")
        password_entry.grid(row=3, column=1, pady=5)

        def confirm_transfer():
            recipient_name = recipient_combo.get()
            password = password_entry.get()
            
            if not recipient_name:
                messagebox.showerror("Error", "Debes seleccionar un usuario destinatario.", parent=transfer_window)
                return
            if not password:
                messagebox.showerror("Error", "Debes ingresar tu contraseña para confirmar.", parent=transfer_window)
                return

            try:
                amount = int(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "El monto debe ser un número positivo.", parent=transfer_window)
                    return
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese un monto válido.", parent=transfer_window)
                return
            
            recipient_id = self.users_map.get(recipient_name)
            
            is_sure = messagebox.askyesno(
                "Confirmar Transferencia", 
                f"¿Transferir ${amount:,.0f} a {recipient_name}?".replace(",", "."),
                parent=transfer_window
            )

            if is_sure:
                success, message = perform_transfer(self.current_user_id, recipient_id, amount, password)
                if success:
                    messagebox.showinfo("Éxito", message, parent=transfer_window)
                    self.refresh_balance_display()
                    self.refresh_ranking_display()
                    transfer_window.destroy()
                else:
                    messagebox.showerror("Error", message, parent=transfer_window)

        tk.Button(frame, text="Confirmar Transferencia", command=confirm_transfer, font=("Arial", 14, "bold"), bg=c["gold"], fg=c["bg"]).grid(row=4, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)

    def open_admin_login(self):
        c = COLORES[self.current_mode]
        admin_login_window = tk.Toplevel(self.root)
        admin_login_window.title("Acceso de Administrador")
        admin_login_window.configure(bg=c["bg"])
        admin_login_window.grab_set()
        frame = tk.Frame(admin_login_window, bg=c["frame_bg"], padx=20, pady=20)
        frame.pack(expand=True, padx=20, pady=20)
        tk.Label(frame, text="Login de Administrador", font=("Helvetica", 18, "bold"), bg=c["frame_bg"], fg=c["fg"]).pack(pady=10)
        tk.Label(frame, text="Usuario:", font=("Arial", 14), bg=c["frame_bg"], fg=c["fg"]).pack()
        user_entry = tk.Entry(frame, font=("Arial", 14))
        user_entry.pack(pady=5)
        tk.Label(frame, text="Contraseña:", font=("Arial", 14), bg=c["frame_bg"], fg=c["fg"]).pack()
        pass_entry = tk.Entry(frame, font=("Arial", 14), show="*")
        pass_entry.pack(pady=5)
        def verify():
            admin_id = authenticate_admin(user_entry.get(), pass_entry.get())
            if admin_id:
                self.current_admin_id = admin_id
                admin_login_window.destroy()
                self.show_candy_exchange_window()
            else:
                messagebox.showerror("Error", "Credenciales de administrador incorrectas.", parent=admin_login_window)
        tk.Button(frame, text="Ingresar", command=verify, font=("Arial", 14, "bold"), bg=c["btn_bg"], fg=c["fg"]).pack(pady=10)
        
        self.root.wait_window(admin_login_window)
        self.refresh_balance_display()


    def show_candy_exchange_window(self):
        c = COLORES[self.current_mode]
        candy_window = tk.Toplevel(self.root)
        candy_window.title("Panel de Administrador - Canjear Dulces")
        candy_window.configure(bg=c["bg"])
        candy_window.grab_set()
        main_frame = tk.Frame(candy_window, bg=c["bg"])
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        tree_frame = tk.Frame(main_frame, bd=2, relief="groove")
        tree_frame.pack(pady=10, fill="both", expand=True)
        columns = ("id", "usuario", "rut", "saldo", "dulces")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("id", width=50, anchor="w")
        tree.column("saldo", anchor="e")
        tree.column("dulces", anchor="center")
        def refresh_tree():
            for i in tree.get_children():
                tree.delete(i)
            for user_data in get_all_users_for_admin():
                tree.insert("", "end", values=user_data)
        refresh_tree()
        exchange_frame = tk.Frame(main_frame, bg=c["frame_bg"], bd=2, relief="ridge", padx=10, pady=10)
        exchange_frame.pack(pady=10, fill="x")
        tk.Label(exchange_frame, text="Opciones de Canje (el usuario gasta saldo para obtener dulces)", font=("Arial", 12, "bold"), bg=c["frame_bg"], fg=c["fg"]).pack()
        
        options = {
            "2 Dulces x $10.000": (10000, 2), 
            "3 Dulces x $15.000": (15000, 3), 
            "4 Dulces x $20.000": (20000, 4), 
            "6 Dulces x $30.000": (30000, 6)
        }

        def on_exchange_click(saldo_cost, dulces_gain):
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Sin Selección", "Por favor, seleccione un usuario de la lista.", parent=candy_window)
                return
            user_id = tree.item(selected_item[0])["values"][0]
            success, message = perform_candy_exchange(self.current_admin_id, user_id, saldo_cost, dulces_gain)
            if success:
                messagebox.showinfo("Éxito", message, parent=candy_window)
                refresh_tree()
                if user_id == self.current_user_id:
                    self.refresh_balance_display()
            else:
                messagebox.showerror("Error", message, parent=candy_window)
        button_panel = tk.Frame(exchange_frame, bg=c["frame_bg"])
        button_panel.pack(pady=5)
        for text, (cost, gain) in options.items():
            tk.Button(button_panel, text=text, font=("Arial", 10), bg=c["btn_bg"], fg=c["fg"], command=lambda c=cost, g=gain: on_exchange_click(c, g)).pack(side="left", padx=5, pady=5)
        tk.Button(exchange_frame, text="Refrescar Lista", command=refresh_tree).pack(pady=5)

    def show_ranking(self):
        c = COLORES[self.current_mode]
        ranking_window = tk.Toplevel(self.root)
        ranking_window.title("🏆 Ranking de jugadores")
        ranking_window.configure(bg=c["bg"])
        ranking_window.grab_set() 
        frame = tk.Frame(ranking_window, bg=c["frame_bg"], bd=5, relief="ridge")
        frame.pack(expand=True, padx=20, pady=20, fill="both")
        title = tk.Label(frame, text="🏆 Ranking por saldo y partidas 🏆", font=("Helvetica", 24, "bold"), bg=c["frame_bg"], fg=c["fg"])
        title.pack(pady=15)
        self.animate_title(title, [c["gold"], c["btn_bg"], c["fg"]])
        tree_frame = tk.Frame(frame, bd=2, relief="groove")
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        columns = ("usuario", "saldo", "ganadas", "perdidas", "empatadas")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        for col in columns:
            tree.heading(col, text=col.capitalize())
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background=c.get("tree_bg", c["frame_bg"]), foreground=c.get("tree_fg", c["fg"]), fieldbackground=c.get("tree_bg", c["frame_bg"]), font=("Arial", 14), rowheight=30)
        style.map('Treeview', background=[('selected', c["btn_bg"])])
        style.configure("Treeview.Heading", background=c.get("tree_heading_bg", c["btn_bg"]), foreground=c.get("tree_heading_fg", c["fg"]), font=("Arial", 16, "bold"))
        
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    u.usuario, 
                    u.saldo,
                    SUM(CASE WHEN h.resultado = 'ganaste' THEN 1 ELSE 0 END) as ganadas,
                    SUM(CASE WHEN h.resultado = 'perdiste' THEN 1 ELSE 0 END) as perdidas,
                    SUM(CASE WHEN h.resultado = 'empate' THEN 1 ELSE 0 END) as empatadas
                FROM usuarios u
                LEFT JOIN historial_partidas h ON u.id_usuario = h.id_usuario
                GROUP BY u.id_usuario, u.usuario, u.saldo
                ORDER BY u.saldo DESC;
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                saldo_formateado = f"${row['saldo']:,.0f}".replace(",", ".")
                tree.insert("", "end", values=(
                    row['usuario'], 
                    saldo_formateado, 
                    row['ganadas'] or 0, 
                    row['perdidas'] or 0, 
                    row['empatadas'] or 0
                ))
        except Exception as e:
            print(f"Error al generar ranking: {e}")
        finally:
            cursor.close()
        
        tk.Button(frame, text="Cerrar", width=20, height=2, bg=c["btn_bg"], fg=c["fg"], activebackground=c["btn_active"], font=("Arial", 16, "bold"), command=ranking_window.destroy).pack(pady=10)
        
        self.root.wait_window(ranking_window)
        self.refresh_balance_display()

    def show_user_history(self):
        c = COLORES[self.current_mode]
        history_window = tk.Toplevel(self.root)
        history_window.title(f"📜 Historial de {self.current_username}")
        history_window.configure(bg=c["bg"])
        history_window.grab_set() 
        frame = tk.Frame(history_window, bg=c["frame_bg"], bd=5, relief="ridge")
        frame.pack(expand=True, padx=20, pady=20, fill="both")
        title = tk.Label(frame, text=f"📜 Historial de apuestas de {self.current_username}", font=("Helvetica", 22, "bold"), bg=c["frame_bg"], fg=c["fg"])
        title.pack(pady=15)
        self.animate_title(title, [c["gold"], c["btn_bg"], c["fg"]])
        tree_frame = tk.Frame(frame, bd=2, relief="groove")
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        columns = ("fecha", "juego", "apuesta", "resultado")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        for col in columns:
            tree.heading(col, text=col.capitalize())
        
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    h.fecha, 
                    j.nombre_juego, 
                    h.apuesta, 
                    h.resultado 
                FROM historial_partidas h
                JOIN juegos j ON h.id_juego = j.id_juego
                WHERE h.id_usuario = %s
                ORDER BY h.fecha DESC;
            """
            cursor.execute(query, (self.current_user_id,))
            for row in cursor.fetchall():
                fecha_dt = row['fecha']
                fecha_str = fecha_dt.strftime('%Y-%m-%d %H:%M:%S') if isinstance(fecha_dt, datetime) else "Fecha no disponible"
                apuesta_formateada = f"${row['apuesta']:,.0f}".replace(",", ".")
                tree.insert("", "end", values=(
                    fecha_str,
                    row['nombre_juego'],
                    apuesta_formateada,
                    row['resultado'].capitalize()
                ))
        except Exception as e:
            print(f"Error al obtener historial: {e}")
        finally:
            cursor.close()

        tk.Button(frame, text="Cerrar", width=20, height=2, bg=c["btn_bg"], fg=c["fg"], activebackground=c["btn_active"], font=("Arial", 16, "bold"), command=history_window.destroy).pack(pady=10)

        self.root.wait_window(history_window)
        self.refresh_balance_display()

    def run_game(self, game="Blackjack"):
        for widget in self.center_content_frame.winfo_children():
            widget.destroy()

        c = COLORES[self.current_mode]
        self.refresh_balance_display()

        self.center_content_frame.config(bd=5, relief="sunken")

        tk.Label(self.center_content_frame, text=f"Saldo disponible: ${self.current_balance:,.0f}".replace(",", "."), font=("Helvetica", 24, "bold"), fg=c["label_fg"], bg=c["frame_bg"]).pack(pady=20)
        tk.Label(self.center_content_frame, text=f"Apuesta para {game}", font=("Helvetica", 20), fg=c["fg"], bg=c["frame_bg"]).pack(pady=10)

        def bet_chosen(amount):
            if amount > self.current_balance:
                messagebox.showerror("Error", "No tienes suficiente saldo para esa apuesta.")
                return
            self._execute_game_logic(game, amount)

        btn_w, btn_h, btn_radius, btn_font = 280, 50, 6, ("Arial", 14, "bold")
        for amount in [100, 200, 500, 1000]:
            if amount <= self.current_balance:
                RoundButton(self.center_content_frame, btn_w, btn_h, btn_radius, c["btn_bg"], c["frame_bg"], command=lambda m=amount: bet_chosen(m), text=f"${amount}", font=btn_font).pack(pady=8)

        def on_other_bet_click():
            def confirm_other():
                try:
                    other_amount = int(other_entry.get())
                    if 1 <= other_amount <= self.current_balance:
                        other_window.destroy()
                        bet_chosen(other_amount)
                    else:
                        messagebox.showerror("Error", "Ingrese un monto válido dentro del saldo disponible.", parent=other_window)
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido.", parent=other_window)

            other_window = tk.Toplevel(self.root)
            other_window.title("Ingrese otro monto")
            other_window.configure(bg=c["bg"])
            other_window.grab_set()
            
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
            other_window.geometry(f'300x200+{x}+{y}')
            
            other_frame = tk.Frame(other_window, bg=c["frame_bg"], padx=20, pady=20)
            other_frame.pack(expand=True, fill='both')
            
            tk.Label(other_frame, text="Ingrese Monto", font=("Helvetica", 14, "bold"), fg=c["fg"], bg=c["frame_bg"]).pack(pady=5)
            other_entry = tk.Entry(other_frame, font=("Helvetica", 14, "bold"))
            other_entry.pack(pady=10)
            tk.Button(other_frame, text="Confirmar", command=confirm_other, font=("Helvetica", 12, "bold"), bg=c["btn_bg"], fg=c["fg"]).pack(pady=10)

        RoundButton(self.center_content_frame, btn_w, btn_h, btn_radius, c["neutral"], c["frame_bg"], on_other_bet_click, "Otro monto", btn_font).pack(pady=8)
        RoundButton(self.center_content_frame, btn_w, btn_h, btn_radius, c["neutral"], c["frame_bg"], self.show_main_menu, "⬅ Volver", btn_font).pack(pady=20)

    def _execute_game_logic(self, game, bet_placed):
        self.root.withdraw()
        final_result_msg = None
        bet_txt_path = resource_path("apuesta.txt")
        result_txt_path = resource_path("resultado.txt")
        
        try:
            open(bet_txt_path, "w").close() 
            open(result_txt_path, "w").close()
        except IOError as e:
            messagebox.showerror("Error de Archivo", f"No se pudieron preparar archivos temporales: {e}")
            self.root.deiconify()
            self.show_main_menu()
            return

        try:
            with open(bet_txt_path, "w") as f:
                f.write(str(bet_placed))
            
            if game == "Tragamonedas":
                slot_root = tk.Toplevel()
                tragamonedas.SlotMachineController(slot_root)
                self.root.wait_window(slot_root)
            elif game == "Ruleta": ruleta.juego_ruleta()
            elif game == "Blackjack": blackjack.juego_blackjack()
            elif game == "Coinflip": coinflip.juego_coinflip()

            
            if not os.path.exists(result_txt_path):
                final_result_msg = f"No se encontró el archivo de resultado para {game}."
            else:
                with open(result_txt_path, "r") as f:
                    result_str = f.read().strip()
                history_result = ""
                if game in ["Blackjack", "Ruleta", "Coinflip"]:
                    history_result = result_str.lower()
                    if history_result == "ganaste":
                        winnings = bet_placed * 1 
                        self.current_balance += winnings
                        final_result_msg = f"¡Ganaste ${winnings:,.0f}! 🎉".replace(",", ".")
                    elif history_result == "perdiste":
                        self.current_balance -= bet_placed
                        final_result_msg = f"Perdiste ${bet_placed:,.0f} 😞".replace(",", ".")
                    else: # Empate
                        final_result_msg = "Empate. No hay cambios en el saldo."
                elif game == "Tragamonedas":
                    try:
                        gross_winnings = int(result_str)
                        if gross_winnings == -1:
                            final_result_msg = "Juego cancelado, no se realizó ninguna apuesta."
                        else:
                            net_change = gross_winnings - bet_placed
                            self.current_balance += net_change
                            if net_change > 0:
                                final_result_msg, history_result = f"¡Ganaste un total de ${net_change:,.0f}! 🎉".replace(",", "."), "ganaste"
                            elif net_change < 0:
                                final_result_msg, history_result = f"Perdiste ${abs(net_change):,.0f} 😞".replace(",", "."), "perdiste"
                            else:
                                final_result_msg, history_result = "Recuperaste tu apuesta.", "empate"
                    except (ValueError, TypeError):
                        final_result_msg = f"Resultado inválido de Tragamonedas: '{result_str}'"
                if history_result:
                    add_history(self.current_user_id, bet_placed, history_result, game)
                update_balance(self.current_user_id, self.current_balance)
        except Exception as e:
            messagebox.showerror("Error en el juego", f"Un error ocurrió al ejecutar {game}: {e}")
        finally:
            self.root.deiconify()
            if not pygame.mixer.get_init(): pygame.mixer.init()
            try:
                 pygame.mixer.music.load(resource_path("musica_ambiente.mp3"))
                 pygame.mixer.music.set_volume(0.15)
                 pygame.mixer.music.play(-1)
            except Exception as e:
                 print(f"Error al recargar música ambiente: {e}")
            
            self.show_main_menu()
            self.refresh_balance_display()
            self.refresh_ranking_display()
            
            if final_result_msg:
                messagebox.showinfo("Resultado", final_result_msg)

    def logout(self):
        self.current_user_id = None
        self.current_username = None
        self.current_balance = 0
        self.show_start_screen()

    def clear_window(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CasinoApp(root)
    root.mainloop()
