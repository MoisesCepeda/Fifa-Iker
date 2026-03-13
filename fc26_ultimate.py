import tkinter as tk
from tkinter import messagebox
import random
import os
import winsound
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

# =========================================================
# RUTAS
# =========================================================
BASE_DIR = r"C:\Users\cepedm2\Desktop\interface fifa"
RUTA_FONDO = os.path.join(BASE_DIR, "imagen.jpg")
RUTA_LOGOS = os.path.join(BASE_DIR, "equipos")
RUTA_SONIDOS = os.path.join(BASE_DIR, "sounds")

SONIDO_RULETA = os.path.join(RUTA_SONIDOS, "roulette.wav")
SONIDO_REVELAR = os.path.join(RUTA_SONIDOS, "reveal.wav")
SONIDO_INICIO = os.path.join(RUTA_SONIDOS, "start.wav")

# =========================================================
# VENTANA
# =========================================================
ANCHO = 1450
ALTO = 860

# =========================================================
# DATOS
# =========================================================
equipos = [
    "Bayern Munich Classic XI",
    "Bundesliga Classic XI",
    "Chelsea Classic XI",
    "Classics Eleven",
    "Juventus Classic XI",
    "La Liga Classic XI",
    "Ligue 1 Classic XI",
    "Liverpool Classic XI",
    "Premier League Classic XI",
    "Real Madrid Classic XI",
    "Serie A Classic XI",
    "Soccer Aid",
    "Zlatan FC"
]

modos_juego = [
    "RUSH",
    "NORMAL",
    "SE VALE TODO",
    "BALÓN MISTERIOSO"
]

logos = {
    "Bayern Munich Classic XI": "bayern.png",
    "Bundesliga Classic XI": "bundesliga.png",
    "Chelsea Classic XI": "chelsea.png",
    "Classics Eleven": "classics.png",
    "Juventus Classic XI": "juventus.png",
    "La Liga Classic XI": "laliga.png",
    "Ligue 1 Classic XI": "ligue1.png",
    "Liverpool Classic XI": "liverpool.png",
    "Premier League Classic XI": "premier.png",
    "Real Madrid Classic XI": "realmadrid.png",
    "Serie A Classic XI": "seriea.png",
    "Soccer Aid": "socceraid.png",
    "Zlatan FC": "zlatan.png"
}

# =========================================================
# ESTADO
# =========================================================
equipo_iker = None
equipo_moy = None
modo_partido = None

logo_iker_img = None
logo_moy_img = None
logo_grande_img = None
bg_img = None

beam_items = []
smoke_items = []
overlay_lines = []
overlay_rects = []
luces_ids = []

animacion_luces_activa = True
animacion_humo_activa = True
animacion_beams_activa = True

# =========================================================
# COLORES
# =========================================================
COLOR_BG_PANEL = "#0c0f12"
COLOR_PANEL = "#11161b"
COLOR_VERDE = "#d8ff2d"
COLOR_CYAN = "#00e6ff"
COLOR_DORADO = "#ffd54a"
COLOR_TEXTO = "#f4f7fb"
COLOR_SUB = "#9aa7b3"
COLOR_BORDE = "#25303b"
COLOR_FONDO = "#0a0d10"

# =========================================================
# SONIDO
# =========================================================
def reproducir_sonido(ruta, async_mode=True):
    try:
        if os.path.exists(ruta):
            flags = winsound.SND_FILENAME
            if async_mode:
                flags |= winsound.SND_ASYNC
            winsound.PlaySound(ruta, flags)
    except:
        pass

def detener_sonido():
    try:
        winsound.PlaySound(None, 0)
    except:
        pass

