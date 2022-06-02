from PyQt5.QtCore import pyqtSignal, QObject


class LogicaPrincipal(QObject):

    senal_status_nombre = pyqtSignal(bool, str)
    senal_status_eleccion = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()

    def revisar_nombre(self, nombre):

        if nombre == "":
            self.senal_status_nombre.emit(False, "vacío")
        else:
            if nombre.isalnum():
                self.senal_status_nombre.emit(True, nombre)
            else:
                self.senal_status_nombre.emit(False, "noalphanum")

    def revisar_seleccion(self, boton_luna, boton_jupiter, boton_invasion):
        if not (boton_luna or boton_jupiter or boton_invasion):
            self.senal_status_eleccion.emit(False, "ninguno")
        else:
            if boton_luna:
                self.senal_status_eleccion.emit(True, "luna")
            elif boton_jupiter:
                self.senal_status_eleccion.emit(True, "júpiter")
            else:
                self.senal_status_eleccion.emit(True, "galaxia")
