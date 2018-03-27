#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/solenoid.py
"""
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from Tile import *
import matplotlib.pyplot as plt

class Solenoid:
    """
    To simulate a solenoid
    
    * Attributes
        - self.B0: float
            magnetic field at the center of the tile
        - self.L: float
            the length of the solenoid in meter
        - self.n: float
            number of tiles per meter
        - self.x0: float
            the x position of the tile
        - self.y0: float
            the y position of the tile
        - self.z0: float
            the z position of the tile
        - self.r0: float
            the radius of the tile
        - self.axis: string
            the axis of the solenoid
        - self.N: int(n*L)
            number of tiles
        - self.tiles: array(Tile)
            the tiles
        
    """
    def __init__(self,B0=1,L=1,n=100,x0=0,y0=0,z0=0,r0=0.5,axis="z"):
        """
        The constructor
        
        * Arguments
        - B0: float
            magnetic field at the center of the tile
        - L: float
            the length of the solenoid in meter
        - n: float
            number of tiles per meter
        - x0: float
            the x position of the tile
        - y0: float
            the y position of the tile
        - z0: float
            the z position of the tile
        - r0: float
            the radius of the tile
        - axis: string (for now, the only acceptable value is "z")
            the axis of the solenoid
        
        * Example
            sol = Solenoid(B0=1,L=1,n=100,x0=0,y0=0,z0=0,r0=0.5,axis="z")
            print(sol)
        """
        self.B0 = B0
        self.L = L
        self.n = n
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r0 = r0
        self.N = int(n*L)
        N = self.N
        d = L/(N-1)
        self.tiles = []
        
        for i in np.arange(N) :
         self.tiles.append(Tile(B0/N,x0=x0,y0=x0,z0=z0-L/2+i*d,r0=r0))
        
        

    def __str__(self):
        return "B0 = "+str(self.B0)+", x0 = "+str(self.x0)+", y0 = "+str(self.y0)+", z0 = "+str(self.z0)+", r0 = "+str(self.r0)+", N = "+str(self.N)+", L = "+str(self.L)

    def field(self,x,y,z):
        """
        To compute the magnetic field produced by the solenoid
        
        * Arguments
            - x: float
                the x coordinate
            - y: float
                the y coordinate
            - z: float
                the y coordinate
        
        * Returns
            - Bx, By, Bz: (float,float,float)
                The magnetic field
        
        * Example
            sol = solenoid(r0=0.5)
            l = np.linspace(-1,1,10)
            x, y, z = np.meshgrid(l,l,l)
            Bx, By, Bz = sol.field(l,l,l)
        """
        Bx = 0
        By = 0
        Bz = 0
        
        for tile in self.tiles:
            bx, by, bz = tile.field(x,y,z)
            Bx += bx
            By += by
            Bz += bz
        return Bx, By, Bz
    
    def displaySolenoid(self,figsize=(10,10),color="red",linewidth=1):
        """
        To display the solenoid
        
        * Arguments
            - figsize: (float,float)
                to determine the size of the figure
            - color: string
                color of the tile
            - linewidth: float
                thickness of the tile
        * Returns
            - fig: matplotlib.pyplot.figure
                the figure
                
        * Example
            sol = Solenoid()
            fig = sol.displaySolenoid()
            fig.savefig("sol.png")
        """
        title = r"$B_0 = "+str(self.B0)+"T, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", N = "+str(self.N)+", L = "+str(self.L)

        fig = plt.figure(figsize=figsize)
        ax = fig.gca(projection='3d')
        ax.set_xlabel(r"x",fontsize=15)
        ax.set_ylabel(r"y",fontsize=15)
        ax.set_zlabel(r"z",fontsize=15)
        ax.set_title(title,fontsize=15)
        
        t = np.linspace(0,2*np.pi,100)
        
        for tile in self.tiles:
            xs = tile.x0 + tile.r0*np.cos(t)
            ys = tile.y0 + tile.r0*np.sin(t)
            zs = tile.z0*np.ones(len(t))
            ax.plot(xs,ys,zs,color=color,linewidth=linewidth)
        
        return fig
    
    def displayField3D(self,figsize=(10,10)):
        """
        To display the field in 3D
        * Arguments
            -
        * Returns
            -
        """
        title = r"$B_0 = "+str(self.B0)+"T, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", N = "+str(self.N)+", L = "+str(self.L)

        fig = plt.figure(figsize=figsize)
        ax = fig.gca(projection='3d')
        ax.set_xlabel(r"x",fontsize=15)
        ax.set_ylabel(r"y",fontsize=15)
        ax.set_zlabel(r"z",fontsize=15)
        ax.set_title(title,fontsize=15)
        return fig

    def displayField2D(self,figsize=(10,10)):
        """
        * Arguments
            -
        * Returns
            -
        """
        title = r"$B_0 = "+str(self.B0)+"T, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", N = "+str(self.N)+", L = "+str(self.L)

        fig = plt.figure(figsize=figsize)
        plt.title(title)
        return fig