# =========================================================
# LOGOS
# =========================================================
def cargar_logo(equipo, tam=(180, 180)):
    if equipo not in logos:
        return None

    ruta_logo = os.path.join(RUTA_LOGOS, logos[equipo])
    if not os.path.exists(ruta_logo):
        return None

    try:
        img = Image.open(ruta_logo).convert("RGBA")
        img = img.resize(tam, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except:
        return None

def mostrar_logo_iker(equipo):
    global logo_iker_img
    logo_iker_img = cargar_logo(equipo, tam=(180, 180))
    if logo_iker_img:
        lbl_logo_iker.config(image=logo_iker_img, text="")
    else:
        lbl_logo_iker.config(image="", text="SIN LOGO", fg=COLOR_SUB)

def mostrar_logo_moy(equipo):
    global logo_moy_img
    logo_moy_img = cargar_logo(equipo, tam=(180, 180))
    if logo_moy_img:
        lbl_logo_moy.config(image=logo_moy_img, text="")
    else:
        lbl_logo_moy.config(image="", text="SIN LOGO", fg=COLOR_SUB)

def mostrar_logo_grande(equipo):
    global logo_grande_img

    if equipo not in logos:
        return

    ruta_logo = os.path.join(RUTA_LOGOS, logos[equipo])
    if not os.path.exists(ruta_logo):
        return

    try:
        img = Image.open(ruta_logo).convert("RGBA")
        img = img.resize((300, 300), Image.LANCZOS)
        logo_grande_img = ImageTk.PhotoImage(img)

        logo_reveal.config(image=logo_grande_img, text="")
        logo_reveal.place(relx=0.5, rely=0.47, anchor="center")
        texto_reveal.config(text=equipo)
        texto_reveal.place(relx=0.5, rely=0.72, anchor="center")

        root.after(1400, ocultar_logo_grande)
    except:
        pass

def ocultar_logo_grande():
    logo_reveal.place_forget()
    texto_reveal.place_forget()

# =========================================================
# FONDO
# =========================================================
def cargar_fondo_en_canvas():
    global bg_img

    if os.path.exists(RUTA_FONDO):
        print("FONDO ENCONTRADO:", RUTA_FONDO)
        fondo = Image.open(RUTA_FONDO).convert("RGBA")
        fondo = fondo.resize((ANCHO, ALTO), Image.LANCZOS)
        fondo = ImageEnhance.Brightness(fondo).enhance(0.58)
        fondo = fondo.filter(ImageFilter.GaussianBlur(radius=0.15))
        bg_img = ImageTk.PhotoImage(fondo)
        canvas_fx.create_image(0, 0, image=bg_img, anchor="nw")
    else:
        print("NO SE ENCONTRÓ EL FONDO:", RUTA_FONDO)
        canvas_fx.create_rectangle(0, 0, ANCHO, ALTO, fill=COLOR_FONDO, outline="")

# =========================================================
# LUCES SUPERIORES
# =========================================================
intensidad_luz = 0
direccion_luz = 1

def crear_luces_estadio():
    global luces_ids
    luces_ids.clear()

    posiciones = [
        (110, 60), (250, 45), (390, 35), (530, 28), (690, 24),
        (860, 28), (1010, 35), (1150, 45), (1290, 60)
    ]

    for x, y in posiciones:
        halo = canvas_fx.create_oval(x - 45, y - 45, x + 45, y + 45, fill="", outline="")
        foco = canvas_fx.create_oval(x - 12, y - 12, x + 12, y + 12, fill="#ffffff", outline="")
        luces_ids.append((halo, foco))

def animar_luces_estadio():
    global intensidad_luz, direccion_luz

    if not animacion_luces_activa:
        return

    intensidad_luz += direccion_luz * 8
    if intensidad_luz >= 140:
        intensidad_luz = 140
        direccion_luz = -1
    elif intensidad_luz <= 25:
        intensidad_luz = 25
        direccion_luz = 1

    tono_verde = min(255, 120 + intensidad_luz)
    tono_azul = min(255, 160 + intensidad_luz // 2)
    halo_color = f"#{20:02x}{tono_verde:02x}{tono_azul:02x}"

    for i, (halo, foco) in enumerate(luces_ids):
        radio_extra = (i % 3) * 6
        x1, y1, x2, y2 = canvas_fx.coords(halo)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        r = 34 + radio_extra + intensidad_luz // 20
        canvas_fx.coords(halo, cx - r, cy - r, cx + r, cy + r)
        canvas_fx.itemconfig(halo, fill=halo_color, outline="", stipple="gray50")
        canvas_fx.itemconfig(foco, fill="#f8fff0", outline="")

    root.after(90, animar_luces_estadio)

# =========================================================
# LUCES MÓVILES ESTILO CHAMPIONS
# =========================================================
def crear_beams():
    global beam_items
    beam_items.clear()

    for i in range(6):
        x = 120 + i * 220
        item = canvas_fx.create_polygon(
            x, 130,
            x + 70, 130,
            x + 180, 760,
            x - 90, 760,
            fill="#1ffff0",
            outline="",
            stipple="gray50"
        )
        beam_items.append({
            "id": item,
            "x": x,
            "vel": random.choice([-3, -2, 2, 3]),
            "ancho": random.randint(50, 85)
        })

def animar_beams():
    if not animacion_beams_activa:
        return

    for beam in beam_items:
        beam["x"] += beam["vel"]

        if beam["x"] < 40 or beam["x"] > ANCHO - 40:
            beam["vel"] *= -1

        x = beam["x"]
        a = beam["ancho"]
        canvas_fx.coords(
            beam["id"],
            x, 120,
            x + a, 120,
            x + a + 90, 760,
            x - 90, 760
        )

    root.after(45, animar_beams)

# =========================================================
# HUMO DE ESTADIO
# =========================================================
def crear_humo():
    global smoke_items
    smoke_items.clear()

    for _ in range(16):
        x = random.randint(0, ANCHO)
        y = random.randint(520, 850)
        r = random.randint(40, 90)
        item = canvas_fx.create_oval(
            x - r, y - r, x + r, y + r,
            fill="#d7d7d7",
            outline="",
            stipple="gray25"
        )
        smoke_items.append({
            "id": item,
            "x": x,
            "y": y,
            "r": r,
            "dx": random.choice([-1, 1]) * random.uniform(0.3, 1.2),
            "dy": random.uniform(-0.8, -0.2)
        })

def animar_humo():
    if not animacion_humo_activa:
        return

    for humo in smoke_items:
        humo["x"] += humo["dx"]
        humo["y"] += humo["dy"]

        if humo["y"] < 420:
            humo["x"] = random.randint(0, ANCHO)
            humo["y"] = random.randint(760, 900)

        x = humo["x"]
        y = humo["y"]
        r = humo["r"]
        canvas_fx.coords(humo["id"], x - r, y - r, x + r, y + r)

    root.after(70, animar_humo)

# =========================================================
# TÚNEL DE ESTADIO
# =========================================================
def crear_tunel_visual():
    global overlay_lines, overlay_rects
    overlay_lines.clear()
    overlay_rects.clear()

    for i in range(12):
        line = canvas_tunel.create_line(0, 0, 0, 0, fill="#d8ff2d", width=3)
        overlay_lines.append(line)

    for i in range(6):
        rect = canvas_tunel.create_rectangle(0, 0, 0, 0, fill="#00d9ff", outline="", stipple="gray50")
        overlay_rects.append(rect)

def animacion_tunel(callback_final=None):
    overlay_tunel.place(x=0, y=0, relwidth=1, relheight=1)
    overlay_tunel.lift()

    pasos = 26

    def frame(i):
        if i < pasos:
            canvas_tunel.delete("texto")

            centro_x = ANCHO // 2
            centro_y = ALTO // 2 + 40
            apertura = 40 + i * 22

            for idx, line in enumerate(overlay_lines):
                factor = idx + 1
                offset = factor * apertura * 0.14

                canvas_tunel.coords(
                    line,
                    centro_x - offset, centro_y - offset,
                    140 + idx * 10, 110 + idx * 18,
                )

            for idx, line in enumerate(overlay_lines):
                factor = idx + 1
                offset = factor * apertura * 0.14
                canvas_tunel.coords(
                    line,
                    centro_x + offset, centro_y - offset,
                    ANCHO - 140 - idx * 10, 110 + idx * 18
                )

            for idx, rect in enumerate(overlay_rects):
                m = idx * 35
                canvas_tunel.coords(
                    rect,
                    180 + m, 90 + m,
                    ANCHO - 180 - m, 110 + m
                )

            canvas_tunel.create_text(
                centro_x, 180,
                text="ENTRANDO AL ESTADIO",
                fill="white",
                font=("Arial", 28, "bold"),
                tags="texto"
            )

            root.after(55, frame, i + 1)
        else:
            overlay_tunel.place_forget()
            if callback_final:
                callback_final()

    frame(0)

# =========================================================
# FUNCIONES DEL JUEGO
# =========================================================
def reiniciar():
    global equipo_iker, equipo_moy, modo_partido
    detener_sonido()

    equipo_iker = None
    equipo_moy = None
    modo_partido = None

    lbl_equipo_iker.config(text="---")
    lbl_equipo_moy.config(text="---")
    lbl_modo_global.config(text="---")

    lbl_logo_iker.config(image="", text="")
    lbl_logo_moy.config(image="", text="")

    barra_iker["value"] = 0
    barra_moy["value"] = 0

    overlay_frame.place_forget()
    overlay_tunel.place_forget()
    countdown_label.place_forget()
    ocultar_logo_grande()

def sortear_modo():
    global modo_partido
    modo_partido = random.choice(modos_juego)
    lbl_modo_global.config(text=modo_partido)

def sortear_iker():
    global equipo_iker
    disponibles = equipos.copy()

    if equipo_moy in disponibles:
        disponibles.remove(equipo_moy)

    if not disponibles:
        messagebox.showwarning("Aviso", "No hay equipos disponibles para IKER.")
        return

    equipo_iker = random.choice(disponibles)
    lbl_equipo_iker.config(text=equipo_iker)
    mostrar_logo_iker(equipo_iker)

def sortear_moy():
    global equipo_moy
    disponibles = equipos.copy()

    if equipo_iker in disponibles:
        disponibles.remove(equipo_iker)

    if not disponibles:
        messagebox.showwarning("Aviso", "No hay equipos disponibles para MOY.")
        return

    equipo_moy = random.choice(disponibles)
    lbl_equipo_moy.config(text=equipo_moy)
    mostrar_logo_moy(equipo_moy)

# =========================================================
# PACK OPENING
# =========================================================
def animacion_pack_opening(callback_final=None):
    overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
    overlay_frame.lift()
    overlay_text.lift()

    frases = [
        "ULTIMATE TEAM DRAFT",
        "GENERANDO PARTIDO",
        "ABRIENDO SOBRE",
        "REVELANDO CLUBES"
    ]

    fondos = ["#101418", "#0e1710", "#0f1116", "#1c2410", "#111111", "#d8ff2d"]
    pasos = 18

    def paso(i):
        if i < pasos:
            color = fondos[i % len(fondos)]
            fg = "#000000" if color == "#d8ff2d" else "#ffffff"
            overlay_frame.config(bg=color)
            overlay_text.config(text=frases[i % len(frases)], bg=color, fg=fg)
            root.after(75, paso, i + 1)
        else:
            overlay_frame.place_forget()
            if callback_final:
                callback_final()

    paso(0)

# =========================================================
# CUENTA REGRESIVA
# =========================================================
def countdown_kickoff():
    countdown_label.place(relx=0.5, rely=0.5, anchor="center")
    secuencia = ["3", "2", "1", "Golizaa!! ⚽"]

    def mostrar(i):
        if i < len(secuencia):
            texto = secuencia[i]
            color = COLOR_VERDE if i < 3 else "#ffffff"
            size = 92 if i < 3 else 56
            countdown_label.config(text=texto, fg=color, font=("Arial", size, "bold"))
            root.after(700 if i < 3 else 950, mostrar, i + 1)
        else:
            countdown_label.place_forget()

    mostrar(0)

# =========================================================
# RULETA
# =========================================================
def animar_ruleta():
    global equipo_iker, equipo_moy, modo_partido

    if len(equipos) < 2:
        messagebox.showwarning("Aviso", "Debe haber al menos 2 equipos.")
        return

    reproducir_sonido(SONIDO_RULETA, async_mode=True)
    vueltas = 30

    def paso(i):
        if i < vueltas:
            e1 = random.choice(equipos)
            e2 = random.choice(equipos)

            while e2 == e1 and len(equipos) > 1:
                e2 = random.choice(equipos)

            modo_temp = random.choice(modos_juego)

            lbl_equipo_iker.config(text=e1)
            lbl_equipo_moy.config(text=e2)
            lbl_modo_global.config(text=modo_temp)

            mostrar_logo_iker(e1)
            mostrar_logo_moy(e2)

            barra_iker["value"] = ((i + 1) / vueltas) * 100
            barra_moy["value"] = ((i + 1) / vueltas) * 100

            root.after(85, paso, i + 1)
        else:
            detener_sonido()

            seleccionados = random.sample(equipos, 2)
            equipo_iker = seleccionados[0]
            equipo_moy = seleccionados[1]
            modo_partido = random.choice(modos_juego)

            lbl_equipo_iker.config(text=equipo_iker)
            lbl_equipo_moy.config(text=equipo_moy)
            lbl_modo_global.config(text=modo_partido)

            mostrar_logo_iker(equipo_iker)
            mostrar_logo_moy(equipo_moy)

            barra_iker["value"] = 100
            barra_moy["value"] = 100

            reproducir_sonido(SONIDO_REVELAR, async_mode=True)
            mostrar_logo_grande(random.choice([equipo_iker, equipo_moy]))
            countdown_kickoff()

    paso(0)

def iniciar_partido():
    reproducir_sonido(SONIDO_INICIO, async_mode=True)
    animacion_tunel(callback_final=lambda: animacion_pack_opening(callback_final=animar_ruleta))

# =========================================================
# BARRA VISUAL
# =========================================================
class BarraFC(tk.Canvas):
    def __init__(self, master, width=220, height=12, **kwargs):
        super().__init__(master, width=width, height=height, bg=COLOR_PANEL, highlightthickness=0, **kwargs)
        self.w = width
        self.h = height
        self.fondo = self.create_rectangle(0, 0, width, height, fill="#202a34", outline="")
        self.relleno = self.create_rectangle(0, 0, 0, height, fill=COLOR_VERDE, outline="")
        self.brillo = self.create_rectangle(0, 0, 0, height, fill="#f2ff9c", outline="", stipple="gray50")
        self._value = 0

    def __setitem__(self, key, value):
        if key == "value":
            self.set_value(value)

    def set_value(self, value):
        self._value = max(0, min(100, value))
        ancho = self.w * (self._value / 100)
        self.coords(self.relleno, 0, 0, ancho, self.h)
        self.coords(self.brillo, max(0, ancho - 22), 0, ancho, self.h)

# =========================================================
# UI
# =========================================================
root = tk.Tk()
root.title("FC26 Ultimate Random")
root.geometry(f"{ANCHO}x{ALTO}")
root.resizable(False, False)
root.configure(bg=COLOR_FONDO)

# Canvas principal
canvas_fx = tk.Canvas(root, width=ANCHO, height=ALTO, highlightthickness=0, bd=0)
canvas_fx.place(x=0, y=0)

# Fondo y efectos
cargar_fondo_en_canvas()
crear_beams()
crear_humo()
crear_luces_estadio()

canvas_fx.create_line(130, 120, 1320, 120, fill="#2e3b46", width=2)
canvas_fx.create_line(130, 670, 1320, 670, fill="#2e3b46", width=2)
canvas_fx.create_line(100, 170, 100, 630, fill="#1c252d", width=3)
canvas_fx.create_line(1350, 170, 1350, 630, fill="#1c252d", width=3)

# Título
titulo = tk.Label(
    root,
    text="FC26 ULTIMATE RANDOM MATCH",
    font=("Arial", 28, "bold"),
    fg=COLOR_VERDE,
    bg="#0d1013"
)
titulo.place(x=330, y=28)

subtitulo = tk.Label(
    root,
    text="IKER vs MOY · MODO DRAFT",
    font=("Arial", 12, "bold"),
    fg=COLOR_SUB,
    bg="#0d1013"
)
subtitulo.place(x=602, y=72)

# Panel IKER
panel_iker = tk.Frame(root, bg=COLOR_PANEL, bd=0, highlightbackground=COLOR_BORDE, highlightthickness=1)
panel_iker.place(x=110, y=150, width=360, height=430)

tag_iker = tk.Label(panel_iker, text="JUGADOR 1", font=("Arial", 10, "bold"), fg=COLOR_SUB, bg=COLOR_PANEL)
tag_iker.place(x=20, y=12)

lbl_nombre_iker = tk.Label(panel_iker, text="IKER", font=("Arial", 20, "bold"), fg=COLOR_CYAN, bg=COLOR_PANEL)
lbl_nombre_iker.place(x=20, y=34)

lbl_logo_iker = tk.Label(panel_iker, bg=COLOR_PANEL, text="")
lbl_logo_iker.place(x=90, y=80)

lbl_equipo_iker = tk.Label(
    panel_iker,
    text="---",
    font=("Arial", 18, "bold"),
    fg=COLOR_TEXTO,
    bg=COLOR_PANEL,
    wraplength=300,
    justify="center"
)
lbl_equipo_iker.place(x=28, y=280, width=300)

barra_iker = BarraFC(panel_iker, width=260, height=12)
barra_iker.place(x=48, y=346)

btn_iker = tk.Button(
    panel_iker,
    text="SORTEAR IKER",
    font=("Arial", 11, "bold"),
    bg="#202831",
    fg="#ffffff",
    activebackground="#27313c",
    activeforeground="#ffffff",
    relief="flat",
    width=18,
    command=sortear_iker
)
btn_iker.place(x=100, y=378)

# Panel MOY
panel_moy = tk.Frame(root, bg=COLOR_PANEL, bd=0, highlightbackground=COLOR_BORDE, highlightthickness=1)
panel_moy.place(x=980, y=150, width=360, height=430)

tag_moy = tk.Label(panel_moy, text="JUGADOR 2", font=("Arial", 10, "bold"), fg=COLOR_SUB, bg=COLOR_PANEL)
tag_moy.place(x=20, y=12)

lbl_nombre_moy = tk.Label(panel_moy, text="MOY", font=("Arial", 20, "bold"), fg=COLOR_DORADO, bg=COLOR_PANEL)
lbl_nombre_moy.place(x=20, y=34)

lbl_logo_moy = tk.Label(panel_moy, bg=COLOR_PANEL, text="")
lbl_logo_moy.place(x=90, y=80)

lbl_equipo_moy = tk.Label(
    panel_moy,
    text="---",
    font=("Arial", 18, "bold"),
    fg=COLOR_TEXTO,
    bg=COLOR_PANEL,
    wraplength=300,
    justify="center"
)
lbl_equipo_moy.place(x=28, y=280, width=300)

barra_moy = BarraFC(panel_moy, width=260, height=12)
barra_moy.place(x=48, y=346)

btn_moy = tk.Button(
    panel_moy,
    text="SORTEAR MOY",
    font=("Arial", 11, "bold"),
    bg="#202831",
    fg="#ffffff",
    activebackground="#27313c",
    activeforeground="#ffffff",
    relief="flat",
    width=18,
    command=sortear_moy
)
btn_moy.place(x=100, y=378)

# Panel central
panel_central = tk.Frame(root, bg=COLOR_BG_PANEL, bd=0, highlightbackground=COLOR_BORDE, highlightthickness=1)
panel_central.place(x=505, y=150, width=430, height=430)

lbl_vs = tk.Label(
    panel_central,
    text="VS",
    font=("Arial", 44, "bold"),
    fg=COLOR_VERDE,
    bg=COLOR_BG_PANEL
)
lbl_vs.place(x=175, y=32)

lbl_mode_tag = tk.Label(
    panel_central,
    text="MODO DEL PARTIDO",
    font=("Arial", 11, "bold"),
    fg=COLOR_SUB,
    bg=COLOR_BG_PANEL
)
lbl_mode_tag.place(x=130, y=120)

lbl_modo_global = tk.Label(
    panel_central,
    text="---",
    font=("Arial", 24, "bold"),
    fg="#ffffff",
    bg=COLOR_BG_PANEL,
    wraplength=340,
    justify="center"
)
lbl_modo_global.place(x=45, y=150, width=340)

btn_modo = tk.Button(
    panel_central,
    text="SORTEAR MODO",
    font=("Arial", 11, "bold"),
    bg="#202831",
    fg="#ffffff",
    activebackground="#27313c",
    activeforeground="#ffffff",
    relief="flat",
    width=16,
    command=sortear_modo
)
btn_modo.place(x=142, y=235)

btn_sortear_todo = tk.Button(
    panel_central,
    text="RANDOM RÁPIDO",
    font=("Arial", 12, "bold"),
    bg="#202831",
    fg="#ffffff",
    activebackground="#27313c",
    activeforeground="#ffffff",
    relief="flat",
    width=18,
    command=animar_ruleta
)
btn_sortear_todo.place(x=126, y=300)

btn_reiniciar = tk.Button(
    panel_central,
    text="REINICIAR",
    font=("Arial", 12, "bold"),
    bg="#2b1b1b",
    fg="#ffffff",
    activebackground="#402727",
    activeforeground="#ffffff",
    relief="flat",
    width=18,
    command=reiniciar
)
btn_reiniciar.place(x=126, y=345)

# Botón grande
btn_start = tk.Button(
    root,
    text="INICIAR PARTIDO",
    font=("Arial", 24, "bold"),
    bg=COLOR_VERDE,
    fg="#000000",
    activebackground="#f0ff73",
    activeforeground="#000000",
    relief="raised",
    bd=4,
    width=18,
    command=iniciar_partido
)
btn_start.place(x=521, y=720)

# Overlay pack opening
overlay_frame = tk.Frame(root, bg="#000000")
overlay_text = tk.Label(
    overlay_frame,
    text="",
    font=("Arial", 34, "bold"),
    fg="#ffffff",
    bg="#000000"
)
overlay_text.place(relx=0.5, rely=0.5, anchor="center")

# Overlay túnel
overlay_tunel = tk.Frame(root, bg="#000000")
canvas_tunel = tk.Canvas(overlay_tunel, width=ANCHO, height=ALTO, bg="#000000", highlightthickness=0)
canvas_tunel.pack(fill="both", expand=True)
crear_tunel_visual()

# Cuenta regresiva
countdown_label = tk.Label(
    root,
    text="",
    font=("Arial", 90, "bold"),
    fg=COLOR_VERDE,
    bg="#000000"
)

# Logo gigante reveal
logo_reveal = tk.Label(root, bg="#000000", text="")
texto_reveal = tk.Label(
    root,
    text="",
    font=("Arial", 26, "bold"),
    fg="#ffffff",
    bg="#000000"
)

# =========================================================
# INICIO
# =========================================================
animar_beams()
animar_humo()
animar_luces_estadio()
root.mainloop()