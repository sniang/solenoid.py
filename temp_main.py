#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/solenoid.py
"""

from Solenoid import *
from Tile import *
import numpy as np

# To export a field map as a .txt file
sol = Solenoid()
sol.exportFieldMap("output.txt",-1,1,-1,1,-1,1,20)