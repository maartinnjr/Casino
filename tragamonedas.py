import random
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import pygame
from collections import Counter

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ----------------------------- MODELO -----------------------------
class SlotMachine:
    def __init__(self):
        self.multipliers = {
            "🍇": 3, "🍒": 4, "🍋": 5,
            "🍊": 6, "🍉": 8, "🍓": 10
        }
        self.symbols = list(self.multipliers.keys())
        self.result = ["❓", "❓", "❓"]

    def spin(self):
        self.result = [random.choice(self.symbols) for _ in range(3)]

    def calculate_winnings(self, bet, chosen_fruit):
        counts = Counter(self.result)
        
        if 3 in counts.values():
            fruit = [k for k, v in counts.items() if v == 3][0]
            multiplier = self.multipliers.get(fruit, 0)
            ganancia_neta = (bet * multiplier) - bet
            return ganancia_neta, f"¡Trío de {fruit}! x{multiplier}"
        
        elif counts[chosen_fruit] == 2:
            ganancia_neta = bet 
            return ganancia_neta, f"¡Par de {chosen_fruit}! Ganas x2"

        elif counts[chosen_fruit] == 1:
            ganancia_neta = 0
            return ganancia_neta, f"¡Una {chosen_fruit}!\nRecuperas tu apuesta"

        else:
            ganancia_neta = -bet
            return ganancia_neta, "Perdiste"

