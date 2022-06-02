import sys
import os
sys.path.append("..")

from math import ceil
from random import shuffle, uniform
from time import sleep
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRect, QThread, Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtMultimedia import QSound
import parametros as p


class SonidoDisparo(QThread):

    def __init__(self):
        super().__init__()
        self.sonido_disparo = QSound(p.RUTA_SONIDO_DISPARO)

    def run(self):
        self.sonido_disparo.play()


class EtiquetaGanaste(QThread):
    def __init__(self):
        super().__init__()
        self.etiqueta = QLabel("            ¡LOS ALIENS HAN SIDO DERROTADOS!")
        self.etiqueta.setFont(QFont(p.FUENTE, 40))
        self.etiqueta.setGeometry(-10, 150, 0, 80)
        self.etiqueta.setStyleSheet("background-color: gold")

    def run(self):
        while self.etiqueta.width() < 1400:
            sleep(0.00001)
            self.etiqueta.setGeometry(-10, 150, self.etiqueta.width()+30, 80)
            self.etiqueta.repaint()


class Perro(QThread):
    def __init__(self, pixeles_perro_y_alien):
        super().__init__()
        self.pixeles_perro_y_alien = pixeles_perro_y_alien
        self.pixeles_perro = QPixmap(p.RUTA_PERRO)

        self.perro_etiqueta = QLabel()
        self.perro_etiqueta.setPixmap(self.pixeles_perro)
        self.perro_etiqueta.setGeometry(100, 373, 200, 250)
        self.perro_etiqueta.setScaledContents(True)
        self.perro_etiqueta.setStyleSheet("background-color: transparent")

    def run(self):
        for j in range(7):
            for i in range(6):
                sleep(0.015)
                self.perro_etiqueta.move(self.perro_etiqueta.x(), self.perro_etiqueta.y() + 2)
                self.perro_etiqueta.repaint()
            for i in range(6):
                sleep(0.015)
                self.perro_etiqueta.move(self.perro_etiqueta.x(), self.perro_etiqueta.y() - 2)
                self.perro_etiqueta.repaint()
        sleep(0.2)
        self.perro_etiqueta.setPixmap(self.pixeles_perro_y_alien)
        self.perro_etiqueta.setGeometry(self.perro_etiqueta.x(), self.perro_etiqueta.y(), 270, 250)
        self.perro_etiqueta.repaint()


class AparecerAlien(QThread):

    senal_aparecer = pyqtSignal()

    def __init__(self, alien):
        super().__init__()
        self.alien = alien

    def run(self):
        self.senal_aparecer.emit()

    def aparecer_alien(self):
        self.alien.alien_etiqueta.setPixmap(self.alien.pixeles_alien)
        self.alien.alien_etiqueta.repaint()
        timer_hacer_invisible = QTimer(self)
        timer_hacer_invisible.setSingleShot(True)
        timer_hacer_invisible.setInterval(200)
        timer_hacer_invisible.timeout.connect(self.desinvisibilizar)
        timer_hacer_invisible.start()

    def desinvisibilizar(self):
        self.alien.invisible = False


class MatarAlien(QThread):

    senal_explotar = pyqtSignal()

    def __init__(self, alien):
        super().__init__()
        self.alien = alien
        self.cantidad_de_movimiento_numero = 0

    def run(self):
        self.alien.invisible = True
        if not self.alien.explotado and not self.alien.aliens_muertos == self.alien.nivel * 2:
            self.senal_explotar.emit()
        else:
            self.alien.alien_etiqueta.setPixmap(self.alien.lista_imagenes_disparo[0])
            sleep(0.2)
            self.alien.alien_etiqueta.setPixmap(self.alien.lista_imagenes_disparo[1])
            sleep(0.2)
            self.alien.alien_etiqueta.setPixmap(self.alien.lista_imagenes_disparo[2])
            sleep(0.2)
            self.alien.alien_etiqueta.setPixmap(self.alien.lista_imagenes_disparo[1])
            if self.alien.aliens_muertos == self.alien.nivel * 2:
                self.alien.alien_etiqueta.setText(str(self.alien.aliens_muertos))
                self.alien.alien_etiqueta.setStyleSheet("color: gold")
            else:
                sleep(0.2)
                self.alien.alien_etiqueta.setPixmap(self.alien.pixeles_invisible)

    def explosion_0(self):
        self.alien.alien_etiqueta.setPixmap(self.alien.lista_imagenes_disparo[0])
        timer_explosion_1 = QTimer(self)
        timer_explosion_1.setInterval(200)
        timer_explosion_1.setSingleShot(True)
        timer_explosion_1.timeout.connect(self.explosion_1)
        timer_explosion_1.start()

    def explosion_1(self):
        self.alien.alien_etiqueta.setPixmap(self.alien.lista_imagenes_disparo[1])
        timer_explosion_2 = QTimer(self)
        timer_explosion_2.setInterval(200)
        timer_explosion_2.setSingleShot(True)
        timer_explosion_2.timeout.connect(self.explosion_2)
        timer_explosion_2.start()

    def explosion_2(self):
        self.alien.alien_etiqueta.setPixmap(self.alien.lista_imagenes_disparo[2])
        timer_explosion_3 = QTimer(self)
        timer_explosion_3.setInterval(200)
        timer_explosion_3.setSingleShot(True)
        timer_explosion_3.timeout.connect(self.explosion_3)
        timer_explosion_3.start()

    def explosion_3(self):
        self.alien.alien_etiqueta.setPixmap(self.alien.lista_imagenes_disparo[1])
        timer_explosion_4 = QTimer(self)
        timer_explosion_4.setInterval(200)
        timer_explosion_4.setSingleShot(True)
        timer_explosion_4.timeout.connect(self.explosion_4)
        timer_explosion_4.start()

    def explosion_4(self):
        if not self.alien.explotado:
            self.alien.alien_etiqueta.setText(str(self.alien.aliens_muertos))
            self.alien.alien_etiqueta.setStyleSheet("color: red")
            x = self.alien.alien_etiqueta.x() + 40
            y = self.alien.alien_etiqueta.y()
            self.alien.alien_etiqueta.move(x, y)
            self.mover_numero_1()

    def mover_numero_1(self):
        timer_mover_numero_1 = QTimer(self)
        timer_mover_numero_1.setSingleShot(True)
        timer_mover_numero_1.setInterval(50)
        timer_mover_numero_1.timeout.connect(self.mover_numero_2)
        x = self.alien.alien_etiqueta.x()
        self.alien.alien_etiqueta.move(x, self.alien.alien_etiqueta.y() - 2)
        self.cantidad_de_movimiento_numero += 1
        timer_mover_numero_1.start()

    def mover_numero_2(self):
        timer_mover_numero_2 = QTimer(self)
        timer_mover_numero_2.setSingleShot(True)
        timer_mover_numero_2.setInterval(50)
        timer_mover_numero_2.timeout.connect(self.mover_numero_1)
        x = self.alien.alien_etiqueta.x()
        self.alien.alien_etiqueta.move(x, self.alien.alien_etiqueta.y() - 2)
        self.cantidad_de_movimiento_numero += 1
        if self.cantidad_de_movimiento_numero < 25:
            timer_mover_numero_2.start()
        else:
            self.desaparecer()

    def desaparecer(self):
        self.alien.alien_etiqueta.setPixmap(self.alien.pixeles_invisible)
        self.alien.explotado = True


