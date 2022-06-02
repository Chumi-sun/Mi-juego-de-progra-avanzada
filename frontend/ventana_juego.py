import sys
from math import ceil
sys.path.append("..")

from time import sleep

from PyQt5.QtCore import QTimer, pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QProgressBar
import parametros as p


class VentanaJuego(QWidget):

    senal_volver_a_ventana_principal = pyqtSignal()
    senal_volver_a_ventana_inicio = pyqtSignal()
    senal_iniciar_juego = pyqtSignal()
    senal_tecla = pyqtSignal(int, tuple)
    senal_pausar = pyqtSignal()
    senal_detener_timers = pyqtSignal()
    senal_disparo = pyqtSignal(int, int, list)
    senal_resetear_puntaje = pyqtSignal()
    senal_borrar_nombre = pyqtSignal()
    senal_guardar_puntaje = pyqtSignal(str, int)
    senal_balas_infinitas = pyqtSignal()
    senal_cheatcode_cia = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 100, p.LARGO_VENTANA_PRINCIPAL, p.ALTO_VENTANA_PRINCIPAL + 100)
        self.setFixedSize(p.LARGO_VENTANA_PRINCIPAL, p.ALTO_VENTANA_PRINCIPAL + 100)
        self.setStyleSheet("background-color: transparent")
        self.mira_telescopica = ""
        self._botón_pausa = ""
        self._botón_volver = ""
        self._botón_salir = ""
        self.ultimas_cuatro_teclas = [0, 0, 0, 0]

    def crear_objetos(self, lista):
        self.lista_aliens = []
        self.intervalo_aliens = 2
        self.pausa = False
        self.fondo = lista[0]
        self.setWindowTitle(lista[1])
        self.lista_aliens = lista[2]
        self.perro = lista[3]
        self.etiqueta_ganaste = lista[4]
        self.nivel = lista[5]
        self.puntaje_acumulado = lista[6]
        self.nombre = lista[7]
        self.numero_de_balas = 0

        self.acabado = False
        self.balas_infinitas = False

        self.fondo.setParent(self)
        self.etiqueta_ganaste.etiqueta.setParent(self)
        self.perro.perro_etiqueta.setParent(self)

        for i in range(len(self.lista_aliens)):
            alien = self.lista_aliens[i]
            alien.alien_etiqueta.setParent(self)
            alien.actualizar.connect(alien.mover_etiqueta)
            if i < 2:
                alien.aparecer_alien.start()
                alien.start()

        ruta_imagen_bala = p.RUTA_IMAGEN_BALA
        pixeles_imagen_bala = QPixmap(ruta_imagen_bala)

        ruta_x_pixelada = p.RUTA_X_PIXELADA
        pixeles_gran_x = QPixmap(ruta_x_pixelada)

        ruta_mira_telescopica_negra = p.RUTA_MIRA_TELESCOPICA_NEGRA
        ruta_mira_telescopica_roja = p.RUTA_MIRA_TELESCOPICA_ROJA

        self.pixeles_mira_telescopica_negra = QPixmap(ruta_mira_telescopica_negra)
        self.pixeles_mira_telescopica_roja = QPixmap(ruta_mira_telescopica_roja)

        if self.mira_telescopica == "":
            self.mira_telescopica = QLabel(self)
            self.mira_telescopica.setPixmap(self.pixeles_mira_telescopica_negra)
            self.mira_telescopica.setGeometry(500, 200, 300, 200)
            self.mira_telescopica.setStyleSheet("background-color: transparent")
            self.mira_telescopica.setScaledContents(True)
        self.mira_telescopica.move(500, 200)
        self.mira_telescopica.raise_()

        rectángulo = QPixmap(p.LARGO_VENTANA_PRINCIPAL, p.ALTO_VENTANA_PRINCIPAL * 0.26)
        rectángulo.fill(QColor("darkslateblue"))

        self.barra_inferior = QLabel(self)
        self.barra_inferior.setPixmap(rectángulo)
        self.barra_inferior.move(0, p.ALTO_VENTANA_PRINCIPAL * 0.9)

        self.etiqueta_tiempo = QLabel("Tiempo restante", self)
        self.etiqueta_tiempo.setFont(QFont(p.FUENTE, 16))
        self.etiqueta_tiempo.move(30, p.ALTURA_ETIQUETAS_NOMBRES_JUEGO)

        self.barra_tiempo = QProgressBar(self)
        self.barra_tiempo.setGeometry(40, 690, 240, 20)
        self.barra_tiempo.setStyleSheet(u"QProgressBar{"
                                        "background-color: rgb(98, 114, 164);"
                                        "color: rgb(200, 200, 200);"
                                        "border-radius: 2px;"
                                        "}"
                                        "QProgressBar::chunk{"
                                        "border-radius: 2px;"
                                        "background-color: qlineargradient"
                                        "(spread:pad, x1:0, y1:0, x2:0.943182,"
                                        " y2:0, stop:0 rgba(254, 121, 199, 255),"
                                        " stop:1 rgba(170, 85, 255, 255));"
                                        "}")

        self.barra_tiempo.setTextVisible(False)

        self.texto_barra = QLabel("0", self)
        self.texto_barra.setFont(QFont(p.FUENTE, 20))
        self.texto_barra.setGeometry(300, 679, 60, 40)

        self.etiqueta_balas = QLabel("Balas", self)
        self.etiqueta_balas.setFont(QFont(p.FUENTE, 16))
        self.etiqueta_balas.move(360, p.ALTURA_ETIQUETAS_NOMBRES_JUEGO)

        self.imagen_bala = QLabel(self)
        self.imagen_bala.setGeometry(365, 665, 40, 80)
        self.imagen_bala.setPixmap(pixeles_imagen_bala)
        self.imagen_bala.setScaledContents(True)

        self.gran_x = QLabel(self)
        self.gran_x.setGeometry(415, 688, 40, 40)
        self.gran_x.setPixmap(pixeles_gran_x)
        self.gran_x.setScaledContents(True)

        self.cuanta_balas_quedan = QLabel(str(p.BALAS_INICIALES), self)
        self.cuanta_balas_quedan.setGeometry(470, 667, 110, 80)
        self.cuanta_balas_quedan.setFont(QFont(p.FUENTE, 40))

        self.etiqueta_puntaje = QLabel("Puntaje", self)
        self.etiqueta_puntaje.setFont(QFont(p.FUENTE, 16))
        self.etiqueta_puntaje.move(600, p.ALTURA_ETIQUETAS_NOMBRES_JUEGO)

        self.puntaje_actual = QLabel("0 puntos", self)
        self.puntaje_actual.setFont(QFont(p.FUENTE, 30))
        self.puntaje_actual.setGeometry(615, 680, 240, 60)

        self.etiqueta_nivel = QLabel("Nivel", self)
        self.etiqueta_nivel.setFont(QFont(p.FUENTE, 16))
        self.etiqueta_nivel.move(850, p.ALTURA_ETIQUETAS_NOMBRES_JUEGO)

        self.nivel_actual = QLabel("1", self)
        self.nivel_actual.setFont(QFont(p.FUENTE, 40))
        self.nivel_actual.setGeometry(865, 667, 100, 80)

        self.aliens_restantes = QLabel("2", self)
        self.aliens_restantes.setFont(QFont(p.FUENTE, 20))
        self.aliens_restantes.setStyleSheet("background-color: transparent")
        self.aliens_restantes.setStyleSheet("color: red")
        self.aliens_restantes.setGeometry(10, 10, 80, 30)

        if self._botón_pausa == "":
            self._botón_pausa = QPushButton("Pausa", self)
            self._botón_pausa.setFont(QFont(p.FUENTE, 20))
            self._botón_pausa.setStyleSheet("background-color: dimgray")
            self._botón_pausa.setGeometry(1070, 615, 180, 40)
            self._botón_pausa.clicked.connect(self.pausar)
            self.botón_pausa.installEventFilter(self)
        else:
            self._botón_pausa.raise_()

        if self._botón_volver == "":
            self._botón_volver = QPushButton("Volver", self)
            self._botón_volver.setFont(QFont(p.FUENTE, 20))
            self._botón_volver.setGeometry(1070, 665, 180, 40)
            self._botón_volver.setStyleSheet("background-color: dimgray")
            self._botón_volver.clicked.connect(self.volver_a_ventana_principal)
            self.botón_volver.installEventFilter(self)
        else:
            self._botón_volver.raise_()

        if self._botón_salir == "":
            self._botón_salir = QPushButton("Salir", self)
            self._botón_salir.setFont(QFont(p.FUENTE, 20))
            self._botón_salir.setGeometry(1070, 715, 180, 40)
            self._botón_salir.setStyleSheet("background-color: brown")
            self._botón_salir.clicked.connect(self.ventana_inicio)
            self.botón_salir.installEventFilter(self)
        else:
            self._botón_salir.raise_()

        self.etiqueta_ganaste.etiqueta.raise_()

        if self.nivel > 1:
            self.actualizar_etiquetas_por_paso_de_nivel()

        self.abrir_ventana()

    @property
    def botón_pausa(self):
        return self._botón_pausa

    @property
    def botón_volver(self):
        return self._botón_volver

    @property
    def botón_salir(self):
        return self._botón_salir

    def eventFilter(self, objeto, evento):
        if objeto is self._botón_pausa and evento.type() == QEvent.KeyPress:
            self.keyPressEvent(evento)
            return True
        if objeto is self._botón_volver and evento.type() == QEvent.KeyPress:
            self.keyPressEvent(evento)
            return True
        if objeto is self._botón_salir and evento.type() == QEvent.KeyPress:
            self.keyPressEvent(evento)
            return True
        return super().eventFilter(objeto, evento)

    def keyPressEvent(self, evento):
        tecla = evento.key()
        if tecla == 80:
            self.pausar()
        for i in range(4):
            if i < 3:
                self.ultimas_cuatro_teclas[i] = self.ultimas_cuatro_teclas[i+1]
            else:
                self.ultimas_cuatro_teclas[i] = tecla
        if [79, 86, 78, 73] == self.ultimas_cuatro_teclas:
            self.senal_balas_infinitas.emit()
            self.balas_infinitas = True
        if self.ultimas_cuatro_teclas[1] == 67 and self.ultimas_cuatro_teclas[2] == 73:
            if self.ultimas_cuatro_teclas[3] == 65:
                self.senal_cheatcode_cia.emit()
        if not self.pausa:
            if tecla == 87 or tecla == 65 or tecla == 83 or tecla == 68:
                x = self.mira_telescopica.x()
                y = self.mira_telescopica.y()
                self.senal_tecla.emit(tecla, (x, y))
            if tecla == 32:
                self.cambiar_color_mira(True)
                self.senal_disparo.emit(self.mira_telescopica.x(),
                                        self.mira_telescopica.y(), self.lista_aliens)

    def cambiar_color_mira(self, cambiar_color):
        if self.cuanta_balas_quedan.text() != "0":
            if cambiar_color:
                self.mantener_el_rojo = QTimer(self)
                self.mantener_el_rojo.setInterval(p.DURACIÓN_MIRA_ROJA * 1000)
                self.mantener_el_rojo.setSingleShot(True)
                self.mantener_el_rojo.start()

                self.mira_telescopica.setPixmap(self.pixeles_mira_telescopica_roja)

                self.mantener_el_rojo.timeout.connect(self.cambiar_color_mira_2)
            else:
                self.mira_telescopica.setPixmap(self.pixeles_mira_telescopica_negra)
        if self.cuanta_balas_quedan.text() == "0" or self.acabado:
            self.mira_telescopica.setPixmap(self.pixeles_mira_telescopica_negra)

    def cambiar_color_mira_2(self):
        self.mantener_el_rojo.stop()
        self.cambiar_color_mira(False)

    def mover_mira(self, posicion):
        self.mira_telescopica.move(*posicion)
        self.mira_telescopica.repaint()

    def cambiar_ronda(self):
        for i in range(self.intervalo_aliens, self.intervalo_aliens+2):
            alien = self.lista_aliens[i]
            alien.aparecer_alien.start()
            sleep(0.02)
            alien.start()
        self.intervalo_aliens += 2

    def actualizar_datos(self, lista):
        tiempo = lista[0]
        balas = lista[1]
        duracion = lista[2]
        aliens_restantes = lista[3]
        if not self.acabado:
            self.barra_tiempo.setValue(int((((duracion * 1000) - tiempo) / (duracion * 1000))
                                           * 100))
            self.texto_barra.setText(f"{(ceil(tiempo/1000)):,}".replace(",", "."))
            self.barra_tiempo.repaint()

            if not self.balas_infinitas:
                self.cuanta_balas_quedan.setText(f"{balas:,}".replace(",", "."))
                self.cuanta_balas_quedan.repaint()

            self.aliens_restantes.setText(str(aliens_restantes))
            self.aliens_restantes.repaint()

    def abrir_ventana(self):
        self.show()

    def acabar_juego(self, lista):
        tiempo_restante = lista[0]
        balas_restantes = lista[1]
        ganar = lista[2]

        if ganar and ganar != "cheatcode":
            self.cuanta_balas_quedan.setText(str(int(self.cuanta_balas_quedan.text())-1))
            self.aliens_restantes.setText(str(int(self.aliens_restantes.text())-1))
            self.perro.start()
            for i in range(len(self.lista_aliens)):
                sleep(0.01)
                alien = self.lista_aliens[i]
                alien.matar_alien.start()
            self.etiqueta_ganaste.start()
            sleep(p.TIEMPO_TERMINATOR_DOG)
        if not tiempo_restante:
            self.barra_tiempo.setValue(100)
            self.texto_barra.setText("0")
        else:
            self.senal_detener_timers.emit()
        if not balas_restantes:
            self.cuanta_balas_quedan.setText("0")

        self.acabado = True
        for alien in self.lista_aliens:
            if alien.vivo:
                alien.vivo = False
        self.etiqueta_ganaste.etiqueta.setStyleSheet("background-color: transparent")
        self.clear_etiquetas()

        self.hide()

    def pausar(self):
        if not self.acabado:
            self.pausa = not self.pausa
            for alien in self.lista_aliens:
                alien.pausa = not alien.pausa
                if not alien.pausa:
                    alien.start()
            self.senal_pausar.emit()

    def volver_a_ventana_principal(self):
        if not self.acabado:
            self.senal_volver_a_ventana_principal.emit()
            self.senal_detener_timers.emit()
            self.hide()
            self.clear_etiquetas()
            self.senal_guardar_puntaje.emit(self.nombre, self.puntaje_acumulado)
            self.puntaje_acumulado = 0
            self.nivel = 1
            self.senal_resetear_puntaje.emit()

    def ventana_inicio(self):
        if not self.acabado:
            self.hide()
            self.senal_volver_a_ventana_inicio.emit()
            self.clear_etiquetas()
            self.senal_detener_timers.emit()
            self.puntaje_acumulado = 0
            self.nivel = 1
            self.senal_resetear_puntaje.emit()
            self.senal_borrar_nombre.emit()
            self.senal_guardar_puntaje.emit(self.nombre, self.puntaje_acumulado)

    def actualizar_etiquetas_por_paso_de_nivel(self):
        self.puntaje_actual.setText(f"{self.puntaje_acumulado:,}".replace(",", ".")+" puntos")
        self.nivel_actual.setText(str(self.nivel))
        self.aliens_restantes.clear()

    def clear_etiquetas(self):
        self.perro.perro_etiqueta.clear()
        for alien in self.lista_aliens:
            alien.alien_etiqueta.clear()
        self.etiqueta_ganaste.etiqueta.clear()
        self.fondo.clear()
        self.barra_inferior.clear()
        self.barra_inferior.clear()
        self.nivel_actual.clear()
        self.puntaje_actual.clear()
        self.gran_x.clear()
        self.imagen_bala.clear()
        self.cuanta_balas_quedan.clear()
        self.aliens_restantes.clear()
        self.etiqueta_ganaste = ""
        self.perro = ""
        self.lista_aliens = ""
