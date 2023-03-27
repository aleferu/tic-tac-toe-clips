#!/usr/bin/env python3


# imports
import numpy as np
import clips
from rules import custom_rules


def pregunta_otra_partida():
    respuesta_valida = False
    respuesta = False
    print('\n¿Desea jugar otra partida?')
    print('Entradas válidas para jugar otra partida: s, S, si, Sí')
    print('Entradas válidas para no jugar otra partida: n, N, no, No')
    while not respuesta_valida:
        respuesta = input('Escriba aquí: ')
        if respuesta in {'s', 'S', 'si', 'Sí'}:
            respuesta = True
            respuesta_valida = True
        elif respuesta in {'n', 'N', 'no', 'No'}:
            respuesta = False
            respuesta_valida = True
        else:
            print('Entrada no válida, por favor, inténtelo de nuevo')
    return respuesta


def tirada_maquina(tablero):
    env = clips.Environment()
    template_casilla = """
        (deftemplate casilla
        (slot coord_x (type INTEGER))           
        (slot coord_y (type INTEGER))
        (slot tipo (type INTEGER))
        (slot elegida (type INTEGER)))
        """
    env.build(template_casilla)
    template_casilla = env.find_template("casilla") # shadowing a propósito
    for coord_x in range(3):
        for coord_y in range(3):
            template_casilla.assert_fact(coord_x=coord_x, 
                                         coord_y=coord_y, 
                                         tipo=int(tablero[coord_x, coord_y]),
                                         elegida=0)
    for rule in custom_rules:
        env.build(rule)

    env.run()

    debug = True
    if debug:
        for f in env.facts():
            print(f)
    maximo = ((0, 0), 0)
    for f in env.facts():
        if f.template == template_casilla:
            if maximo[1] < f["elegida"]:
                maximo = ((f["coord_x"], f["coord_y"]), f["elegida"])
    return maximo[0]


def determina_si_ganador(jugador, tablero):
    a_buscar = -1
    if jugador == 'usuario':
        a_buscar = 1
    elif jugador == 'máquina':
        a_buscar = 2

    for i in range(3):
        if (tablero[i] == a_buscar).all():
            return True
        if (tablero[:, i] == a_buscar).all():
            return True
    if (tablero[::, ::-1].diagonal() == a_buscar).all():
        return True
    return (tablero.diagonal() == a_buscar).all()


def muestra_tablero(tablero):
    mapping = {0: ' ', 1: 'x', 2: 'o'}
    dibujar_linea = lambda: print('-------')
    dibujar_linea()
    for coord_x in range(3):
        for coord_y in range(3):
            print(f'|{mapping[tablero[coord_x, coord_y]]}', end='')
        print('|')
        dibujar_linea()


def pregunta_coordenadas_tirada(tablero):
    respuesta_valida_x, respuesta_valida_y = False, False
    coord_x, coord_y = 0, 0

    print('\n¡Le toca!')
    while not respuesta_valida_x:
        coord_x = input(f'Introduzca la coordenada x [Rango 0-2]: ')
        try:
            coord_x = int(coord_x)
            if coord_x < 0 or coord_x > 2:
                raise Exception()
            respuesta_valida_x = True
        except:
            print('Valor no válido para la coordenada x, inténtelo de nuevo.')

    while not respuesta_valida_y:
        coord_y = input(f'Introduzca la coordenada y [Rango 0-2]: ')
        try:
            coord_y = int(coord_y)
            if coord_y < 0 or coord_y > 2:
                raise Exception()
            respuesta_valida_y = True
        except:
            print('Valor no válido para la coordenada y, inténtelo de nuevo.')

    if tablero[coord_x, coord_y] != 0:
        print(f'El tablero ya está ocupado en {(coord_x, coord_y)}, inténtelo de nuevo.')
        (coord_x, coord_y) = pregunta_coordenadas_tirada(tablero)

    return (coord_x, coord_y)


def pregunta_quien_empieza():
    respuesta_valida = False
    respuesta = ''
    print('\n¿Quién empieza: usuario (cruces) o máquina (círculos)?')
    print('Entradas válidas para que empiece el usuario: u, U, x')
    print('Entradas válidas para que empiece la máquina: m, M, o')
    while not respuesta_valida:
        respuesta = input('¿Quién empieza? Escriba aquí: ')
        if respuesta in {'u', 'U', 'x'}:
            respuesta = 'usuario'
            respuesta_valida = True
        elif respuesta in {'m', 'M', 'o'}:
            respuesta = 'máquina'
            respuesta_valida = True
        else:
            print('Entrada no válida, por favor, inténtelo de nuevo')
    return respuesta


def empezar_partida():
    # Bienvenida
    print('\n=========================================')
    print('Empezamos el juego')
    print('Las casillas se indican según coordenadas (x,y)')
    print('La posición superior izquierda es (0,0)')
    print('La posición inferior derecha es (2,2)')
    print('=========================================')

    # Inicialización de variables que necesitamos
    turno_de = pregunta_quien_empieza() # usuario, máquina
    tablero = np.zeros(9, dtype=int).reshape(3, 3) # 0 (nada)
                                                   # 1 (cruz)
                                                   # 2 (circulo)
    # tablero = np.array([0, 0, 0, 
    #                     0, 0, 1, 
    #                     1, 0, 0]).reshape(3, 3)
    num_tiradas = 0
    partida_en_juego = True
    print(f'\nTablero inicial:')
    muestra_tablero(tablero)

    # Bucle
    print(f'\nEmpieza la partida, juega {turno_de}.\n')
    while partida_en_juego:
        # Actualización del número de tiradas
        num_tiradas += 1

        # Tirada del usuario
        if turno_de == 'usuario':
            coords = pregunta_coordenadas_tirada(tablero)
            print(f'\nSe va a colocar una cruz en la posición {coords}.')
            tablero[coords] = 1
            partida_en_juego = not determina_si_ganador('usuario', tablero)
            if not partida_en_juego:
                print("La partida ha terminado. Ha ganado el usuario. Gracias por jugar.")

        # Tirada de la máquina
        if turno_de == 'máquina':
            coords = tirada_maquina(tablero)
            print(f'\nLa máquina va a colocar un círculo en la posición {coords}.')
            tablero[coords] = 2
            partida_en_juego = not determina_si_ganador('máquina', tablero)
            if not partida_en_juego:
                print("La partida ha terminado. Ha ganado la máquina. Gracias por jugar.")
        
        # Muestra el estado actual del tablero
        muestra_tablero(tablero)

        # Comprobación de empate
        if num_tiradas == 9 and partida_en_juego:
            print('La partida ha terminado en empate, gracias por jugar.\n')
            partida_en_juego = False

        # Turno del otro
        turno_de = 'máquina' if turno_de == 'usuario' else 'usuario'

    if pregunta_otra_partida():
        empezar_partida()


if __name__ == '__main__':
    empezar_partida()