class Alien(QThread):

    actualizar = pyqtSignal(int, int)

    def __init__(self, ruta_alien, ruta_alien_dead, posicion, nivel, velocidad, cuantos_aliens):
        direcciones_posibles = [(i, j) for i in range(2) for j in range(2)]
        shuffle(direcciones_posibles)
        direccion_x = direcciones_posibles[0][0]
        direccion_y = direcciones_posibles[0][1]
        if not direccion_x:
            direccion_x = -1
        if not direccion_y:
            direccion_y = -1

        super().__init__()

        self.invisible = True

        self.aliens_muertos = 0

        self.cuantos_aliens = cuantos_aliens

        self.explotado = False

        self.nivel = nivel

        ruta_disparo_1 = p.RUTA_DISPARO_1
        ruta_disparo_2 = p.RUTA_DISPARO_2
        ruta_disparo_3 = p.RUTA_DISPARO_3

        pixeles_disparo_1 = QPixmap(ruta_disparo_1)
        pixeles_disparo_2 = QPixmap(ruta_disparo_2)
        pixeles_disparo_3 = QPixmap(ruta_disparo_3)

        self.pixeles_invisible = QPixmap()
        self.pixeles_invisible.fill(Qt.transparent)

        self.lista_imagenes_disparo = [pixeles_disparo_1, pixeles_disparo_2, pixeles_disparo_3]

        self.pixeles_alien = QPixmap(ruta_alien)
        self.pixeles_alien_dead = QPixmap(ruta_alien_dead)

        self._posicion_x = posicion[0] * 90

        self._posicion_y = posicion[1] * 90

        self.alien_etiqueta = QLabel()
        self.alien_etiqueta.setGeometry(self.posicion_x, self.posicion_y, 100, 100)
        self.alien_etiqueta.setPixmap(self.pixeles_invisible)
        self.alien_etiqueta.setStyleSheet("background-color: transparent")
        self.alien_etiqueta.setScaledContents(True)
        self.alien_etiqueta.setFont(QFont(p.FUENTE, 30))

        self.velocidad = velocidad

        self.velocidad[0] *= direccion_x
        self.velocidad[1] *= direccion_y

        if self.nivel > 1:
            numerador = uniform(0.9, 1)
            self.velocidad[0] *= 1/numerador
            self.velocidad[1] *= 1/numerador

        self.vivo = True
        self.pausa = False

        self.matar_alien = MatarAlien(self)
        self.aparecer_alien = AparecerAlien(self)
        self.matar_alien.senal_explotar.connect(self.matar_alien.explosion_0)
        self.aparecer_alien.senal_aparecer.connect(self.aparecer_alien.aparecer_alien)


    @property
    def posicion_x(self):
        return self._posicion_x

    @posicion_x.setter
    def posicion_x(self, valor):
        if valor < 0:
            self._posicion_x = 0
            self.velocidad[0] = self.velocidad[0] * (-1)
        elif valor > 1230:
            self._posicion_x = 1230
            self.velocidad[0] = self.velocidad[0] * (-1)
        else:
            self._posicion_x = valor

    @property
    def posicion_y(self):
        return self._posicion_y

    @posicion_y.setter
    def posicion_y(self, valor):
        if valor < 0:
            self._posicion_y = 0
            self.velocidad[1] = self.velocidad[1] * (-1)
        elif valor > 500:
            self._posicion_y = 500
            self.velocidad[1] = self.velocidad[1] * (-1)
        else:
            self._posicion_y = valor

    def run(self):
        while self.vivo and not self.pausa:
            sleep(0.01)
            self.posicion_x += self.velocidad[0]
            self.posicion_y += self.velocidad[1]
            self.actualizar.emit(self.posicion_x, self.posicion_y)

    def mover_etiqueta(self, posicion_x, posicion_y):
        self.alien_etiqueta.move(posicion_x, posicion_y)
