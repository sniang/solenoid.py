#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/Solenoyds
https://sniang.github.io/Solenoyds
"""

from Solenoyds.Solenoid import Solenoid
from Solenoyds.Loop import Loop
import numpy as np


# create a loop and compute the field
r0 = 2
loop = Loop(1,0,0,0,r0)
Bx, By, Bz = loop.field(1,1,1)
print(Bx, By, Bz)

# warning : you cannot estimate the field on the loop
x0 = np.sqrt(r0)
y0 = x0
Bx, By, Bz = loop.field(x0, y0, 0)
print(Bx, By, Bz)

# To plot the field on the main axis
loop = Loop(B0=0.1)
fig = loop.plotFieldMainAxis(zmin=-5,zmax=5)
fig.savefig("axis_loop.png")

# display the loop
loop = Loop(1,1,2,3,5)
fig = loop.displayLoop()
fig.savefig("loop.png")

# display the field created by a loop in 2D
loop = Loop(1,1,2,3,5)
fig = loop.displayField2D(figsize=(8,8))
fig.savefig("2D.png")

# display the field created by a loop in 3D
loop = Loop(1,1,2,3,5)
fig = loop.displayField3D()
fig.savefig("3D.png")


# create a solenoid and compute the field
sol = Solenoid(r0=0.5)
l = np.linspace(-1,1,10)
x, y, z = np.meshgrid(l,l,l)
Bx, By, Bz = sol.field(x, y, z)

# To plot the field on the main axis
sol = Solenoid(n = 1000, I = 100,L = 5, z0 = 33)
fig = sol.plotFieldMainAxis(zmin=-sol.L,zmax=sol.L)
fig.savefig("axis_sol.png")

#To do a colormap of the field
sol = Solenoid(n=50,x0=2,L=5)
fig1, fig2, fig3 = sol.colormapField()
fig1.savefig("colomap1.png")
fig2.savefig("colomap2.png")
fig3.savefig("colomap3.png")

# To export a field map as a .txt file
sol = Solenoid(n=50)
sol.exportFieldMap("output_main.txt",-1,1,-1,1,-1,1,20)

# To export the field computed in some points as a .txt file
z = np.linspace(-2,2,20)
x = np.zeros_like(z)
y = np.zeros_like(z)
sol = Solenoid(n=40)
sol.exportField("output.txt",x,y,z)

# display the solenoid
sol = Solenoid(n=100)
fig = sol.displaySolenoid()
fig.savefig("sol.png")

# display the field created by a solenoid in 2D
sol = Solenoid(n=100)
fig = sol.displayField2D(figsize=(8,8))
fig.savefig("sol_2D.png")

# display the field created by a solenoid in 3D
sol = Solenoid(n = 50)
fig = sol.displayField3D()
fig.savefig("sol_3D.png")

