#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/solenoid.py
"""
import numpy as np
from scipy import special
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import warnings

class Tile:
    """
    To simulate the tile
    
    * Attributes
        - self.B0: float
            magnetic field at the center of the tile
        - self.x0: float
            the x position of the tile
        - self.y0: float
            the y position of the tile
        - self.z0: float
            the z position of the tile
        - self.r0: float
            the radius of the tile
    """
    def __init__(self,B0=1,x0=0,y0=0,z0=0,r0=1):
        """
        The constructor
        * Arguments
            - B0: float
                magnetic field at the center of the tile
            - x0: float
                the x position of the tile
            - y0: float
                the y position of the tile
            - z0: float
                the z position of the tile
            - r0: float
                the radius of the tile
                
        * Example
            tile = Tile(1,1,2,3,5) 
        """
        self.B0 = B0
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r0 = r0

    def __str__(self):
        return "B0 = "+str(self.B0)+", x0 = "+str(self.x0)+", y0 = "+str(self.y0)+", z0 = "+str(self.z0)+", r0 = "+str(self.r0)

    def field(self,x,y,z):
        """
        To compute the magnetic field produced by the tile
        
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
            tile = Tile(1,1,2,3,5)
            l = np.linspace(-1,1,10)
            x, y, z = np.meshgrid(l,l,l)
            Bx, By, Bz = tile.field(x, y, z)
        """
        x = x-self.x0
        y = y-self.y0
        z = z-self.z0
        
        def f(x1,y1,z1):
            K = special.ellipk
            E = special.ellipe
            r = np.sqrt(x1**2+y1**2)
            a = r/self.r0
            b = z1/self.r0
            c = z1/r
            Q = (1+a)**2 + b**2
            m = 4*a/Q
            
            if r == self.r0 and z1 == 0:
                warnings.warn("Warning : you cannot estimate the field on the tile")
                return np.nan, np.nan, np.nan
            if r == 0:
                ca = self.r0/np.sqrt(self.r0**2+z1**2)
                Bz = self.B0*(ca**3)                
                return 0, 0, Bz
            
            if np.abs(m-1) < 0.01:
                def K(x):
                    return special.ellipkm1(1-x)
            
            c1 = x1/r
            s1 = y1/r
    
            Bz = self.B0/(np.pi*np.sqrt(Q))*(E(m)*(1-a**2-b**2)/(Q-4*a)+K(m))
            Br = self.B0*c/(np.pi*np.sqrt(Q))*(E(m)*(1+a**2+b**2)/(Q-4*a)-K(m))
            Bx = Br*c1
            By = Br*s1
            return Bx, By, Bz
        vect = np.vectorize(f)
        return vect(x,y,z)


    def displayTile(self,figsize=(10,10),color="red",linewidth=3):
        """
        To display the tile
        
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
            tile = Tile(1,1,2,3,5)
            fig = tile.displayTile()
            fig.savefig("tile.png")
        """
        t = np.linspace(0,2*np.pi,100)
        xs = self.x0 + self.r0*np.cos(t)
        ys = self.y0 + self.r0*np.sin(t)
        zs = self.z0*np.ones(len(t))
        
        title = r"$B_0 = "+str(self.B0)+"T, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)
        
        fig = plt.figure(figsize=figsize)
        ax = fig.gca(projection='3d')
        ax.plot(xs,ys,zs,color=color,linewidth=linewidth)
        ax.set_xlabel(r"x",fontsize=15)
        ax.set_ylabel(r"y",fontsize=15)
        ax.set_zlabel(r"z",fontsize=15)
        ax.set_title(title,fontsize=15)
        
        return fig
    
    def displayField3D(self,figsize=(10,10),nb_points=8,colorTile="red",colorArrow="blue",linewidth=3):
        """
        To display the field
        * Arguments
            - figsize: (float,float)
                to determine the size of the figure
            - nb_points: int
                number of points of evaluation on each axis
            - colorTile: string
                color of the tile
            - colorArrow: string
                color of the arrows
            - linewidth: float
                thickness of the tile
                
        * Returns
            - fig: matplotlib.pyplot.figure
                the figure
        * Example
            tile = Tile(1,1,2,3,5)
            fig = tile.displayField3D()
            fig.savefig("3D.png")
        """
        x, y, z = np.meshgrid(np.linspace(-2*self.r0+self.x0, 2*self.r0+self.x0, nb_points),
                               np.linspace(-2*self.r0+self.y0, 2*self.r0+self.y0, nb_points),
                               np.linspace(-2*self.r0+self.z0, 2*self.r0+self.z0, nb_points))
        x = np.concatenate(np.concatenate(x))
        y = np.concatenate(np.concatenate(y))
        z = np.concatenate(np.concatenate(z))
        Bx, By, Bz = self.field(x,y,z)
        
        t = np.linspace(0,2*np.pi,100)
        xs = self.x0 + self.r0*np.cos(t)
        ys = self.y0 + self.r0*np.sin(t)
        zs = self.z0*np.ones(len(t))
        
        title = r"$B_0 = "+str(self.B0)+"T, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)
        
        fig = plt.figure(figsize=figsize)
        ax = fig.gca(projection='3d')
        ax.set_xlabel(r"x",fontsize=15)
        ax.set_ylabel(r"y",fontsize=15)
        ax.set_zlabel(r"z",fontsize=15)
        ax.set_title(title,fontsize=15)
        ax.quiver(x, y, z, Bx, By, Bz, length=self.r0*0.2, normalize=True, color = colorArrow)
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
                To diplay the position of the tile
        * Returns
            - fig: matplotlib.pyplot.figure
                the figure
                
        * Example
            tile = Tile(1,1,2,3,5)
            fig = tile.displayField2D()
            fig.savefig("2D.png")
        """
        nb_points = int(nb_points)
        fig = plt.figure(figsize=figsize)


        if eq_0 == "x":
            x1, x2 = np.meshgrid(np.linspace(-2*self.r0+self.y0, 2*self.r0+self.y0, nb_points),np.linspace(-2*self.r0+self.z0, 2*self.r0+self.z0, nb_points))
            x3 = np.zeros_like(x1)+self.x0
            Bx3, Bx1, Bx2 = self.field(x3, x1, x2)
            dotx1 = np.array([-self.r0,self.r0])+self.y0
            dotx2 = [self.z0,self.z0]
            xlabel = r"$y$"
            ylabel = r"$z$"
            title = r"x = "+str(self.x0)

        elif eq_0 == "y":
            x1, x2 = np.meshgrid(np.linspace(-2*self.r0+self.x0, 2*self.r0+self.x0, nb_points),np.linspace(-2*self.r0+self.z0, 2*self.r0+self.z0, nb_points))
            x3 = np.zeros_like(x1)+self.y0
            Bx1, Bx3, Bx2 = self.field(x1, x3, x2)
            dotx1 = np.array([-self.r0,self.r0])+self.x0
            dotx2 = [self.z0,self.z0]
            xlabel = r"$x$"
            ylabel = r"$z$"
            title = r"y = "+str(self.y0)

        else:
            print("Your choice of plan is incorrect")
            return fig        

        no = np.sqrt(Bx1**2+Bx2**2+Bx3**2)
        Bx1 = Bx1/no
        Bx2 = Bx2/no
        
        plt.title(r"$B_0 = $"+str(self.B0)+"$T$, "+title,fontsize=15)
        plt.xlabel(xlabel,fontsize=15)
        plt.ylabel(ylabel,fontsize=15)
        plt.quiver(x1,x2,Bx1,Bx2,color=color)
        
        if markTile:
            plt.plot(dotx1,dotx2,'.',ms=15,color="red")
        plt.tight_layout()

        return fig
