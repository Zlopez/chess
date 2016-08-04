# chess
Chess client for linux command line. It processes one move or prepare a new game

## Installation
Just clone repository

`git clone git@github.com:Zlopez/chess.git`

## Start a new game
To start a new game just run

`python3 chess.py`

## Playing a game
To play one turn just run

`python3 chess.py -s <state> -p <player> -m <move>`

- **state** is in format generated in first run of `chess.py`.
- **player** is defined as **W, WHITE** for white or **B, BLACK** for Black.
- **move** is defined in format **from-to**. (Example: A1-A2)

For better readability use argument **-H**.
