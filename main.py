#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/solenoid.py
"""

from Solenoid import *
from Tile import *
import numpy as np

# create a tile and compute the field
r0 = 2
tile = Tile(1,0,0,0,r0)
Bx, By, Bz = tile.field(1,1,1)
print(Bx, By, Bz)
# warning : you cannot estimate the field on the tile
x0 = np.sqrt(r0)
y0 = x0
Bx, By, Bz = tile.field(x0, y0, 0)
print(Bx, By, Bz)

# display the tile
tile = Tile(1,1,2,3,5)
fig = tile.displayTile()
fig.savefig("tile.png")

# display the field created by a tile in 2D
tile = Tile(1,1,2,3,5)
fig = tile.displayField2D()
fig.savefig("2D.png")

# display the field created by a tile in 3D
tile = Tile(1,1,2,3,5)
fig = tile.displayField3D()
fig.savefig("3D.png")

# display the solenoid
sol = Solenoid()
fig = sol.displaySolenoid()
fig.savefig("sol.png")

# display the field created by a solenoid in 2D
sol = Solenoid()
fig = sol.displayField3D()
fig.savefig("sol_3D.png")

# display the field created by a solenoid in 3D
sol = Solenoid()
fig = sol.displayField2D()
fig.savefig("sol_2D.png")




