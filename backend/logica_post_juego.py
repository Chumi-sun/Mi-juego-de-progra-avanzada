import sys
import os
sys.path.append("..")

from math import ceil
from random import shuffle, uniform
from time import sleep
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRect, QThread, QEvent
from PyQt5.QtGui import QPixmap, QFont
import parametros as p


class LogicaPostJuego(QObject):

    senal_abrir_ventana_post_juego = pyqtSignal(list)
    senal_salir = pyqtSignal()
    senal_borrar_puntaje = pyqtSignal()
    senal_cerrar_post_juego = pyqtSignal()
    senal_siguiente_nivel = pyqtSignal(int)
    senal_borrar_nombre = pyqtSignal()

    def __init__(self):
        super().__init__()

    def crear_objetos(self, lista):
        ganar = lista[8]
        self.puntaje_acumulado = lista[4]
        if ganar == "cheatcode":
            self.siguiente_nivel()
        else:
            tiempo_restante = lista[0]
            balas_restantes = lista[1]
            ganar = lista[2]
            puntaje_nivel = lista[3]

            nivel = lista[5]
            destino = lista[6]
            self.nombre = lista[7]

            self.nivel = QLabel(str(nivel))
            self.nivel.setFont(QFont(p.FUENTE, 25))
            self.nivel.move(p.X_ETIQUETAS_NUMEROS_POST_JUEGO, 200)

            self.balas_restantes = QLabel(str(balas_restantes))
            self.balas_restantes.setFont(QFont(p.FUENTE, 25))
            self.balas_restantes.move(p.X_ETIQUETAS_NUMEROS_POST_JUEGO, 290)

            self.tiempo_restante = QLabel(str(ceil(tiempo_restante/1000)))
            self.tiempo_restante.setFont(QFont(p.FUENTE, 25))
            self.tiempo_restante.move(p.X_ETIQUETAS_NUMEROS_POST_JUEGO, 380)

            string_puntaje = self.puntaje_acumulado
            self.puntaje_acumulado_etiqueta = QLabel(f"{string_puntaje:,}".replace(",", "."))
            self.puntaje_acumulado_etiqueta.setFont(QFont(p.FUENTE, 25))
            self.puntaje_acumulado_etiqueta.move(p.X_ETIQUETAS_NUMEROS_POST_JUEGO, 470)
            self.puntaje_acumulado_etiqueta.setStyleSheet("background-color: gold")

            self.puntaje_nivel = QLabel(f"{puntaje_nivel:,}".replace(",", "."))
            self.puntaje_nivel.setFont(QFont(p.FUENTE, 25))
            self.puntaje_nivel.move(p.X_ETIQUETAS_NUMEROS_POST_JUEGO, 560)

            if destino == "luna":
                pixeles_fondo = QPixmap(p.RUTA_FONDO_LUNA)
                pixeles_alien = QPixmap(p.RUTA_ALIEN_1_DEAD)
            elif destino == "júpiter":
                pixeles_fondo = QPixmap(p.RUTA_FONDO_JUPITER)
                pixeles_alien = QPixmap(p.RUTA_ALIEN_2_DEAD)
            else:
                pixeles_fondo = QPixmap(p.RUTA_FONDO_GALAXIA)
                pixeles_alien = QPixmap(p.RUTA_ALIEN_3_DEAD)

            self.fondo = QLabel()
            self.fondo.setPixmap(pixeles_fondo)
            self.fondo.setGeometry(-300, 0, 1150, p.ALTO_VENTANA_PRINCIPAL + 120)
            self.fondo.setScaledContents(True)

            self.alien = QLabel()
            self.alien.setPixmap(pixeles_alien)
            self.alien.setGeometry(570, 50, 100, 100)
            self.alien.setScaledContents(True)

            self._boton_salir = QPushButton(" Salir ")
            self._boton_salir.setFont(QFont(p.FUENTE, 20))
            self._boton_salir.move(500, 700)
            self._boton_salir.clicked.connect(self.salir)
            self.boton_salir.installEventFilter(self)

            self._boton_siguiente_nivel = QPushButton(" Siguiente nivel ")
            self._boton_siguiente_nivel.setFont(QFont(p.FUENTE, 20))
            self._boton_siguiente_nivel.move(200, 700)
            self.boton_siguiente_nivel.installEventFilter(self)

            self.etiqueta_ganaste_o_perdiste = QLabel("")
            self.etiqueta_ganaste_o_perdiste.setFont(QFont(p.FUENTE, 20))
            self.etiqueta_ganaste_o_perdiste.move(100, 640)

            if ganar:
                self._boton_siguiente_nivel.clicked.connect(self.siguiente_nivel)
                self.etiqueta_ganaste_o_perdiste.setText(
                    " ¡Puedes dominar el siguiente nivel! ")
                self.etiqueta_ganaste_o_perdiste.setStyleSheet("background-color: green")
                self.boton_siguiente_nivel.setStyleSheet("background-color: green")
            else:
                self.etiqueta_ganaste_o_perdiste.setText(
                    " Perdiste, los aliens invadieron la tierra. ")
                self.etiqueta_ganaste_o_perdiste.setStyleSheet("background-color: red")
                self.boton_siguiente_nivel.setStyleSheet("background-color: red")

            self.senal_abrir_ventana_post_juego.emit([self.fondo,
                                                      self.alien, self.nivel,
                                                      self.balas_restantes, self.tiempo_restante,
                                                      self.puntaje_nivel,
                                                      self.puntaje_acumulado_etiqueta,
                                                      self.boton_siguiente_nivel, self.boton_salir,
                                                      self.etiqueta_ganaste_o_perdiste, ganar])

    @property
    def boton_salir(self):
        return self._boton_salir

    @property
    def boton_siguiente_nivel(self):
        return self._boton_siguiente_nivel

    def eventFilter(self, objeto, evento):
        if evento.type() == QEvent.KeyPress:
            return True
        return super().eventFilter(objeto, evento)

    def salir(self):
        self.senal_salir.emit()
        self.senal_cerrar_post_juego.emit()
        self.senal_borrar_puntaje.emit()
        self.senal_borrar_nombre.emit()
        self.registrar_nombre(self.nombre, self.puntaje_acumulado)

    def registrar_nombre(self, nombre, puntaje):
        with open("puntajes.txt", "a", encoding="UTF-8") as archivo_puntajes:
            archivo_puntajes.write(f"\n{nombre},{str(puntaje).replace('.', '')}")

    def siguiente_nivel(self):
        sleep(0.2)
        self.senal_siguiente_nivel.emit(int(str(self.puntaje_acumulado).replace(".", "")))
        self.senal_cerrar_post_juego.emit()
