custom_rules = {
 
# If the agent can win, it'll win

"""
(defrule diagonal_victory
    (declare (salience 10))
    (square (coord_x ?x) (coord_y ?x) (type 2))
    (square (coord_x ?y) (coord_y ?y) (type 2))
    ?c <- (square (coord_x ?z) (coord_y ?z) (type 0))
    (test (not (= ?y ?x)))
    (not (square_chosen ?))
    =>
    (assert (square_chosen yes))
    (modify ?c (chosen 1))
    (assert (diagonal_victory activated)))
""",
"""
(defrule other_diagonal_victory
    (declare (salience 10))
    ?c1 <- (square (coord_x 0) (coord_y 2) (type ?x))
    ?c2 <- (square (coord_x 1) (coord_y 1) (type ?y))
    ?c3 <- (square (coord_x 2) (coord_y 0) (type ?z))
    (test (or (and (= ?x 0) (= ?y 2) (= ?z 2))
              (and (= ?x 2) (= ?y 0) (= ?z 2))
              (and (= ?x 2) (= ?y 2) (= ?z 0))))
    (not (square_chosen ?))
    =>
    (assert (square_chosen yes))
    (if (= ?x 0) then (modify ?c1 (chosen 1)))
    (if (= ?y 0) then (modify ?c2 (chosen 1)))
    (if (= ?z 0) then (modify ?c3 (chosen 1)))
    (assert (other_diagonal_victory activated)))
""",
"""
(defrule row_victory
    (declare (salience 10))
    (square (coord_x ?x) (coord_y ?y1) (type 2))
    (square (coord_x ?x) (coord_y ?y2) (type 2))
    ?c <- (square (coord_x ?x) (coord_y ?y3) (type 0))
    (test (not (= ?y1 ?y2)))
    (not (square_chosen ?))
    =>
    (assert (square_chosen yes))
    (modify ?c (chosen 1))
    (assert (row_victory activated)))
""",
"""
(defrule column_victory
    (declare (salience 10))
    (square (coord_x ?x1) (coord_y ?y) (type 2))
    (square (coord_x ?x2) (coord_y ?y) (type 2))
    ?c <- (square (coord_x ?x3) (coord_y ?y) (type 0))
    (test (not (= ?x1 ?x2)))
    (not (square_chosen ?))
    =>
    (assert (square_chosen yes))
    (modify ?c (chosen 1))
    (assert (column_victory activated)))
""",

# If the agent will lose, it'll prevent it

"""
(defrule diagonal_prevent_defeat
    (declare (salience 9))
    (square (coord_x ?x) (coord_y ?x) (type 1))
    (square (coord_x ?y) (coord_y ?y) (type 1))
    ?c <- (square (coord_x ?z) (coord_y ?z) (type 0))
    (test (not (= ?y ?x)))
    (not (square_chosen ?))
    =>
    (assert (square_chosen yes))
    (modify ?c (chosen 1))
    (assert (diagonal_prevent_defeat activated)))
""",
"""
(defrule other_diagonal_prevent_defeat
    (declare (salience 9))
    ?c1 <- (square (coord_x 0) (coord_y 2) (type ?x))
    ?c2 <- (square (coord_x 1) (coord_y 1) (type ?y))
    ?c3 <- (square (coord_x 2) (coord_y 0) (type ?z))
    (test (or (and (= ?x 0) (= ?y 1) (= ?z 1))
              (and (= ?x 1) (= ?y 0) (= ?z 1))
              (and (= ?x 1) (= ?y 1) (= ?z 0))))
    (not (square_chosen ?))
    =>
    (assert (square_chosen yes))
    (if (= ?x 0) then (modify ?c1 (chosen 1)))
    (if (= ?y 0) then (modify ?c2 (chosen 1)))
    (if (= ?z 0) then (modify ?c3 (chosen 1)))
    (assert (other_diagonal_prevent_defeat activated)))
""",
"""
(defrule row_prevent_defeat
    (declare (salience 9))
    (square (coord_x ?x) (coord_y ?y1) (type 1))
    (square (coord_x ?x) (coord_y ?y2) (type 1))
    ?c <- (square (coord_x ?x) (coord_y ?y3) (type 0))
    (test (not (= ?y1 ?y2)))
    (not (square_chosen ?))
    =>
    (assert (square_chosen yes))
    (modify ?c (chosen 1))
    (assert (row_prevent_defeat activated)))
""",
"""
(defrule column_prevent_defeat
    (declare (salience 9))
    (square (coord_x ?x1) (coord_y ?y) (type 1))
    (square (coord_x ?x2) (coord_y ?y) (type 1))
    ?c <- (square (coord_x ?x3) (coord_y ?y) (type 0))
    (test (not (= ?x1 ?x2)))
    (not (square_chosen ?))
    =>
    (assert (square_chosen yes))
    (modify ?c (chosen 1))
    (assert (column_prevent_defeat activated)))
""",

# The agent threatens the maximum number of wins possible

"""
(defrule diagonal_threaten_win
    (declare (salience 7))
    ?c1 <- (square (coord_x ?x) (coord_y ?x) (type 2))
    ?c2 <- (square (coord_x ?y) (coord_y ?y) (type 0) (chosen ?e2))
    ?c3 <- (square (coord_x ?z) (coord_y ?z) (type 0) (chosen ?e3))
    (test (not (= ?y ?z)))
    (not (square_chosen ?))
    (not (agent_threat_studied ?c1 ?c2 ?c3))
    (not (agent_threat_studied ?c1 ?c3 ?c2))
    =>
    (assert (agent_threat_studied ?c1 ?c2 ?c3))
    (modify ?c2 (chosen (+ 1 ?e2)))
    (modify ?c3 (chosen (+ 1 ?e3)))
    (assert (diagonal_threaten_win activated)))
""",
"""
(defrule other_diagonal_threaten_win
    (declare (salience 7))
    ?c1 <- (square (coord_x 0) (coord_y 2) (type ?x) (chosen ?e1))
    ?c2 <- (square (coord_x 1) (coord_y 1) (type ?y) (chosen ?e2))
    ?c3 <- (square (coord_x 2) (coord_y 0) (type ?z) (chosen ?e3))
    (test (or (and (= ?x 0) (= ?y 0) (= ?z 2))
              (and (= ?x 0) (= ?y 2) (= ?z 0))
              (and (= ?x 2) (= ?y 0) (= ?z 0))))
    (not (square_chosen ?))
    (not (agent_threat_studied ?c1 ?c2 ?c3))
    (not (agent_threat_studied ?c1 ?c3 ?c2))
    (not (agent_threat_studied ?c2 ?c3 ?c1))
    (not (agent_threat_studied ?c2 ?c1 ?c3))
    (not (agent_threat_studied ?c3 ?c2 ?c1))
    (not (agent_threat_studied ?c3 ?c1 ?c2))
    =>
    (assert (agent_threat_studied ?c1 ?c2 ?c3))
    (if (= ?x 2) then (modify ?c2 (chosen (+ 1 ?e2))) (modify ?c3 (chosen (+ 1 ?e3))))
    (if (= ?y 2) then (modify ?c1 (chosen (+ 1 ?e1))) (modify ?c3 (chosen (+ 1 ?e3))))
    (if (= ?z 2) then (modify ?c1 (chosen (+ 1 ?e1))) (modify ?c2 (chosen (+ 1 ?e2))))
    (assert (other_diagonal_threaten_win activated)))
""",
"""
(defrule row_threaten_win
    (declare (salience 7))
    ?c1 <- (square (coord_x ?x) (coord_y ?y1) (type 2))
    ?c2 <- (square (coord_x ?x) (coord_y ?y2) (type 0) (chosen ?e2))
    ?c3 <- (square (coord_x ?x) (coord_y ?y3) (type 0) (chosen ?e3))
    (test (not (= ?y2 ?y3)))
    (not (square_chosen ?))
    (not (agent_threat_studied ?c1 ?c2 ?c3))
    (not (agent_threat_studied ?c1 ?c3 ?c2))
    =>
    (assert (agent_threat_studied ?c1 ?c2 ?c3))
    (modify ?c2 (chosen (+ 1 ?e2)))
    (modify ?c3 (chosen (+ 1 ?e3)))
    (assert (row_threaten_win activated)))
""",
"""
(defrule column_threaten_win
    (declare (salience 7))
    ?c1 <- (square (coord_x ?x1) (coord_y ?y) (type 2))
    ?c2 <- (square (coord_x ?x2) (coord_y ?y) (type 0) (chosen ?e2))
    ?c3 <- (square (coord_x ?x3) (coord_y ?y) (type 0) (chosen ?e3))
    (test (not (= ?x2 ?x3)))
    (not (square_chosen ?))
    (not (agent_threat_studied ?c1 ?c2 ?c3))
    (not (agent_threat_studied ?c1 ?c3 ?c2))
    =>
    (assert (agent_threat_studied ?c1 ?c2 ?c3))
    (modify ?c2 (chosen (+ 1 ?e2)))
    (modify ?c3 (chosen (+ 1 ?e3)))
    (assert (column_threaten_win activated)))
""",
"""
(defrule multiple_win_threats
    (declare (salience 6))
    (square (chosen ?e))
    (test  (> ?e 0))
    (not (square_chosen ?))
    (not (agent_multiple_threats_exist ?))
    (not (user_threat_exists ?))
    =>
    (assert (agent_multiple_threats_exist yes)))
""",

# The agent defends the maximum number of loses possible

"""
(defrule diagonal_stop_threat_defeat
    (declare (salience 5))
    ?c1 <- (square (coord_x ?x) (coord_y ?x) (type 1))
    ?c2 <- (square (coord_x ?y) (coord_y ?y) (type 0) (chosen ?e2))
    ?c3 <- (square (coord_x ?z) (coord_y ?z) (type 0) (chosen ?e3))
    (test (not (= ?y ?z)))
    (not (square_chosen ?))
    (not (agent_multiple_threats_exist ?))
    (not (user_threat_studied ?c1 ?c2 ?c3))
    (not (user_threat_studied ?c1 ?c3 ?c2))
    =>
    (assert (user_threat_studied ?c1 ?c2 ?c3))
    (assert (user_threat_exists yes))
    (if (= ?y 1) then (modify ?c2 (chosen (+ 2 ?e2))) else (modify ?c2 (chosen (+ 1 ?e2))))
    (if (= ?z 1) then (modify ?c3 (chosen (+ 2 ?e3))) else (modify ?c3 (chosen (+ 1 ?e2))))
    (assert (diagonal_stop_threat_defeat activated)))
""",
"""
(defrule other_diagonal_stop_threat_defeat
    (declare (salience 5))
    ?c1 <- (square (coord_x 0) (coord_y 2) (type ?x) (chosen ?e1))
    ?c2 <- (square (coord_x 1) (coord_y 1) (type ?y) (chosen ?e2))
    ?c3 <- (square (coord_x 2) (coord_y 0) (type ?z) (chosen ?e3))
    (test (or (and (= ?x 0) (= ?y 0) (= ?z 1))
              (and (= ?x 0) (= ?y 1) (= ?z 0))
              (and (= ?x 1) (= ?y 0) (= ?z 0))))
    (not (square_chosen ?))
    (not (agent_multiple_threats_exist ?))
    (not (user_threat_studied ?c1 ?c2 ?c3))
    (not (user_threat_studied ?c1 ?c3 ?c2))
    (not (user_threat_studied ?c2 ?c3 ?c1))
    (not (user_threat_studied ?c2 ?c1 ?c3))
    (not (user_threat_studied ?c3 ?c2 ?c1))
    (not (user_threat_studied ?c3 ?c1 ?c2))
    =>
    (assert (user_threat_studied ?c1 ?c2 ?c3))
    (assert (user_threat_exists yes))
    (if (= ?x 1) then (modify ?c2 (chosen (+ 2 ?e2))) (modify ?c3 (chosen (+ 1 ?e3))))
    (if (= ?y 1) then (modify ?c1 (chosen (+ 1 ?e1))) (modify ?c3 (chosen (+ 1 ?e3))))
    (if (= ?z 1) then (modify ?c1 (chosen (+ 1 ?e1))) (modify ?c2 (chosen (+ 2 ?e2))))
    (assert (other_diagonal_stop_threat_defeat activated)))
""",
"""
(defrule row_stop_threat_defeat
    (declare (salience 5))
    ?c1 <- (square (coord_x ?x) (coord_y ?y1) (type 1))
    ?c2 <- (square (coord_x ?x) (coord_y ?y2) (type 0) (chosen ?e2))
    ?c3 <- (square (coord_x ?x) (coord_y ?y3) (type 0) (chosen ?e3))
    (test (not (= ?y2 ?y3)))
    (not (square_chosen ?))
    (not (agent_multiple_threats_exist ?))
    (not (user_threat_studied ?c1 ?c2 ?c3))
    (not (user_threat_studied ?c1 ?c3 ?c2))
    =>
    (assert (user_threat_studied ?c1 ?c2 ?c3))
    (assert (user_threat_exists yes))
    (modify ?c2 (chosen (+ 1 ?e2)))
    (modify ?c3 (chosen (+ 1 ?e3)))
    (assert (row_stop_threat_defeat activated)))
""",
"""
(defrule column_stop_threat_defeat
    (declare (salience 5))
    ?c1 <- (square (coord_x ?x1) (coord_y ?y) (type 1))
    ?c2 <- (square (coord_x ?x2) (coord_y ?y) (type 0) (chosen ?e2))
    ?c3 <- (square (coord_x ?x3) (coord_y ?y) (type 0) (chosen ?e3))
    (test (not (= ?x2 ?x3)))
    (not (square_chosen ?))
    (not (agent_multiple_threats_exist ?))
    (not (user_threat_studied ?c1 ?c2 ?c3))
    (not (user_threat_studied ?c1 ?c3 ?c2))
    =>
    (assert (user_threat_studied ?c1 ?c2 ?c3))
    (assert (user_threat_exists yes))
    (modify ?c2 (chosen (+ 1 ?e2)))
    (modify ?c3 (chosen (+ 1 ?e3)))
    (assert (column_stop_threat_defeat activated)))
""",

# First round

"""
(defrule first_turn
    (declare (salience 3))
    (not (square (type 1)))
    (not (square (type 2)))
    ?c <- (square (coord_x 1) (coord_y 1))
    (not (square_chosen ?))
    (not (agent_multiple_threats_exist ?))
    (not (user_threat_exists ?))
    =>
    (modify ?c (chosen 1))
    (assert (square_chosen yes))
    (assert (first_turn activated)))
""",

# Backup rule

"""
(defrule any_free_square
    (declare (salience 1))
    ?c <- (square (type 0))
    (not (square_chosen ?))
    (not (agent_multiple_threats_exist ?))
    (not (user_threat_exists ?))
    =>
    (modify ?c (chosen 1))
    (assert (square_chosen yes))
    (assert (any_free_square activated)))
"""
}
