custom_rules = {
 
# Si puede ganar, gana

"""
(defrule posible_victoria_diagonal
    (declare (salience 10))
    (casilla (coord_x ?x) (coord_y ?x) (tipo 2))
    (casilla (coord_x ?y) (coord_y ?y) (tipo 2))
    ?c <- (casilla (coord_x ?z) (coord_y ?z) (tipo 0))
    (test (not (= ?y ?x)))
    (not (casilla_elegida ?))
    =>
    (assert (casilla_elegida sí))
    (modify ?c (elegida 1))
    (printout t "posible_victoria_diagonal" crlf))
""",
"""
(defrule posible_victoria_otra_diagonal
    (declare (salience 10))
    ?c1 <- (casilla (coord_x 0) (coord_y 2) (tipo ?x))
    ?c2 <- (casilla (coord_x 1) (coord_y 1) (tipo ?y))
    ?c3 <- (casilla (coord_x 2) (coord_y 0) (tipo ?z))
    (test (or (and (= ?x 0) (= ?y 2) (= ?z 2))
              (and (= ?x 2) (= ?y 0) (= ?z 2))
              (and (= ?x 2) (= ?y 2) (= ?z 0))))
    (not (casilla_elegida ?))
    =>
    (assert (casilla_elegida sí))
    (if (= ?x 0) then (modify ?c1 (elegida 1)))
    (if (= ?y 0) then (modify ?c2 (elegida 1)))
    (if (= ?z 0) then (modify ?c3 (elegida 1)))
    (printout t "posible_victoria_otra_diagonal" crlf))
""",
"""
(defrule posible_victoria_horizontal
    (declare (salience 10))
    (casilla (coord_x ?x) (coord_y ?y1) (tipo 2))
    (casilla (coord_x ?x) (coord_y ?y2) (tipo 2))
    ?c <- (casilla (coord_x ?x) (coord_y ?y3) (tipo 0))
    (test (not (= ?y1 ?y2)))
    (not (casilla_elegida ?))
    =>
    (assert (casilla_elegida sí))
    (modify ?c (elegida 1))
    (printout t "posible_victoria_horizontal" crlf))
""",
"""
(defrule posible_victoria_vertical
    (declare (salience 10))
    (casilla (coord_x ?x1) (coord_y ?y) (tipo 2))
    (casilla (coord_x ?x2) (coord_y ?y) (tipo 2))
    ?c <- (casilla (coord_x ?x3) (coord_y ?y) (tipo 0))
    (test (not (= ?x1 ?x2)))
    (not (casilla_elegida ?))
    =>
    (assert (casilla_elegida sí))
    (modify ?c (elegida 1))
    (printout t "posible_victoria_vertical" crlf))
""",

# Si va a perder, lo evita

"""
(defrule posible_derrota_diagonal
    (declare (salience 9))
    (casilla (coord_x ?x) (coord_y ?x) (tipo 1))
    (casilla (coord_x ?y) (coord_y ?y) (tipo 1))
    ?c <- (casilla (coord_x ?z) (coord_y ?z) (tipo 0))
    (test (not (= ?y ?x)))
    (not (casilla_elegida ?))
    =>
    (assert (casilla_elegida sí))
    (modify ?c (elegida 1))
    (printout t "posible_derrota_diagonal" crlf))
""",
"""
(defrule posible_derrota_otra_diagonal
    (declare (salience 9))
    ?c1 <- (casilla (coord_x 0) (coord_y 2) (tipo ?x))
    ?c2 <- (casilla (coord_x 1) (coord_y 1) (tipo ?y))
    ?c3 <- (casilla (coord_x 2) (coord_y 0) (tipo ?z))
    (test (or (and (= ?x 0) (= ?y 1) (= ?z 1))
              (and (= ?x 1) (= ?y 0) (= ?z 1))
              (and (= ?x 1) (= ?y 1) (= ?z 0))))
    (not (casilla_elegida ?))
    =>
    (assert (casilla_elegida sí))
    (if (= ?x 0) then (modify ?c1 (elegida 1)))
    (if (= ?y 0) then (modify ?c2 (elegida 1)))
    (if (= ?z 0) then (modify ?c3 (elegida 1)))
    (printout t "posible_derrota_otra_diagonal" crlf))
""",
"""
(defrule posible_derrota_horizontal
    (declare (salience 9))
    (casilla (coord_x ?x) (coord_y ?y1) (tipo 1))
    (casilla (coord_x ?x) (coord_y ?y2) (tipo 1))
    ?c <- (casilla (coord_x ?x) (coord_y ?y3) (tipo 0))
    (test (not (= ?y1 ?y2)))
    (not (casilla_elegida ?))
    =>
    (assert (casilla_elegida sí))
    (modify ?c (elegida 1))
    (printout t "posible_derrota_horizontal" crlf))
""",
"""
(defrule posible_derrota_vertical
    (declare (salience 9))
    (casilla (coord_x ?x1) (coord_y ?y) (tipo 1))
    (casilla (coord_x ?x2) (coord_y ?y) (tipo 1))
    ?c <- (casilla (coord_x ?x3) (coord_y ?y) (tipo 0))
    (test (not (= ?x1 ?x2)))
    (not (casilla_elegida ?))
    =>
    (assert (casilla_elegida sí))
    (modify ?c (elegida 1))
    (printout t "posible_derrota_vertical" crlf))
""",

# Amenazar victoria

"""
(defrule amenazar_victoria_diagonal
    (declare (salience 7))
    ?c1 <- (casilla (coord_x ?x) (coord_y ?x) (tipo 2))
    ?c2 <- (casilla (coord_x ?y) (coord_y ?y) (tipo 0) (elegida ?e2))
    ?c3 <- (casilla (coord_x ?z) (coord_y ?z) (tipo 0) (elegida ?e3))
    (test (not (= ?y ?z)))
    (not (casilla_elegida ?))
    (not (estudiado_amenaza_maquina ?c1 ?c2 ?c3))
    (not (estudiado_amenaza_maquina ?c1 ?c3 ?c2))
    =>
    (assert (estudiado_amenaza_maquina ?c1 ?c2 ?c3))
    (modify ?c2 (elegida (+ 1 ?e2)))
    (modify ?c3 (elegida (+ 1 ?e3)))
    (printout t "amenazar_victoria_diagonal" crlf))
""",
"""
(defrule amenazar_victoria_otra_diagonal
    (declare (salience 7))
    ?c1 <- (casilla (coord_x 0) (coord_y 2) (tipo ?x) (elegida ?e1))
    ?c2 <- (casilla (coord_x 1) (coord_y 1) (tipo ?y) (elegida ?e2))
    ?c3 <- (casilla (coord_x 2) (coord_y 0) (tipo ?z) (elegida ?e3))
    (test (or (and (= ?x 0) (= ?y 0) (= ?z 2))
              (and (= ?x 0) (= ?y 2) (= ?z 0))
              (and (= ?x 2) (= ?y 0) (= ?z 0))))
    (not (casilla_elegida ?))
    (not (estudiado_amenaza_maquina ?c1 ?c2 ?c3))
    (not (estudiado_amenaza_maquina ?c1 ?c3 ?c2))
    (not (estudiado_amenaza_maquina ?c2 ?c3 ?c1))
    (not (estudiado_amenaza_maquina ?c2 ?c1 ?c3))
    (not (estudiado_amenaza_maquina ?c3 ?c2 ?c1))
    (not (estudiado_amenaza_maquina ?c3 ?c1 ?c2))
    =>
    (assert (estudiado_amenaza_maquina ?c1 ?c2 ?c3))
    (if (= ?x 2) then (modify ?c2 (elegida (+ 1 ?e2))) (modify ?c3 (elegida (+ 1 ?e3))))
    (if (= ?y 2) then (modify ?c1 (elegida (+ 1 ?e1))) (modify ?c3 (elegida (+ 1 ?e3))))
    (if (= ?z 2) then (modify ?c1 (elegida (+ 1 ?e1))) (modify ?c2 (elegida (+ 1 ?e2))))
    (printout t "amenazar_victoria_otra_diagonal" crlf))
""",
"""
(defrule amenazar_victoria_horizontal
    (declare (salience 7))
    ?c1 <- (casilla (coord_x ?x) (coord_y ?y1) (tipo 2))
    ?c2 <- (casilla (coord_x ?x) (coord_y ?y2) (tipo 0) (elegida ?e2))
    ?c3 <- (casilla (coord_x ?x) (coord_y ?y3) (tipo 0) (elegida ?e3))
    (test (not (= ?y2 ?y3)))
    (not (casilla_elegida ?))
    (not (estudiado_amenaza_maquina ?c1 ?c2 ?c3))
    (not (estudiado_amenaza_maquina ?c1 ?c3 ?c2))
    =>
    (assert (estudiado_amenaza_maquina ?c1 ?c2 ?c3))
    (modify ?c2 (elegida (+ 1 ?e2)))
    (modify ?c3 (elegida (+ 1 ?e3)))
    (printout t "amenazar_victoria_horizontal" crlf))
""",
"""
(defrule amenazar_victoria_vertical
    (declare (salience 7))
    ?c1 <- (casilla (coord_x ?x1) (coord_y ?y) (tipo 2))
    ?c2 <- (casilla (coord_x ?x2) (coord_y ?y) (tipo 0) (elegida ?e2))
    ?c3 <- (casilla (coord_x ?x3) (coord_y ?y) (tipo 0) (elegida ?e3))
    (test (not (= ?x2 ?x3)))
    (not (casilla_elegida ?))
    (not (estudiado_amenaza_maquina ?c1 ?c2 ?c3))
    (not (estudiado_amenaza_maquina ?c1 ?c3 ?c2))
    =>
    (assert (estudiado_amenaza_maquina ?c1 ?c2 ?c3))
    (modify ?c2 (elegida (+ 1 ?e2)))
    (modify ?c3 (elegida (+ 1 ?e3)))
    (printout t "amenazar_victoria_vertical" crlf))
""",
"""
(defrule hay_amenaza_multiple
    (declare (salience 6))
    (casilla (elegida ?e))
    (test  (> ?e 0))
    (not (casilla_elegida ?))
    (not (amenaza_multiple ?))
    (not (estudiando_amenazas_derrota ?))
    (not (centro_cogida))
    =>
    (assert (amenaza_multiple sí))
    (printout t "hay_amenaza_multiple" crlf))
""",

# Evitar amenaza múltiple

"""
(defrule evitar_amenaza_derrota_diagonal
    (declare (salience 5))
    ?c1 <- (casilla (coord_x ?x) (coord_y ?x) (tipo 1))
    ?c2 <- (casilla (coord_x ?y) (coord_y ?y) (tipo 0) (elegida ?e2))
    ?c3 <- (casilla (coord_x ?z) (coord_y ?z) (tipo 0) (elegida ?e3))
    (test (not (= ?y ?z)))
    (not (casilla_elegida ?))
    (not (amenaza_multiple ?))
    (not (estudiado_amenaza_usuario ?c1 ?c2 ?c3))
    (not (estudiado_amenaza_usuario ?c1 ?c3 ?c2))
    =>
    (assert (estudiado_amenaza_usuario ?c1 ?c2 ?c3))
    (assert (estudiando_amenazas_derrota sí))
    (if (= ?y 1) then (modify ?c2 (elegida (+ 2 ?e2))) else (modify ?c2 (elegida (+ 1 ?e2))))
    (if (= ?z 1) then (modify ?c3 (elegida (+ 2 ?e3))) else (modify ?c3 (elegida (+ 1 ?e2))))
    (printout t "evitar_amenaza_derrota_diagonal" crlf))
""",
"""
(defrule evitar_amenaza_derrota_otra_diagonal
    (declare (salience 5))
    ?c1 <- (casilla (coord_x 0) (coord_y 2) (tipo ?x) (elegida ?e1))
    ?c2 <- (casilla (coord_x 1) (coord_y 1) (tipo ?y) (elegida ?e2))
    ?c3 <- (casilla (coord_x 2) (coord_y 0) (tipo ?z) (elegida ?e3))
    (test (or (and (= ?x 0) (= ?y 0) (= ?z 1))
              (and (= ?x 0) (= ?y 1) (= ?z 0))
              (and (= ?x 1) (= ?y 0) (= ?z 0))))
    (not (casilla_elegida ?))
    (not (amenaza_multiple ?))
    (not (estudiado_amenaza_usuario ?c1 ?c2 ?c3))
    (not (estudiado_amenaza_usuario ?c1 ?c3 ?c2))
    (not (estudiado_amenaza_usuario ?c2 ?c3 ?c1))
    (not (estudiado_amenaza_usuario ?c2 ?c1 ?c3))
    (not (estudiado_amenaza_usuario ?c3 ?c2 ?c1))
    (not (estudiado_amenaza_usuario ?c3 ?c1 ?c2))
    =>
    (assert (estudiado_amenaza_usuario ?c1 ?c2 ?c3))
    (assert (estudiando_amenazas_derrota sí))
    (if (= ?x 1) then (modify ?c2 (elegida (+ 2 ?e2))) (modify ?c3 (elegida (+ 1 ?e3))))
    (if (= ?y 1) then (modify ?c1 (elegida (+ 1 ?e1))) (modify ?c3 (elegida (+ 1 ?e3))))
    (if (= ?z 1) then (modify ?c1 (elegida (+ 1 ?e1))) (modify ?c2 (elegida (+ 2 ?e2))))
    (printout t "evitar_amenaza_derrota_otra_diagonal" crlf))
""",
"""
(defrule evitar_amenaza_derrota_horizontal
    (declare (salience 5))
    ?c1 <- (casilla (coord_x ?x) (coord_y ?y1) (tipo 1))
    ?c2 <- (casilla (coord_x ?x) (coord_y ?y2) (tipo 0) (elegida ?e2))
    ?c3 <- (casilla (coord_x ?x) (coord_y ?y3) (tipo 0) (elegida ?e3))
    (test (not (= ?y2 ?y3)))
    (not (casilla_elegida ?))
    (not (amenaza_multiple ?))
    (not (estudiado_amenaza_usuario ?c1 ?c2 ?c3))
    (not (estudiado_amenaza_usuario ?c1 ?c3 ?c2))
    =>
    (assert (estudiado_amenaza_usuario ?c1 ?c2 ?c3))
    (assert (estudiando_amenazas_derrota sí))
    (modify ?c2 (elegida (+ 1 ?e2)))
    (modify ?c3 (elegida (+ 1 ?e3)))
    (printout t "evitar_amenaza_derrota_horizontal" crlf))
""",
"""
(defrule evitar_amenaza_derrota_vertical
    (declare (salience 5))
    ?c1 <- (casilla (coord_x ?x1) (coord_y ?y) (tipo 1))
    ?c2 <- (casilla (coord_x ?x2) (coord_y ?y) (tipo 0) (elegida ?e2))
    ?c3 <- (casilla (coord_x ?x3) (coord_y ?y) (tipo 0) (elegida ?e3))
    (test (not (= ?x2 ?x3)))
    (not (casilla_elegida ?))
    (not (amenaza_multiple ?))
    (not (estudiado_amenaza_usuario ?c1 ?c2 ?c3))
    (not (estudiado_amenaza_usuario ?c1 ?c3 ?c2))
    =>
    (assert (estudiado_amenaza_usuario ?c1 ?c2 ?c3))
    (assert (estudiando_amenazas_derrota sí))
    (modify ?c2 (elegida (+ 1 ?e2)))
    (modify ?c3 (elegida (+ 1 ?e3)))
    (printout t "evitar_amenaza_derrota_vertical" crlf))
""",
"""
(defrule se_evita_amenaza_multiple
    (declare (salience 4))
    (casilla (elegida ?e))
    (test  (> ?e 1))
    (not (casilla_elegida ?))
    (not (amenaza_multiple ?))
    (not (se_evita_amenaza_multiple ?))
    (not (centro_cogida ?))
    (estudiando_amenazas_derrota sí)
    =>
    (assert (se_evita_amenaza_multiple sí))
    (printout t "se_evita_amenaza_multiple" crlf))
""",

# Cualquier casilla libre

"""
(defrule cualquier_casilla_libre
    (declare (salience 1))
    ?c <- (casilla (tipo 0))
    (not (casilla_elegida ?))
    (not (amenaza_multiple ?))
    (not (centro_cogida ?))
    (not (estudiando_amenazas_derrota ?))
    =>
    (modify ?c (elegida 1))
    (assert (casilla_elegida sí))
    (printout t "cualquier_casilla_libre" crlf))
"""
}
