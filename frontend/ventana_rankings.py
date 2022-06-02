import sys
sys.path.append("..")

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt, QEvent
import parametros as p


class VentanaRankings(QWidget):

    senal_ver_ranking = pyqtSignal(bool)
    senal_abrir_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 200, 500, 500)
        self.setWindowTitle("Ranking de puntajes más altos")
        self.setFixedSize(450, 570)
        self.setStyleSheet("background-color: darkslateblue;")
        self.crear_elementos()

    def crear_elementos(self):
        self.titulo = QLabel("RANKING\nINTERGALÁCTICO", self)
        self.titulo.setFont(QFont(p.FUENTE, 35))
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.move(72, 50)
        self.etiquetas = []

        for i in range(5):
            etiqueta_nombre_jugador = QLabel(str(i+1)+". VACÍO", self)
            etiqueta_nombre_jugador.setFont(QFont(p.FUENTE, 16))
            etiqueta_nombre_jugador.move(80, 230 + (50*i))

            etiqueta_puntaje_jugador = QLabel("XXXX", self)
            etiqueta_puntaje_jugador.setFont(QFont(p.FUENTE, 16))
            etiqueta_puntaje_jugador.move(325, 230 + (50*i))

            self.etiquetas.append([etiqueta_nombre_jugador, etiqueta_puntaje_jugador])
            self.senal_ver_ranking.emit(True)

        self._botón_volver = QPushButton("Volver", self)
        self._botón_volver.move(180, 490)
        self._botón_volver.setFont(QFont(p.FUENTE, 16))
        self._botón_volver.clicked.connect(self.volver_a_inicio)
        self.botón_volver.installEventFilter(self)

    @property
    def botón_volver(self):
        return self._botón_volver

    def eventFilter(self, obj, evento):
        if obj is self._botón_volver and evento.type() == QEvent.KeyPress:
            return True
        return super().eventFilter(obj, evento)

    def colocar_texto_etiquetas_puntajes(self, lista_jugadores_y_puntajes):
        for index in range(len(lista_jugadores_y_puntajes)):
            self.etiquetas[index][0].setText(str(index+1) + ". " +
                                             lista_jugadores_y_puntajes[index][0])
            self.etiquetas[index][1].setText(f"{lista_jugadores_y_puntajes[index][1]:,}"
                                             .replace(",", "."))

    def volver_a_inicio(self):
        self.hide()
        self.senal_abrir_inicio.emit()

    def abrir_ventana(self, status):
        if status:
            self.show()

    def closeEvent(self, event):
        if event.type() == 19:
            self.volver_a_inicio()
