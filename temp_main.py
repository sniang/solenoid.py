#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/solenoid.py
"""

from Solenoid import *
from Tile import *
import numpy as np

# display the field created by a tile in 2D
tile = Tile()
fig = tile.displayField2D()
fig.savefig("2D.png")


# display the field created by a solenoid in 3D
sol = Solenoid(n = 10)
fig = sol.displayField2D()
fig.savefig("sol_2D.png")

