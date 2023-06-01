# TIC TAC TOE agent using CLIPS

[CLIPS](https://www.clipsrules.net/) is a tool for building rule-based expert systems. We had to do a tic tac toe agent using CLIPS and I got a 10/10 so why not translate it and publish it here.


## How to run?

Install the dependencies:

```bash
pip install numpy, clipspy
```

Run it:

```
./tic_tac_toe.py
```

Or with the python command:

```
python3 tic_tac_toe.py
```

## How does it work?

The board is made of 9 squares with (x,y) coordinates:

|**(0,0)**|**(0,1)**|**(0,2)**|
|:---:|:---:|:---:|
|**(1,0)**|**(1,1)**|**(1,2)**|
|**(2,0)**|**(2,1)**|**(2,2)**|

9 CLIPS facts represent the board, one for each square. The template is the following:

```lisp
(deftemplate square
            (slot coord_x (type INTEGER))           
            (slot coord_y (type INTEGER))
            (slot type (type INTEGER))
            (slot chosen (type INTEGER)))
```

* ```coord_x``` is the row.
* ```coord_y``` is the column.
* ```type``` represent the current state of the square (I now realize I should have called it state, oh well). 0 is empty, 1 is ```x```, 2 is ```o```.
* ```chosen``` is part of the priority system. Let's talk about that.

The agent, with the rules and their established order, is only in charge of modifying the ```chosen``` attribute, which starts at 0, the other attributes do not change when the agent is running. When the agent is finished running the squares will have different values for said attribute, the square with the highest value is then chosen and an ```o``` will be placed at that position.

The agent then runs (or not) the following rules:

1. The agent looks for a win. If it finds one, then the agent sets the ```chosen``` attribute of the winning square to 1 and the agent stops. The rules associated are:
* ```diagonal_victory```
* ```other_diagonal_victory```
* ```row_victory```
* ```column_victory```

2. If rule 1 fails to run, then the agent looks for a possible defeat. If it finds one, then the agent sets the ```chosen``` attribute of the losing square to 1 and the agent stops. The rules associated are:
* ```diagonal_prevent_defeat```
* ```other_diagonal_prevent_defeat```
* ```row_prevent_defeat```
* ```column_prevent_defeat```

3. If rules 1 and 2 fail to run, then the agent looks for squares where it can threat a win in the next move. It adds 1 to the ```chosen``` attribute of said squares. If he's able to threaten a win, then the agent stops. The rules associated are:
* ```diagonal_threaten_win```
* ```other_diagonal_threaten_win```
* ```row_threaten_win```
* ```column_threaten_win```
* ```multiple_win_threats```

4. If rules 1, 2 and 3 fail to run, then the agent looks for squares where the user can threat a win in the next move. It adds 1 to the ```chosen``` attribute of said squares. If the user is able to threat multiple wins (that is ```chosen > 1``` in at least one of the squares) then the agent stops, this is needed in order to stop the user from putting an ```x``` in a square that guarantees a win in his next next turn. This rules also give double the priority to the center square at the diagonal rules. The rules associated are:
* ```diagonal_stop_threat_defeat```
* ```other_diagonal_stop_threat_defeat```
* ```row_stop_threat_defeat```
* ```column_stop_threat_defeat```

5. If it's the first turn of the game then place the ```o``` at the center square. The rule associated is ```first_turn```.

6. Backup rule, it's supposed to never happen. Just place the ```o``` wherever it can. The rule associated is ```any_free_square```.

## More

I had to translate everything from spanish so I might have missed something.
