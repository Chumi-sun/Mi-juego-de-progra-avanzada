from PyQt5.QtWidgets import QApplication

from backend.logica_rankings import LogicaRankings
from backend.logica_post_juego import LogicaPostJuego
from backend.logica_juego import LogicaJuego
from backend.logica_principal import LogicaPrincipal

from frontend.ventana_juego import VentanaJuego
from frontend.ventana_post_juego import VentanaPostJuego
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_rankings import VentanaRankings
from frontend.ventana_principal import VentanaPrincipal


if __name__ == "__main__":
    app = QApplication([])

    # Backend
    logica_rankings = LogicaRankings()
    logica_principal = LogicaPrincipal()
    logica_juego = LogicaJuego()
    logica_post_juego = LogicaPostJuego()

    # Frontend
    ventana_inicio = VentanaInicio()
    ventana_rankings = VentanaRankings()
    ventana_principal = VentanaPrincipal()
    ventana_juego = VentanaJuego()
    ventana_post_juego = VentanaPostJuego()

    # señales
    ventana_inicio.senal_abrir_rankings.connect(ventana_rankings.abrir_ventana)
    ventana_inicio.senal_consultar_puntajes_altos.connect(logica_rankings.puntajes_altos)
    ventana_inicio.senal_abrir_ventana_principal.connect(ventana_principal.abrir_ventana)

    ventana_rankings.senal_abrir_inicio.connect(ventana_inicio.abrir_ventana)
    logica_rankings.senal_ranking.connect(ventana_rankings.colocar_texto_etiquetas_puntajes)

    ventana_principal.senal_volver.connect(ventana_inicio.abrir_ventana)
    ventana_principal.senal_enviar_nombre.connect(logica_principal.revisar_nombre)
    ventana_principal.senal_enviar_seleccion.connect(logica_principal.revisar_seleccion)
    ventana_principal.senal_abrir_juego.connect(logica_juego.iniciar_juego)

    logica_principal.senal_status_nombre.connect(ventana_principal.ingreso_nombre)
    logica_principal.senal_status_eleccion.connect(ventana_principal.ingreso_seleccion)

    logica_juego.senal_escenario_escogido.connect(ventana_juego.crear_objetos)
    logica_juego.senal_datos_juego.connect(ventana_juego.actualizar_datos)
    logica_juego.senal_cambio_mira_telescopica.connect(ventana_juego.mover_mira)
    logica_juego.senal_acabar_juego.connect(ventana_juego.acabar_juego)
    logica_juego.senal_enviar_datos_post_juego.connect(logica_post_juego.crear_objetos)
    logica_juego.senal_ronda_acabada.connect(ventana_juego.cambiar_ronda)

    ventana_juego.senal_volver_a_ventana_principal.connect(ventana_principal.abrir_ventana)
    ventana_juego.senal_volver_a_ventana_inicio.connect(ventana_inicio.abrir_ventana)
    ventana_juego.senal_pausar.connect(logica_juego.pausar)
    ventana_juego.senal_tecla.connect(logica_juego.mover_mira)
    ventana_juego.senal_detener_timers.connect(logica_juego.detener_timers)
    ventana_juego.senal_disparo.connect(logica_juego.disparar)
    ventana_juego.senal_resetear_puntaje.connect(logica_juego.borrar_puntaje)
    ventana_juego.senal_borrar_nombre.connect(ventana_principal.borrar_nombre)
    ventana_juego.senal_guardar_puntaje.connect(logica_post_juego.registrar_nombre)
    ventana_juego.senal_cheatcode_cia.connect(logica_juego.cheatcode_cia)
    ventana_juego.senal_balas_infinitas.connect(logica_juego.cheatcode_balas_infinitas)

    logica_post_juego.senal_abrir_ventana_post_juego.connect(ventana_post_juego.recibir_objetos)
    logica_post_juego.senal_salir.connect(ventana_inicio.abrir_ventana)
    logica_post_juego.senal_cerrar_post_juego.connect(ventana_post_juego.cerrar_ventana)
    logica_post_juego.senal_borrar_puntaje.connect(logica_juego.borrar_puntaje)
    logica_post_juego.senal_siguiente_nivel.connect(logica_juego.siguiente_nivel)
    logica_post_juego.senal_borrar_nombre.connect(ventana_principal.borrar_nombre)

    # Ejecución
    ventana_inicio.show()
    app.exec()
