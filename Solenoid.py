#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/solenoid.py
"""
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class Solenoid:
    """
    To simulate a solenoid
    """
    def __init__(self,B0=1,L=1,nl=100,x0=0,y0=0,z0=0,r0=0.5,axis="z"):
        """
        The constructor
        * Arguments
            -
        * Returns
            -
        """
        self.B0 = B0
        self.L = L
        self.nl = nl
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r0 = r0

    def __str__(self):
        return "B0 = "+str(self.B0)+", x0 = "+str(self.x0)+", y0 = "+str(self.y0)+", z0 = "+str(self.z0)+", r0 = "+str(self.r0)+", nl = "+str(self.nl)+", L = "+str(self.L)

    def field(self):
        """
        To compute the magnetic field
        * Arguments
            -
        * Returns
            -
        """
        return 0
    def displaySolenoid(self,figsize=(10,10)):
        """
        To display the solenoid
        * Arguments
            -
        * Returns
            -
        """
        title = r"$B_0 = "+str(self.B0)+"T, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", nl = "+str(self.nl)+", L = "+str(self.L)

        fig = plt.figure(figsize=figsize)
        ax = fig.gca(projection='3d')
        ax.set_xlabel(r"x",fontsize=15)
        ax.set_ylabel(r"y",fontsize=15)
        ax.set_zlabel(r"z",fontsize=15)
        ax.set_title(title,fontsize=15)
        return fig
    
    def displayField3D(self,figsize=(10,10)):
        """
        To display the field in 3D
        * Arguments
            -
        * Returns
            -
        """
        title = r"$B_0 = "+str(self.B0)+"T, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", nl = "+str(self.nl)+", L = "+str(self.L)

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
        title = r"$B_0 = "+str(self.B0)+"T, x_0 = "+str(self.x0)+", y_0 = "+str(self.y0)+", z_0 = "+str(self.z0)+", r_0 = $"+str(self.r0)+", nl = "+str(self.nl)+", L = "+str(self.L)

        fig = plt.figure(figsize=figsize)
        plt.title(title)
        return fig