# ----------------------------- VISTA -----------------------------
class SlotMachineView:
    def __init__(self, root, controller, bet_amount):
        self.controller = controller
        self.root = root
        self.bet_amount = bet_amount
        self.root.title("Tragamonedas")
        self.root.attributes("-fullscreen", True)
        
        self.setup_background()

        self.main_container = tk.Frame(self.root, bg="#111111")
        self.main_container.config(bg=self.main_container.master.cget('bg'))
        self.main_container.pack(pady=20, padx=20, expand=True)

        self.game_frame = tk.Frame(self.main_container, bg="#1c1c1c", bd=20, relief="ridge", padx=30, pady=30)
        self.game_frame.pack(side="left", padx=20)

        self.prizes_frame = tk.Frame(self.main_container, bg="#1c1c1c", bd=10, relief="ridge", padx=20, pady=20)
        self.prizes_frame.pack(side="left", padx=20, fill="y")
        
        self.setup_game_ui()
        self.setup_prizes_ui()

    def setup_background(self):
        try:
            image_path = resource_path("fondotragamonedas.jpg")
            img = Image.open(image_path)
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            img = img.resize((w, h), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)
            background_label = tk.Label(self.root, image=self.bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"No se pudo cargar el fondo: {e}")
            self.root.configure(bg="#111111")

    def setup_game_ui(self):
        self.bet_label = tk.Label(self.game_frame, text=f"Tu Apuesta: ${self.bet_amount}",
                                  font=("Arial", 24, "bold"), fg="#FFD700", bg="#1c1c1c")
        self.bet_label.pack(pady=10)

        self.reel_frame = tk.Frame(self.game_frame, bg="#1c1c1c", bd=10, relief="ridge", pady=10)
        self.reel_frame.pack(pady=20)
        self.reel_labels = [
            tk.Label(self.reel_frame, text="❓", font=("Arial", 60, "bold"),
                     bg="#e74c3c", fg="white", width=5, height=2, relief="raised", bd=5)
            for _ in range(3)
        ]
        for label in self.reel_labels:
            label.pack(side="left", padx=15)

        tk.Label(self.game_frame, text="Elige tu fruta de la suerte:", font=("Arial", 18),
                 fg="#FFD700", bg="#1c1c1c").pack(pady=(20, 5))
        
        fruit_frame = tk.Frame(self.game_frame, bg="#1c1c1c")
        fruit_frame.pack(pady=10)
        self.fruit_buttons = {}
        for fruit in self.controller.get_symbols():
            btn = tk.Button(fruit_frame, text=fruit, font=("Arial", 30),
                            command=lambda f=fruit: self.controller.select_fruit(f),
                            bg="#555555", fg="white", relief="raised", bd=3, cursor="hand2")
            btn.pack(side="left", padx=5)
            self.fruit_buttons[fruit] = btn

        self.info_label = tk.Label(self.game_frame, text="Presiona ESPACIO para girar o ESC para salir",
                                   font=("Arial", 16), fg="white", bg="#1c1c1c")
        self.info_label.pack(pady=20)

        self.root.bind("<space>", lambda e: self.controller.play())
        self.root.bind("<Escape>", lambda e: self.controller.salir())

    def setup_prizes_ui(self):
        tk.Label(self.prizes_frame, text="Tabla de Premios", font=("Arial", 22, "bold", "underline"),
                 fg="#FFD700", bg="#1c1c1c").pack(pady=(0, 15))
        
        multipliers = self.controller.get_multipliers()
        
        tk.Label(self.prizes_frame, text="Trío de cualquier fruta:", font=("Arial", 18, "bold"),
                 fg="#FFD700", bg="#1c1c1c").pack(anchor="w", pady=(10,0))
        for fruit, mult in sorted(multipliers.items(), key=lambda item: item[1]):
            prize_text = f"   {fruit}{fruit}{fruit}   »  Ganas x{mult}"
            tk.Label(self.prizes_frame, text=prize_text, font=("Arial", 16),
                     fg="white", bg="#1c1c1c").pack(anchor="w")
            
        tk.Label(self.prizes_frame, text="\nPar de tu fruta elegida:", font=("Arial", 18, "bold"),
                 fg="white", bg="#1c1c1c").pack(anchor="w", pady=5)
        tk.Label(self.prizes_frame, text="   (ej: 🍓🍓❓)  »  Ganas x2", font=("Arial", 16),
                 fg="white", bg="#1c1c1c").pack(anchor="w")

        tk.Label(self.prizes_frame, text="\n1 de tu fruta elegida:", font=("Arial", 18, "bold"),
                 fg="white", bg="#1c1c1c").pack(anchor="w", pady=5)
        tk.Label(self.prizes_frame, text="   (ej: 🍓❓❓)  »  Recuperas apuesta", font=("Arial", 16),
                 fg="white", bg="#1c1c1c").pack(anchor="w")


    def highlight_selected_fruit(self, selected_fruit):
        for fruit, button in self.fruit_buttons.items():
            if fruit == selected_fruit:
                button.config(relief="sunken", bg="#FFD700", fg="black")
            else:
                button.config(relief="raised", bg="#555555", fg="white")

    def animate_reels(self, final_result, sound_stop):
        symbols = self.controller.get_symbols()
        for _ in range(10):
            for i in range(3):
                self.reel_labels[i].config(text=random.choice(symbols), fg="white")
            self.root.update()
            time.sleep(0.05)
        for _ in range(10):
            for i in range(3):
                self.reel_labels[i].config(text=random.choice(symbols), fg="white")
            self.root.update()
            time.sleep(0.1)
        self.reel_labels[0].config(text=final_result[0], fg="#FFD700")
        if sound_stop: sound_stop.play()
        self.root.update()
        for _ in range(10):
            for i in range(1, 3):
                self.reel_labels[i].config(text=random.choice(symbols), fg="white")
            self.root.update()
            time.sleep(0.15)
        self.reel_labels[1].config(text=final_result[1], fg="#FFD700")
        if sound_stop: sound_stop.play()
        self.root.update()
        for _ in range(10):
            self.reel_labels[2].config(text=random.choice(symbols), fg="white")
            self.root.update()
            time.sleep(0.25)
        self.reel_labels[2].config(text=final_result[2], fg="#FFD700")
        if sound_stop: sound_stop.play()
        self.root.update()

    def show_final_screen(self, message, net_winnings):
        self.root.after(1500, lambda: self.create_result_dialog(message, net_winnings))

    def create_result_dialog(self, message, net_winnings):
        dialog = tk.Toplevel(self.root)
        dialog.overrideredirect(True)
        dialog.config(bg="black")
        
        dialog.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        dialog.grab_set()

        result_box = tk.Frame(dialog, bg="#141414", bd=3, relief="ridge", highlightbackground="#D4AF37", highlightthickness=3)
        result_box.place(relx=0.5, rely=0.5, anchor="center")

        if net_winnings > 0:
            color = "#FFD700"
            final_message_text = f"{message}\n¡Ganaste ${net_winnings:,.0f}!".replace(",",".")
        elif net_winnings == 0:
            color = "white"
            final_message_text = f"{message}\nRecuperaste tu apuesta."
        else:
            color = "#E53935"
            final_message_text = f"{message}\nPerdiste ${abs(net_winnings):,.0f}.".replace(",",".")

        final_message_label = tk.Label(result_box, text=final_message_text, font=("Arial", 32, "bold"),
                                       fg=color, bg="#141414", wraplength=500, justify="center", padx=40, pady=20)
        final_message_label.pack(pady=(20, 10))

        volver_btn = tk.Button(result_box, text="Volver al casino",
                               font=("Arial", 22, "bold"), bg="#C41E3A", fg="white",
                               activebackground="#FF6347", relief="raised", bd=5,
                               padx=20, pady=10, cursor="hand2", command=self.controller.salir)
        volver_btn.pack(pady=(10, 30))

