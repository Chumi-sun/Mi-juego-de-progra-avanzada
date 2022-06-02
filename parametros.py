import os
from random import uniform
# rutas
RUTA_LOGO = os.path.join("Sprites", "Logo", "Logo.png")
RUTA_FONDO_JUPITER = os.path.join("Sprites", "Fondos", "Jupiter.png")
RUTA_FONDO_GALAXIA = os.path.join("Sprites", "Fondos", "Galaxia.png")
RUTA_FONDO_LUNA = os.path.join("Sprites", "Fondos", "Luna.png")
RUTA_ALIEN_1 = os.path.join("Sprites", "Aliens", "Alien1.png")
RUTA_ALIEN_2 = os.path.join("Sprites", "Aliens", "Alien2.png")
RUTA_ALIEN_3 = os.path.join("Sprites", "Aliens", "Alien3.png")
RUTA_ALIEN_1_DEAD = os.path.join("Sprites", "Aliens", "Alien1_dead.png")
RUTA_ALIEN_2_DEAD = os.path.join("Sprites", "Aliens", "Alien2_dead.png")
RUTA_ALIEN_3_DEAD = os.path.join("Sprites", "Aliens", "Alien3_dead.png")
RUTA_IMAGEN_BALA = os.path.join("Sprites", "Elementos juego", "Bala.png")
RUTA_X_PIXELADA = os.path.join("Extras", "x_pixelada.png")
RUTA_MIRA_TELESCOPICA_NEGRA = os.path.join("Sprites", "Elementos juego", "Disparador_negro.png")
RUTA_MIRA_TELESCOPICA_ROJA = os.path.join("Sprites", "Elementos juego", "Disparador_rojo.png")
RUTA_DISPARO_1 = os.path.join("Sprites", "Elementos juego", "Disparo_f1.png")
RUTA_DISPARO_2 = os.path.join("Sprites", "Elementos juego", "Disparo_f2.png")
RUTA_DISPARO_3 = os.path.join("Sprites", "Elementos juego", "Disparo_f3.png")
RUTA_PERRO = os.path.join("Sprites", "Terminator-Dog", "Dog1.png")
RUTA_PERRO_LUNA = os.path.join("Sprites", "Terminator-Dog", "Perro_y_alien1.png")
RUTA_PERRO_JUPITER = os.path.join("Sprites", "Terminator-Dog", "Perro_y_alien2.png")
RUTA_PERRO_GALAXIA = os.path.join("Sprites", "Terminator-Dog", "Perro_y_alien3.png")
RUTA_SONIDO_DISPARO = os.path.join("Sonidos", "disparo.wav")

# Fuentes
FUENTE = "Agency FB"

# Tamaños
LARGO_VENTANA_INICIO = 900
ALTO_VENTANA_INICIO = 750
LARGO_VENTANA_PRINCIPAL = 1330
ALTO_VENTANA_PRINCIPAL = 665
POSICIÓN_X_PRIMER_MUNDO = 70
POSICIÓN_Y_PRIMER_MUNDO = 150
LARGO_PRIMER_MUNDO = 350
ALTO_PRIMER_MUNDO = 250
ALTURA_ETIQUETAS_NOMBRES_JUEGO = 620
X_ETIQUETAS_NUMEROS_POST_JUEGO = 600

# tiempos
DURACIÓN_NIVEL_INICIAL = 30
DURACIÓN_MIRA_ROJA = 1
TIEMPO_TERMINATOR_DOG = 2.2

# Cantidades
BALAS_INICIALES = 15
ALIENS_INICIALES = 2
VELOCIDAD_MIRA_TELESCOPICA = 20
VELOCIDAD_ALIEN = [1, 1]
VELOCIDAD_ALIEN_2 = [1, 1]

# Ponderadores
MINIMO_PONDERADOR_TUTORIAL = 0.9
MAXIMO_PONDERADOR_TUTORIAL = 1
PONDERADOR_TUTORIAL = uniform(MINIMO_PONDERADOR_TUTORIAL, MAXIMO_PONDERADOR_TUTORIAL)
MINIMO_PONDERADOR_ENTRENAMIENTO = 0.8
MAXIMO_PONDERADOR_ENTRENAMIENTO = 0.9
PONDERADOR_ENTRENAMIENTO = uniform(MINIMO_PONDERADOR_ENTRENAMIENTO, MAXIMO_PONDERADOR_ENTRENAMIENTO)
MINIMO_PONDERADOR_INVASION = 0.7
MAXIMO_PONDERADOR_INVASION = 0.8
PONDERADOR_INVASION = uniform(MINIMO_PONDERADOR_INVASION, MAXIMO_PONDERADOR_INVASION)
