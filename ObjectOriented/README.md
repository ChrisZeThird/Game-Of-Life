## About this folder

You will find here several files containing different classes. Two main categories exist: the 0-player or Classic mod of Conway's game, and the 1v1 mod or Versus mod. The next step is to developp an artificial intelligence that would play against the player. Or other mod where each round the players can add one or more cell to the board in order to win.

An additionnal file called `TestGoL.py` is available if you want to test the classes immediately. You can change the parameters set of course.

## About the 1v1 mod

The 1v1 mode behaves like the 0-player version: each player places an initial configuration of their cells and the winner is the one with still-standing cells. You can still change the parameters `p1` and `p2`
corresponding to the player colour. Just note that the `cmap` used is called `CMRmap` to have black for `0` and white for `1`. But you can still decide to change it. Just make sure to adapt the cell
conditions accordingly.
