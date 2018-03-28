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
        - I: float
            the current intensity
        - self.B0: float
            magnetic field inside the solenoid if it were infinite
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
    def __init__(self,I=400,L=1,n=2000,x0=0,y0=0,z0=0,r0=0.5,axis="z"):
        """
        The constructor
        
        * Arguments
        - I: float
            the current intensity
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
            sol = Solenoid(I=400,L=1,n=100,x0=0,y0=0,z0=0,r0=0.5,axis="z")
            print(sol)
        """
        mu0 = 4E-7*np.pi
        self.B0 = mu0*n*I
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
        self.I = I
        
        b0 = I*mu0/2/r0
        
        for i in np.arange(N) :
         self.tiles.append(Tile(b0,x0=x0,y0=x0,z0=z0-L/2+i*d,r0=r0))
        
        

    def __str__(self):
        return "I = "+str(self.I)+", x0 = "+str(self.x0)+", y0 = "+str(self.y0)+", z0 = "+str(self.z0)+", r0 = "+str(self.r0)+", N = "+str(self.N)+", L = "+str(self.L)

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
            sol = Solenoid(r0=0.5)
            l = np.linspace(-1,1,10)
            x, y, z = np.meshgrid(l,l,l)
            Bx, By, Bz = sol.field(x, y, z)
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
        title = r"$I = "+str(self.I)+"A, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", N = "+str(self.N)+", L = "+str(self.L)

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
    
    def displayField3D(self,figsize=(10,10),nb_points=8,colorTile="red",colorArrow="blue",linewidth=1):
        """
        To display the field in 3D
        * Arguments
            - figsize: (float,float)
                to determine the size of the figure
            - nb_points: int
                number of points of evaluation on each axis
            - colorTile: string
                color of the tiles
            - colorArrow: string
                color of the arrows
            - linewidth: float
                thickness of the tiles
                
        * Returns
            - fig: matplotlib.pyplot.figure
                the figure
        * Example
            sol = Solenoid(n = 50)
            fig = sol.displayField3D()
            fig.savefig("sol_3D.png")
        """
        x, y, z = np.meshgrid(np.linspace(-3*self.r0+self.x0, 3*self.r0+self.x0, nb_points),
                              np.linspace(-3*self.r0+self.y0, 3*self.r0+self.y0, nb_points),
                              np.linspace(self.z0-self.L,self.z0+self.L, nb_points))
        x = np.concatenate(np.concatenate(x))
        y = np.concatenate(np.concatenate(y))
        z = np.concatenate(np.concatenate(z))
        Bx, By, Bz = self.field(x,y,z)
        
        title = r"$I = "+str(self.I)+"A, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", N = "+str(self.N)+", L = "+str(self.L)
        
        fig = plt.figure(figsize=figsize)
        ax = fig.gca(projection='3d')
        ax.set_xlabel(r"x",fontsize=15)
        ax.set_ylabel(r"y",fontsize=15)
        ax.set_zlabel(r"z",fontsize=15)
        ax.set_title(title,fontsize=15)
        ax.quiver(x, y, z, Bx, By, Bz, length=self.r0*0.2, normalize=True, color = colorArrow)
        
        for tile in self.tiles:
            t = np.linspace(0,2*np.pi,100)
            xs = tile.x0 + tile.r0*np.cos(t)
            ys = tile.y0 + tile.r0*np.sin(t)
            zs = tile.z0*np.ones(len(t))
            ax.plot(xs,ys,zs,color=colorTile,linewidth=linewidth)
        
        return fig

    def displayField2D(self,eq_0="y",figsize=(10,10),nb_points=20,color="blue",markTile=True):
        """
        To display the field in a plan x=0, y=0 or z=0

        * Arguments
            - eq_0: string
                to define the variable equal to 0
                accepted argument "x", "y"
            - figsize: (float,float)
                to determine the size of the figure
            - nb_points: int
                number of points of evaluation on each axis
            - color: string
                color of the arrows
            - markTile: boolean
                To diplay the position of the tiles
        * Returns
            - fig: matplotlib.pyplot.figure
                the figure
                
        * Example
            sol = Solenoid(n=100)
            fig = sol.displayField2D(figsize=(8,8))
            fig.savefig("sol_2D.png")
        """
        nb_points = int(nb_points)
        fig = plt.figure(figsize=figsize)
        
        title = r"$I = "+str(self.I)+"A, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", N = "+str(self.N)+", L = "+str(self.L)
        if eq_0 == "x":
            xlabel = r"$y$"
            ylabel = r"$z$"
            title += r", $x = "+str(self.x0)+"$"
            x1, x2 = np.meshgrid(np.linspace(-3*self.r0+self.y0, 3*self.r0+self.y0, nb_points),np.linspace(self.z0-self.L,self.z0+self.L, nb_points))
            x3 = np.zeros_like(x1)+self.x0
            Bx3, Bx1, Bx2 = self.field(x3, x1, x2)
            
        elif eq_0 == "y":
            xlabel = r"$x$"
            ylabel = r"$z$"
            title += r", $y = "+str(self.y0)+"$"
            x1, x2 = np.meshgrid(np.linspace(-3*self.r0+self.x0, 3*self.r0+self.x0, nb_points),np.linspace(self.z0-self.L,self.z0+self.L, nb_points))
            x3 = np.zeros_like(x1)+self.y0
            Bx1, Bx3, Bx2 = self.field(x1, x3, x2)
        else:
            print("Your choice of plan is incorrect")
            return fig
        
        if markTile:
            for tile in self.tiles:
                if eq_0 == "x":
                    dotx1 = np.array([-tile.r0,tile.r0])+tile.y0
                    dotx2 = [tile.z0,tile.z0]
                elif eq_0 == "y":
                    
                    dotx1 = np.array([-tile.r0,tile.r0])+tile.x0
                    dotx2 = [tile.z0,tile.z0]
                plt.plot(dotx1,dotx2,'.',ms=5,color="red")
            
        no = np.sqrt(Bx1**2+Bx2**2+Bx3**2)
        Bx1 = Bx1/no
        Bx2 = Bx2/no

        plt.quiver(x1,x2,Bx1,Bx2,color=color)
            
                
        plt.title(r"$I = $"+str(self.I)+"$A$, "+title,fontsize=15)
        plt.xlabel(xlabel,fontsize=15)
        plt.ylabel(ylabel,fontsize=15)
        plt.tight_layout()

        return fig
    
    def exportFieldMap(self,filename,xmin,xmax,ymin,ymax,zmin,zmax,nb_points):
        """
        To export a field map as a .txt file
        
        * Arguments
            - filename: String
                the name of the output file
            - xmin: float
                the x min coordinate
            - xmax: float
                the x max coordinate
            - ymin: float
                the y min coordinate
            - ymax: float
                the y max coordinate
            - zmin: float
                the z min coordinate
            - zmax: float
                the z max coordinate
            - nb_points: int
                number of points of evaluation on each axis
        * Example
            sol = Solenoid()
            sol.exportFieldMap("output.txt",-1,1,-1,1,-1,1,20)
        """
        
        return 0
