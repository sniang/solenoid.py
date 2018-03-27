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
sol = Solenoid(B0=1,L=1,n=100,x0=0,y0=0,z0=0,r0=r0,axis="z")
print(sol)

sol.displaySolenoid()
Bx, By, Bz = sol.field(1,1,1)
print(Bx, By, Bz)

# warning : you cannot estimate the field on the tile
x0 = np.sqrt(r0)
y0 = x0
Bx, By, Bz = sol.field(x0, y0, 0.5)
print(Bx, By, Bz)
