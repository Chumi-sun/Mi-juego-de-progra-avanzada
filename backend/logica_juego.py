import sys
import os
sys.path.append("..")

from math import ceil
from random import shuffle, sample
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRect, QThread, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QSound
import parametros as p
from backend.threads_juego import Alien, Perro, EtiquetaGanaste, SonidoDisparo


class LogicaJuego(QObject):

    senal_escenario_escogido = pyqtSignal(list)
    senal_datos_juego = pyqtSignal(list)
    senal_cambio_mira_telescopica = pyqtSignal(tuple)
    senal_alien_shot = pyqtSignal(Alien)
    senal_acabar_juego = pyqtSignal(list)
    senal_enviar_datos_post_juego = pyqtSignal(list)
    senal_ronda_acabada = pyqtSignal()
    senal_pasar_de_nivel = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.lista_aliens = []

        self.puntaje_acumulado = 0
        self.nivel = 1
        self.velocidad = p.VELOCIDAD_ALIEN.copy()
        self.duracion = p.DURACIÓN_NIVEL_INICIAL

        self.ruta_fondo = ""
        self.ruta_alien = ""
        self.ruta_alien_dead = ""

        self.fondo = QLabel()
        self.alien = QLabel()
        self.alien_dead = QLabel()

        self.fondo.setGeometry(0, 0, p.LARGO_VENTANA_PRINCIPAL, p.ALTO_VENTANA_PRINCIPAL + 100)
        self.alien.setFixedSize(100, 100)
        self.alien_dead.setFixedSize(100, 100)

        self.sonido_disparo = SonidoDisparo()

    @property
    def balas_restantes(self):
        return self._balas_restantes

    @balas_restantes.setter
    def balas_restantes(self, valor):
        if valor <= 0:
            self._balas_restantes = 0
        else:
            self._balas_restantes = valor

    def iniciar_juego(self, nombre, destino):
        self.nombre = nombre
        self.lista_aliens = []
        self.aliens_muertos = 0
        self.destino = destino
        self._balas_restantes = self.nivel * 4
        self.puntaje_nivel = 0

        self.activo = True
        self.ganaste = False
        self.cheatcode_balas = False

        if self.destino == "luna":
            self.titulo_ventana = "Tutorial Lunar"
            self.ruta_fondo = p.RUTA_FONDO_LUNA
            self.ruta_alien = p.RUTA_ALIEN_1
            self.ruta_alien_dead = p.RUTA_ALIEN_1_DEAD
            self.dificultad = p.PONDERADOR_TUTORIAL
            self.ruta_perro_y_alien = p.RUTA_PERRO_LUNA
        elif self.destino == "júpiter":
            self.titulo_ventana = "Entrenamiento en Júpiter"
            self.ruta_fondo = p.RUTA_FONDO_JUPITER
            self.ruta_alien = p.RUTA_ALIEN_2
            self.ruta_alien_dead = p.RUTA_ALIEN_2_DEAD
            self.dificultad = p.PONDERADOR_ENTRENAMIENTO
            self.ruta_perro_y_alien = p.RUTA_PERRO_JUPITER
        else:
            self.titulo_ventana = "Invasión Galáctica"
            self.ruta_fondo = p.RUTA_FONDO_GALAXIA
            self.ruta_alien = p.RUTA_ALIEN_3
            self.ruta_alien_dead = p.RUTA_ALIEN_3_DEAD
            self.dificultad = p.PONDERADOR_INVASION
            self.ruta_perro_y_alien = p.RUTA_PERRO_GALAXIA

        if self.nivel > 0:
            self.duracion *= self.dificultad

        self.timer_nivel = QTimer(self)
        self.timer_nivel.setInterval(self.duracion * 1000)
        self.timer_nivel.setSingleShot(True)
        self.timer_nivel.timeout.connect(self.tiempo_agotado)
        self.timer_nivel.start()

        self.timer_datos = QTimer(self)
        self.timer_datos.setInterval(16)
        self.timer_datos.timeout.connect(self.enviar_datos)
        self.timer_datos.start()

        self.crear_aliens()

        self.pixeles_perro_y_alien = QPixmap(self.ruta_perro_y_alien)
        self.perro = Perro(self.pixeles_perro_y_alien)

        pixeles_fondo = QPixmap(self.ruta_fondo)
        pixeles_alien = QPixmap(self.ruta_alien)
        pixeles_alien_dead = QPixmap(self.ruta_alien_dead)

        self.fondo.setPixmap(pixeles_fondo)
        self.fondo.setScaledContents(True)

        self.alien.setPixmap(pixeles_alien)
        self.alien.setScaledContents(True)

        self.alien_dead.setPixmap(pixeles_alien_dead)
        self.alien_dead.setScaledContents(True)

        self.etiqueta_ganaste = EtiquetaGanaste()

        self.senal_escenario_escogido.emit([self.fondo, self.titulo_ventana, self.lista_aliens,
                                            self.perro, self.etiqueta_ganaste, self.nivel,
                                            self.puntaje_acumulado, self.nombre])

    def crear_aliens(self):
        self.lista_aliens = []
        tuplas_posibles = []
        if self.nivel > 0:
            self.velocidad[0] = self.velocidad[0] * 1/self.dificultad
        if self.nivel > 0:
            self.velocidad[1] = self.velocidad[1] * 1/self.dificultad

        for i in range(13):
            for j in range(6):
                tuplas_posibles.append((i, j))
        shuffle(tuplas_posibles)

        for i in range(int((self.nivel + int(self.nivel//40))//40)):
            posiciones_extra = sample(tuplas_posibles.copy(), len(tuplas_posibles.copy()))
            tuplas_posibles += posiciones_extra
        for i in range(0, (self.nivel * 2)):
            posicion = tuplas_posibles[i]
            alien = Alien(self.ruta_alien, self.ruta_alien_dead, posicion,
                          self.nivel, self.velocidad.copy(), self.nivel * 2)
            self.lista_aliens.append(alien)

    def mover_mira(self, dirección, posición):
        x = posición[0]
        y = posición[1]
        if dirección == 87:
            if y - p.VELOCIDAD_MIRA_TELESCOPICA >= -80:
                nueva_posicion = (x, y - p.VELOCIDAD_MIRA_TELESCOPICA)
            else:
                nueva_posicion = (x, -80)
        elif dirección == 65:
            if x - p.VELOCIDAD_MIRA_TELESCOPICA >= -130:
                nueva_posicion = (x - p.VELOCIDAD_MIRA_TELESCOPICA, y)
            else:
                nueva_posicion = (-130, y)
        elif dirección == 83:
            if y + p.VELOCIDAD_MIRA_TELESCOPICA <= 478:
                nueva_posicion = (x, y + p.VELOCIDAD_MIRA_TELESCOPICA)
            else:
                nueva_posicion = (x, 478)
        elif dirección == 68:
            if x + p.VELOCIDAD_MIRA_TELESCOPICA <= 1161:
                nueva_posicion = (x + p.VELOCIDAD_MIRA_TELESCOPICA, y)
            else:
                nueva_posicion = (1161, y)
        self.senal_cambio_mira_telescopica.emit(nueva_posicion)

    def disparar(self, posicion_x, posicion_y, lista_aliens):
        quieres_sonido = False
        if quieres_sonido:
            self.sonido_disparo.start()
        centro_mira_x = posicion_x + 130
        centro_mira_y = posicion_y + 80
        for alien in lista_aliens:
            if centro_mira_x < alien.alien_etiqueta.x() + 70 < centro_mira_x + 100:
                if centro_mira_y < alien.alien_etiqueta.y() + 70 < centro_mira_y + 100:
                    if not alien.invisible:
                        alien.vivo = False
                        self.aliens_muertos += 1
                        alien.aliens_muertos = self.aliens_muertos
                        alien.matar_alien.start()
                        alien.invisible = True
                        if not self.aliens_muertos % 2:
                            if not (self.aliens_muertos == len(self.lista_aliens)):
                                self.senal_ronda_acabada.emit()
        if not self.cheatcode_balas:
            self.balas_restantes -= 1
        if self.balas_restantes == 0:
            self.balas_agotadas()


    def calcular_puntaje_nivel(self, lista):

        tiempo_restante = ceil(lista[0]/1000)

        balas_restantes = lista[1]

        puntaje_nivel = int(((len(self.lista_aliens) * 100) +
                             (((tiempo_restante * 30) + (balas_restantes * 70))
                              * self.nivel))/self.dificultad)

        return puntaje_nivel

    def detener_timers(self):
        self.timer_nivel.stop()
        self.timer_datos.stop()

    def enviar_datos(self):
        cantidad_de_aliens = len(self.lista_aliens)
        aliens_muertos = 0
        for alien in self.lista_aliens:
            if not alien.vivo:
                aliens_muertos += 1
        if aliens_muertos == cantidad_de_aliens:
            self.aliens_agotados()
        self.senal_datos_juego.emit([self.timer_nivel.remainingTime(), self.balas_restantes,
                                     self.duracion, self.nivel*2 - aliens_muertos])

    def tiempo_agotado(self):
        self.timer_datos.stop()

        lista = ([0, self.balas_restantes, self.ganaste])

        self.enviar_senales_termino_juego(lista)

    def balas_agotadas(self):
        aliens_vivos = 0
        for alien in self.lista_aliens:
            if alien.vivo:
                aliens_vivos += 1
        if aliens_vivos:
            lista = [self.timer_nivel.remainingTime(), self.balas_restantes, self.ganaste]
            self.enviar_senales_termino_juego(lista)

    def aliens_agotados(self):
        self.ganaste = True
        lista = [self.timer_nivel.remainingTime(), self.balas_restantes, self.ganaste]
        self.enviar_senales_termino_juego(lista)
        self.ganaste = False

    def cheatcode_cia(self):
        self.ganaste = "cheatcode"
        lista = [self.timer_nivel.remainingTime(), self.balas_restantes, self.ganaste]
        self.enviar_senales_termino_juego(lista)
        self.ganaste = False

    def enviar_senales_termino_juego(self, lista):
        ganar = lista[2]
        if ganar:
            self.puntaje_nivel = self.calcular_puntaje_nivel(lista)
        else:
            self.puntaje_nivel = 0
        self.puntaje_acumulado += self.puntaje_nivel
        self.senal_acabar_juego.emit(lista)
        lista.append(self.puntaje_nivel)
        lista.append(self.puntaje_acumulado)
        lista.append(self.nivel)
        lista.append(self.destino)
        lista.append(self.nombre)
        lista.append(ganar)

        for alien in self.lista_aliens:
            alien.alien_etiqueta.hide()
        self.senal_enviar_datos_post_juego.emit(lista)

    def pausar(self):
        if self.activo:
            self.activo = False
            self.tiempo_restante = self.timer_nivel.remainingTime()
            self.timer_datos.stop()
            self.timer_nivel.stop()
        else:
            self.activo = True
            self.timer_nivel.setInterval(self.tiempo_restante)
            self.timer_datos.start()
            self.timer_nivel.start()

    def borrar_puntaje(self):
        self.puntaje_acumulado = 0
        self.nivel = 1
        self.velocidad = p.VELOCIDAD_ALIEN.copy()
        self.duracion = p.DURACIÓN_NIVEL_INICIAL

    def siguiente_nivel(self, puntaje_acumulado):

        self.lista_aliens = []
        self.puntaje_acumulado = puntaje_acumulado
        self.nivel += 1
        self.iniciar_juego(self.nombre, self.destino)

    def cheatcode_balas_infinitas(self):
        self.cheatcode_balas = True
