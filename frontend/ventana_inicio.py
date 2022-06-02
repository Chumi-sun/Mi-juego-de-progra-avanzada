import sys
sys.path.append("..")


from PyQt5.QtGui import QPixmap, QFont, QPainter
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QPushButton
from PyQt5.QtCore import pyqtSignal, QRectF, QEvent
import parametros as p


class VentanaInicio(QWidget):

    senal_abrir_ventana_principal = pyqtSignal(bool)
    senal_abrir_rankings = pyqtSignal(bool)
    senal_consultar_puntajes_altos = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("¡A CAZAR ALIENS!")
        self.setFixedSize(p.LARGO_VENTANA_INICIO, p.ALTO_VENTANA_INICIO)
        self.setStyleSheet("background-color: darkslateblue;")
        self.crear_elementos()

    def crear_elementos(self):
        # Fondo
        ruta_fondo = p.RUTA_FONDO_GALAXIA
        pixeles_fondo = QPixmap(ruta_fondo)
        self.fondo = QLabel(self)
        self.fondo.setGeometry(-50, 0, p.LARGO_VENTANA_INICIO+100, p.ALTO_VENTANA_INICIO)
        self.fondo.setPixmap(pixeles_fondo)
        self.fondo.setScaledContents(True)

        # Logo
        ruta_logo = p.RUTA_LOGO
        pixeles_logo = QPixmap(ruta_logo)
        self.logo = QLabel(self)
        self.logo.setGeometry(50, 40, p.LARGO_VENTANA_INICIO*0.88, p.ALTO_VENTANA_INICIO*0.62)
        self.logo.setStyleSheet("background-color: transparent")
        self.logo.setPixmap(pixeles_logo)
        self.logo.setScaledContents(True)

        # botones
        self._botón_jugar = QPushButton("¡Jugar!", self)
        self._botón_jugar.setFont(QFont(p.FUENTE, 22))
        self._botón_jugar.setGeometry(270, 550, 350, 54)
        self._botón_jugar.clicked.connect(self.jugar)
        self.botón_jugar.installEventFilter(self)

        self._botón_rankings = QPushButton("RANKING INTERGALÁCTICO", self)
        self._botón_rankings.setFont((QFont(p.FUENTE, 22)))
        self._botón_rankings.setGeometry(270, 640, 350, 54)
        self._botón_rankings.clicked.connect(self.rankings)
        self.botón_rankings.installEventFilter(self)

    @property
    def botón_jugar(self):
        return self._botón_jugar

    @property
    def botón_rankings(self):
        return self._botón_rankings

    def eventFilter(self, obj, event):
        if obj is self._botón_jugar and event.type() == QEvent.KeyPress:
            return True
        if obj is self._botón_rankings and event.type() == QEvent.KeyPress:
            return True
        return super().eventFilter(obj, event)

    def jugar(self):
        self.senal_abrir_ventana_principal.emit(True)
        self.hide()

    def rankings(self):
        self.senal_consultar_puntajes_altos.emit()
        self.senal_abrir_rankings.emit(True)
        self.hide()

    def abrir_ventana(self):
        self.show()
