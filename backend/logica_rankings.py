from PyQt5.QtCore import pyqtSignal, QObject


def enteros(lista):
    return lista[1]


class LogicaRankings(QObject):

    senal_ranking = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def puntajes_altos(self):
        lista_jugadores = []
        self.datos_jugadores = []
        with open("puntajes.txt", encoding="UTF-8") as puntajes:
            for puntaje in puntajes.readlines():
                if puntaje != "\n":
                    info = puntaje.rstrip("\n").split(",")
                    info[1] = int(info[1])
                    lista_jugadores.append(info)

        lista_jugadores.sort(key=enteros, reverse=True)
        for i in range(min(5, len(lista_jugadores))):
            self.datos_jugadores.append(lista_jugadores[i])

        self.senal_ranking.emit(self.datos_jugadores)
