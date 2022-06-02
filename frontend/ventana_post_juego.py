import sys
sys.path.append("..")

from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QPushButton, QProgressBar

import parametros as p


class VentanaPostJuego(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 800, p.ALTO_VENTANA_PRINCIPAL + 120)
        self.setFixedSize(800, p.ALTO_VENTANA_PRINCIPAL + 120)
        self.setStyleSheet("background-color: darkslateblue")

    def recibir_objetos(self, lista):

        self.fondo = lista[0]
        self.fondo.setParent(self)
        self.titular = QLabel(" Resumen del nivel ", self)
        self.titular.setFont(QFont(p.FUENTE, 40))
        self.titular.move(100, 63)

        self.texto_nivel_actual = QLabel("                 Nivel actual ", self)
        self.texto_nivel_actual.setFont(QFont(p.FUENTE, 25))
        self.texto_nivel_actual.setGeometry(0, 200, 1000, 54)

        self.texto_balas_restantes = QLabel("                 Balas restantes ", self)
        self.texto_balas_restantes.setFont(QFont(p.FUENTE, 25))
        self.texto_balas_restantes.setGeometry(00, 290, 1000, 54)

        self.texto_tiempo_restante = QLabel("                 Tiempo restante", self)
        self.texto_tiempo_restante.setFont(QFont(p.FUENTE, 25))
        self.texto_tiempo_restante.setGeometry(0, 380, 1000, 54)

        self.texto_puntaje_total = QLabel("                 Puntaje total ", self)
        self.texto_puntaje_total.setFont(QFont(p.FUENTE, 25))
        self.texto_puntaje_total.setGeometry(0, 470, 1000, 54)
        self.texto_puntaje_total.setStyleSheet("background-color: gold")

        self.texto_puntaje_nivel = QLabel("                 Puntaje nivel ", self)
        self.texto_puntaje_nivel.setFont(QFont(p.FUENTE, 25))
        self.texto_puntaje_nivel.setGeometry(0, 560, 1000, 54)

        for i in range(1, len(lista)-1):
            etiqueta = lista[i]
            etiqueta.setParent(self)
            if i == 1:
                etiqueta.setStyleSheet("background-color: transparent")

        if lista[-1]:
            self.setWindowTitle("¡Ganaste!")
        else:
            self.setWindowTitle("Perdiste")

        self.abrir_ventana()

    def abrir_ventana(self):
        self.show()

    def cerrar_ventana(self):
        self.hide()
