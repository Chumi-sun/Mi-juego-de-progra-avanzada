import sys
sys.path.append("")

from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton,\
    QRadioButton, QButtonGroup, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt, QEvent
import parametros as p


class VentanaPrincipal(QWidget):

    senal_volver = pyqtSignal()
    senal_enviar_nombre = pyqtSignal(str)
    senal_enviar_seleccion = pyqtSignal(bool, bool, bool)
    senal_abrir_juego = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 100, p.LARGO_VENTANA_PRINCIPAL, p.ALTO_VENTANA_PRINCIPAL)
        self.nombre = False
        self.destino = False
        self.setWindowTitle("¡A lo salvaje!")
        self.setFixedSize(p.LARGO_VENTANA_PRINCIPAL, p.ALTO_VENTANA_PRINCIPAL)
        self.setStyleSheet("background-color: darkslateblue")
        self.crear_objetos()

    def crear_objetos(self):
        ruta_galaxia = p.RUTA_FONDO_GALAXIA
        ruta_jupiter = p.RUTA_FONDO_JUPITER
        ruta_luna = p.RUTA_FONDO_LUNA
        ruta_alien_1 = p.RUTA_ALIEN_1
        ruta_alien_2 = p.RUTA_ALIEN_2
        ruta_alien_3 = p.RUTA_ALIEN_3

        pixeles_galaxia = QPixmap(ruta_galaxia)
        pixeles_jupiter = QPixmap(ruta_jupiter)
        pixeles_luna = QPixmap(ruta_luna)
        pixeles_alien_1 = QPixmap(ruta_alien_1)
        pixeles_alien_2 = QPixmap(ruta_alien_2)
        pixeles_alien_3 = QPixmap(ruta_alien_3)
        cuadro = QPixmap(20 + p.LARGO_PRIMER_MUNDO, 20 + p.ALTO_PRIMER_MUNDO)
        cuadro.fill(QColor("darkslateblue"))

        self.fondo = QLabel(self)
        self.fondo.setGeometry(-500, 0, 500 + p.LARGO_VENTANA_PRINCIPAL,
                               655 + p.ALTO_VENTANA_PRINCIPAL)
        self.fondo.setPixmap(pixeles_jupiter)
        self.fondo.setScaledContents(True)


        self.cuadro_luna = QLabel(self)
        self.cuadro_luna.setPixmap(cuadro)
        self.cuadro_luna.move(p.POSICIÓN_X_PRIMER_MUNDO-10, p.POSICIÓN_Y_PRIMER_MUNDO-10)

        self.imagen_luna = QLabel(self)
        self.imagen_luna.setGeometry(p.POSICIÓN_X_PRIMER_MUNDO,
                                     p.POSICIÓN_Y_PRIMER_MUNDO,
                                     p.LARGO_PRIMER_MUNDO,
                                     p.ALTO_PRIMER_MUNDO)
        self.imagen_luna.setPixmap(pixeles_luna)
        self.imagen_luna.setScaledContents(True)


        self.cuadro_jupiter = QLabel(self)
        self.cuadro_jupiter.setPixmap(cuadro)
        self.cuadro_jupiter.move((p.POSICIÓN_X_PRIMER_MUNDO*7)-10, p.POSICIÓN_Y_PRIMER_MUNDO-10)

        self.imagen_jupiter = QLabel(self)
        self.imagen_jupiter.setGeometry(p.POSICIÓN_X_PRIMER_MUNDO*7,
                                        p.POSICIÓN_Y_PRIMER_MUNDO,
                                        p.LARGO_PRIMER_MUNDO,
                                        p.ALTO_PRIMER_MUNDO)
        self.imagen_jupiter.setPixmap(pixeles_jupiter)
        self.imagen_jupiter.setScaledContents(True)


        self.cuadro_galaxia = QLabel(self)
        self.cuadro_galaxia.setPixmap(cuadro)
        self.cuadro_galaxia.move((p.POSICIÓN_X_PRIMER_MUNDO*13)-10, p.POSICIÓN_Y_PRIMER_MUNDO-10)

        self.imagen_galaxia = QLabel(self)
        self.imagen_galaxia.setGeometry(p.POSICIÓN_X_PRIMER_MUNDO*13,
                                        p.POSICIÓN_Y_PRIMER_MUNDO,
                                        p.LARGO_PRIMER_MUNDO,
                                        p.ALTO_PRIMER_MUNDO)
        self.imagen_galaxia.setPixmap(pixeles_galaxia)
        self.imagen_galaxia.setScaledContents(True)

        self.alien_1 = QLabel(self)
        self.alien_1.setGeometry((p.POSICIÓN_X_PRIMER_MUNDO +
                                  p.LARGO_PRIMER_MUNDO)-30, 370, 40, 40)
        self.alien_1.setPixmap(pixeles_alien_1)
        self.alien_1.setScaledContents(True)

        self.alien_2 = QLabel(self)
        self.alien_2.setGeometry(((p.POSICIÓN_X_PRIMER_MUNDO +
                                   p.LARGO_PRIMER_MUNDO)*2)-30, 370, 40, 40)
        self.alien_2.setPixmap(pixeles_alien_2)
        self.alien_2.setScaledContents(True)

        self.alien_3 = QLabel(self)
        self.alien_3.setGeometry(((p.POSICIÓN_X_PRIMER_MUNDO
                                   + p.LARGO_PRIMER_MUNDO)*3)-30, 370, 40, 40)
        self.alien_3.setPixmap(pixeles_alien_3)
        self.alien_3.setScaledContents(True)

        self._boton_volver = QPushButton("Volver a la pantalla de título", self)
        self._boton_volver.setFont(QFont(p.FUENTE, 12))
        self._boton_volver.move(25, 25)
        self._boton_volver.clicked.connect(self.volver)
        self.boton_volver.installEventFilter(self)

        self.título = QLabel("   ELIGE EL LUGAR DE LA CACERÍA", self)
        self.título.setFont(QFont(p.FUENTE, 25))
        self.título.setGeometry(452, 42, 429, 55)

        self.grupo_botones = QButtonGroup(self)
        self.grupo_botones.setExclusive(False)

        self.botón_selección_luna = QRadioButton("  TUTORIAL LUNAR", self)
        self.botón_selección_luna.setFont(QFont(p.FUENTE, 18))
        self.botón_selección_luna.setGeometry(p.POSICIÓN_X_PRIMER_MUNDO,
                                              p.POSICIÓN_Y_PRIMER_MUNDO+225, 185, 35)
        self.botón_selección_luna.setStyleSheet("background-color: darkslateblue")
        self.grupo_botones.addButton(self.botón_selección_luna)
        self.botón_selección_luna.clicked.connect(self.deschequear_otros_luna)

        self.botón_selección_jupiter = QRadioButton("  ENTRENAMIENTO EN JÚPITER", self)
        self.botón_selección_jupiter.setFont(QFont(p.FUENTE, 18))
        self.botón_selección_jupiter.setGeometry(p.POSICIÓN_X_PRIMER_MUNDO * 7,
                                                 p.POSICIÓN_Y_PRIMER_MUNDO+225, 280, 35)
        self.botón_selección_jupiter.setStyleSheet("background-color: darkslateblue")
        self.grupo_botones.addButton(self.botón_selección_jupiter)
        self.botón_selección_jupiter.clicked.connect(self.deschequear_otros_jupiter)

        self.botón_selección_invasion = QRadioButton("  INVASIÓN INTERGALÁCTICA", self)
        self.botón_selección_invasion.setFont(QFont(p.FUENTE, 18))
        self.botón_selección_invasion.setGeometry(p.POSICIÓN_X_PRIMER_MUNDO*13,
                                                  p.POSICIÓN_Y_PRIMER_MUNDO+225, 260, 35)
        self.botón_selección_invasion.setStyleSheet("background-color: darkslateblue")
        self.grupo_botones.addButton(self.botón_selección_invasion)
        self.botón_selección_invasion.clicked.connect(self.deschequear_otros_invasion)

        self.edit_nombre = QLineEdit("", self)
        self.edit_nombre.setFont(QFont(p.FUENTE, 12))
        self.edit_nombre.setStyleSheet("color: white")
        self.edit_nombre.setGeometry(110, 502, 355, 35)

        self.instrucción_usuario = QLabel("  ¿Cuál es tu nombre, Cazador Espacial?", self)
        self.instrucción_usuario.setFont(QFont(p.FUENTE, 18))
        self.instrucción_usuario.setGeometry(80, 470, 385, 35)

        self._boton_ingresar = QPushButton(" Ingresar", self)
        self._boton_ingresar.setFont(QFont(p.FUENTE, 22))
        self._boton_ingresar.setGeometry(580, 565, 160, 60)
        self._boton_ingresar.clicked.connect(self.ingresar)
        self.boton_ingresar.installEventFilter(self)

        self.error_nombre = QLabel("", self)
        self.error_nombre.setFont(QFont(p.FUENTE, 14))
        self.error_nombre.move(120, 544)
        self.error_nombre.setStyleSheet("background-color: transparent")

        self.error_selección = QLabel("  Selecciona un mundo para la cacería.", self)
        self.error_selección.setFont(QFont(p.FUENTE, 20))
        self.error_selección.setGeometry(870, 480, 394, 40)
        self.error_selección.setStyleSheet("background-color: transparent")

    def ingresar(self):
        self.senal_enviar_nombre.emit(self.edit_nombre.text())
        self.senal_enviar_seleccion.emit(self.botón_selección_luna.isChecked(),
                                         self.botón_selección_jupiter.isChecked(),
                                         self.botón_selección_invasion.isChecked())

    @property
    def boton_ingresar(self):
        return self._boton_ingresar

    @property
    def boton_volver(self):
        return self._boton_volver

    def eventFilter(self, obj, event):
        if obj is self._boton_volver and event.type() == QEvent.KeyPress:
            return True
        if obj is self._boton_ingresar and event.type() == QEvent.KeyPress:
            return True
        return super().eventFilter(obj, event)

    def ingreso_nombre(self, bien, nombre):
        if not bien and nombre == "vacío":
            self.error_nombre.setText(" Escribe tu nombre Cazador.")
            self.error_nombre.setStyleSheet("background-color: darkslateblue")
            self.error_nombre.setGeometry(120, 544, 200, 30)
            self.error_nombre.repaint()
        else:
            if bien:
                self.nombre = nombre
                self.abrir_juego()
            else:
                self.error_nombre.setText(" Solo números y letras Cazador.")
                self.error_nombre.setStyleSheet("background-color: darkslateblue")
                self.error_nombre.setGeometry(120, 544, 229, 30)
                self.error_nombre.repaint()

    def ingreso_seleccion(self, hay_elección, destino):
        if not hay_elección:
            self.error_selección.setStyleSheet("background-color: darkslateblue")
            self.error_selección.repaint()
        else:
            self.destino = destino
            self.abrir_juego()

    def abrir_juego(self):
        if self.nombre and self.destino:
            self.botón_selección_luna.setChecked(False)
            self.botón_selección_jupiter.setChecked(False)
            self.botón_selección_invasion.setChecked(False)

            self.botón_selección_luna.repaint()
            self.botón_selección_jupiter.repaint()
            self.botón_selección_invasion.repaint()

            self.error_nombre.setStyleSheet("background-color: transparent")
            self.error_nombre.setText("")
            self.error_nombre.repaint()

            self.error_selección.setStyleSheet("background-color: transparent")
            self.error_selección.repaint()

            self.senal_abrir_juego.emit(self.nombre, self.destino)

            self.hide()

            self.nombre = False
            self.destino = False

    def abrir_ventana(self):
        self.show()

    def volver(self):
        self.botón_selección_luna.setChecked(False)
        self.botón_selección_jupiter.setChecked(False)
        self.botón_selección_invasion.setChecked(False)

        self.botón_selección_luna.repaint()
        self.botón_selección_jupiter.repaint()
        self.botón_selección_invasion.repaint()

        self.error_nombre.setStyleSheet("background-color: transparent")
        self.error_nombre.setText("")
        self.error_nombre.repaint()

        self.error_selección.setStyleSheet("background-color: transparent")
        self.error_selección.repaint()

        self.edit_nombre.setText("")
        self.edit_nombre.repaint()

        self.nombre = False
        self.destino = False

        self.hide()
        self.senal_volver.emit()

    def deschequear_otros_luna(self):
        self.botón_selección_invasion.setChecked(False)
        self.botón_selección_jupiter.setChecked(False)
        self.botón_selección_invasion.repaint()
        self.botón_selección_jupiter.repaint()

    def deschequear_otros_jupiter(self):
        self.botón_selección_luna.setChecked(False)
        self.botón_selección_invasion.setChecked(False)
        self.botón_selección_luna.repaint()
        self.botón_selección_invasion.repaint()

    def deschequear_otros_invasion(self):
        self.botón_selección_luna.setChecked(False)
        self.botón_selección_jupiter.setChecked(False)
        self.botón_selección_luna.repaint()
        self.botón_selección_jupiter.repaint()

    def mousePressEvent(self, event):
        if p.POSICIÓN_X_PRIMER_MUNDO - 10 < event.x() < \
                p.POSICIÓN_X_PRIMER_MUNDO + p.LARGO_PRIMER_MUNDO + 10:
            if p.POSICIÓN_Y_PRIMER_MUNDO-10 < event.y() < \
                    p.POSICIÓN_Y_PRIMER_MUNDO + p.ALTO_PRIMER_MUNDO + 10:
                if not self.botón_selección_luna.isChecked():
                    self.botón_selección_luna.setChecked(True)
                else:
                    self.botón_selección_luna.setChecked(False)

                if self.botón_selección_jupiter.isChecked():
                    self.botón_selección_jupiter.setChecked(False)
                    self.botón_selección_jupiter.repaint()
                if self.botón_selección_invasion.isChecked():
                    self.botón_selección_invasion.setChecked(False)
                    self.botón_selección_invasion.repaint()

        if p.POSICIÓN_X_PRIMER_MUNDO * 7 - 10 < event.x() < \
                (p.POSICIÓN_X_PRIMER_MUNDO * 7 + p.LARGO_PRIMER_MUNDO + 10):
            if p.POSICIÓN_Y_PRIMER_MUNDO - 10 < event.y() < \
                    p.POSICIÓN_Y_PRIMER_MUNDO + p.ALTO_PRIMER_MUNDO + 10:
                if not self.botón_selección_jupiter.isChecked():
                    self.botón_selección_jupiter.setChecked(True)
                else:
                    self.botón_selección_jupiter.setChecked(False)

                if self.botón_selección_luna.isChecked():
                    self.botón_selección_luna.setChecked(False)
                    self.botón_selección_luna.repaint()

                if self.botón_selección_invasion.isChecked():
                    self.botón_selección_invasion.setChecked(False)
                    self.botón_selección_invasion.repaint()

        if p.POSICIÓN_X_PRIMER_MUNDO * 13 - 10 < event.x() < \
                (p.POSICIÓN_X_PRIMER_MUNDO * 13 + p.LARGO_PRIMER_MUNDO + 10):
            if p.POSICIÓN_Y_PRIMER_MUNDO - 10 < event.y() < \
                    p.POSICIÓN_Y_PRIMER_MUNDO + p.ALTO_PRIMER_MUNDO + 10:
                if not self.botón_selección_invasion.isChecked():
                    self.botón_selección_invasion.setChecked(True)
                else:
                    self.botón_selección_invasion.setChecked(False)

                if self.botón_selección_luna.isChecked():
                    self.botón_selección_luna.setChecked(False)
                    self.botón_selección_luna.repaint()

                if self.botón_selección_jupiter.isChecked():
                    self.botón_selección_jupiter.setChecked(False)
                    self.botón_selección_jupiter.repaint()

    def borrar_nombre(self):
        self.edit_nombre.setText("")