# ----------------------------- CONTROLADOR -----------------------------
class SlotMachineController:
    def __init__(self, root):
        self.model = SlotMachine()
        
        try:
            apuesta_txt_path = resource_path("apuesta.txt")
            with open(apuesta_txt_path, "r") as f:
                self.bet_amount = int(f.read().strip())
        except (IOError, ValueError):
            self.bet_amount = 10 

        self.view = SlotMachineView(root, self, self.bet_amount)
        self.view.root.protocol("WM_DELETE_WINDOW", self.salir)
        
        self.selected_fruit = None
        self.net_winnings = 0
        self.game_played = False
        
        pygame.mixer.init()
        self.sound_win_fruit = self._load_sound("winfruit.wav")
        self.sound_lose = self._load_sound("lose.wav")
        self.sound_stop = self._load_sound("fruit.wav")
        self.sound_strawberry_win = self._load_sound("winstrawberry.wav")
        self.sound_tie = self._load_sound("win.wav")

    def _load_sound(self, filename):
        try:
            path = resource_path(os.path.join("sounds", filename))
            return pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Error al cargar el sonido '{filename}': {e}")
            return None

    def get_symbols(self):
        return self.model.symbols
    
    def get_multipliers(self):
        return self.model.multipliers

    def select_fruit(self, fruit):
        if not self.game_played:
            self.selected_fruit = fruit
            self.view.highlight_selected_fruit(fruit)

    def play(self):
        if self.game_played:
            return
        
        if self.selected_fruit is None:
            messagebox.showwarning("Falta Selección", "Por favor, elige una fruta antes de girar.")
            return
        
        self.game_played = True
        self.view.root.unbind("<space>")
        self.view.info_label.config(text="¡Mucha suerte!")

        self.model.spin()
        self.view.animate_reels(self.model.result, self.sound_stop)
        
        net_winnings, message = self.model.calculate_winnings(self.bet_amount, self.selected_fruit)
        self.net_winnings = net_winnings

        if self.model.result == ["🍓", "🍓", "🍓"]:
            if self.sound_strawberry_win:
                self.sound_strawberry_win.play()
        elif net_winnings > 0:
            if self.sound_win_fruit:
                self.sound_win_fruit.play()
        elif net_winnings == 0:
            if self.sound_tie:
                self.sound_tie.play()
        else:
            if self.sound_lose:
                self.sound_lose.play()

        self.view.show_final_screen(message, self.net_winnings)

    def salir(self):
        # --- INICIO: LÓGICA CORREGIDA ---
        if not self.game_played:
            # Si el juego no se ha jugado, el resultado es -1 para indicar cancelación.
            resultado_final_para_archivo = -1
        else:
            # Si se jugó, se calcula la ganancia bruta normalmente.
            ganancia_bruta = self.net_winnings + self.bet_amount
            resultado_final_para_archivo = ganancia_bruta
        # --- FIN: LÓGICA CORREGIDA ---

        resultado_txt_path = resource_path("resultado.txt")
        with open(resultado_txt_path, "w") as f:
            f.write(str(resultado_final_para_archivo))

        self.view.root.destroy()

# ----------------------------- EJECUCIÓN -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineController(root)
    root.mainloop()
