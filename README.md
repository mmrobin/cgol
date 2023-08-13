# cgol
...(pronounced, and maybe later written 'seagull') is a terminal-based text-only implementation of Conway's Game of Life with periodic boundary conditions.

Conway's Game of Life is a cellular automaton and zero-player game which takes place on a (usually infinite) square grid.
Every cell (square) is alive xor dead at any given time (generation). The rules are simple:
1) Any living cell with 2 or 3 living neighbors continues to live;
2) Any dead cell with exactly 3 living neighbors springs to life;
3) All other cells die or remain dead.

Conway's Game is a good example of the principle that simple rules often lead to complex conditions.
It is also amusing to look at and often inspiring, which is why I built it right in the terminal (where I spend a lot of time).

Run the file with `$ python3 cgol.py`; due to the way this is implemented it is not (currently) compatible with interactive mode.
This toy currently generates a random board for generation 0.

Features coming soon*:
- Pause/play and manual stepping
- Auto-stop (either upon discovery of a looping condiition or after a specified number of generations)
- Saving and loading board states, probably as strict binary strings (which the grid object can sort out by itself)
- Binary mode -- replace the unicode block characters with 1s and 0s.
- An *actual* installation (to be able to just type `$ cgol`)

``*`` "soon" as in, not never.
