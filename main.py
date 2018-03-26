#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/solenoid.py
"""

from Solenoid import *
from Tile import *
import numpy as np


tile = Tile(1,1,2,3,5)
fig = tile.displayTile()
fig.savefig("tile.png")

tile = Tile(1,1,2,3,5)
fig = tile.displayField2D()
fig.savefig("2D.png")

tile = Tile(1,1,2,3,5)
fig = tile.displayField3D()
fig.savefig("3D.png")

