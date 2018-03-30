#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: samuel.niang@cern.ch
https://github.com/sniang/Solenoyds
https://sniang.github.io/Solenoyds
"""
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Solenoyds.Loop import Loop

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
            number of loops per meter
        - self.x0: float
            the x position of the loop
        - self.y0: float
            the y position of the loop
        - self.z0: float
            the z position of the loop
        - self.r0: float
            the radius of the loop
        - self.axis: string
            the axis of the solenoid
        - self.N: int(n*L)
            number of loops
        - self.loops: array(Loop)
            the loops
        
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
            number of loops per meter
        - x0: float
            the x position of the loop
        - y0: float
            the y position of the loop
        - z0: float
            the z position of the loop
        - r0: float
            the radius of the loop
        - axis: string (for now, the only acceptable value is "z")
            the axis of the solenoid
        
        * Example
            sol = Solenoid(I=400,L=1,n=100,x0=0,y0=0,z0=0,r0=0.5,axis="z")
            print(sol)
        """
        N = int(n*L)
        mu0 = 4E-7*np.pi
        B0 = mu0*n*I
        self.N = N
        self.mu0 = mu0
        self.B0 = B0
        self.L = L
        self.n = n
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r0 = r0
        self.loops = []
        self.I = I
        
        b0 = I*mu0/2/r0
        
        if N == 1:
            self.loops.append(Loop(b0,x0=x0,y0=y0,z0=z0,r0=r0))
        else:
            d = L/(N-1)
            for i in np.arange(N) :
                self.loops.append(Loop(b0,x0=x0,y0=y0,z0=z0-L/2+i*d,r0=r0))
        
        

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
        
        for loop in self.loops:
            bx, by, bz = loop.field(x,y,z)
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
                color of the loop
            - linewidth: float
                thickness of the loop
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
        
        for loop in self.loops:
            xs = loop.x0 + loop.r0*np.cos(t)
            ys = loop.y0 + loop.r0*np.sin(t)
            zs = loop.z0*np.ones(len(t))
            ax.plot(xs,ys,zs,color=color,linewidth=linewidth)
        
        return fig
    
    def displayField3D(self,figsize=(10,10),nb_points=8,colorLoop="red",colorArrow="blue",linewidth=1):
        """
        To display the field in 3D
        * Arguments
            - figsize: (float,float)
                to determine the size of the figure
            - nb_points: int
                number of points of evaluation on each axis
            - colorLoop: string
                color of the loops
            - colorArrow: string
                color of the arrows
            - linewidth: float
                thickness of the loops
                
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
        
        for loop in self.loops:
            t = np.linspace(0,2*np.pi,100)
            xs = loop.x0 + loop.r0*np.cos(t)
            ys = loop.y0 + loop.r0*np.sin(t)
            zs = loop.z0*np.ones(len(t))
            ax.plot(xs,ys,zs,color=colorLoop,linewidth=linewidth)
        
        return fig

    def displayField2D(self,eq_0="y",figsize=(10,10),nb_points=20,color="blue",markLoop=True):
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
            - markLoop: boolean
                To diplay the position of the loops
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
        
        if markLoop:
            for loop in self.loops:
                if eq_0 == "x":
                    dotx1 = np.array([-loop.r0,loop.r0])+loop.y0
                    dotx2 = [loop.z0,loop.z0]
                elif eq_0 == "y":
                    
                    dotx1 = np.array([-loop.r0,loop.r0])+loop.x0
                    dotx2 = [loop.z0,loop.z0]
                plt.plot(dotx1,dotx2,'.',ms=5,color="red")
            
        no = np.sqrt(Bx1**2+Bx2**2+Bx3**2)
        Bx1 = Bx1/no
        Bx2 = Bx2/no

        plt.quiver(x1,x2,Bx1,Bx2,color=color)
            
                
        plt.title(title,fontsize=15)
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
            sol = Solenoid(n=50)
            sol.exportFieldMap("output_map.txt",-1,1,-1,1,-1,1,20)
        """
        
        x, y, z = np.meshgrid(np.linspace(xmin,xmax,nb_points),
                              np.linspace(ymin,ymax,nb_points),
                              np.linspace(zmin,zmax,nb_points))
        x = np.concatenate(np.concatenate(x))
        y = np.concatenate(np.concatenate(y))
        z = np.concatenate(np.concatenate(z))
        Bx, By, Bz = self.field(x,y,z)
        
        with open(filename,'w') as f:
            for i in np.arange(len(x)):
                f.write(str(x[i])+';'+str(y[i])+';'+str(z[i])+';'+str(Bx[i])+';'+str(By[i])+';'+str(Bz[i])+'\n')

    def exportField(self,filename,x,y,z):
        """
        To export the field computed in some points as a .txt file
        
        * Arguments
            - filename: String
                the name of the output file
            - x: 1D np.array(float)
                the x coordinates
            - y: 1D np.array(float)
                the y coordinates
            - z: 1D np.array(float)
                the z coordinates
        * Example
            z = np.linspace(-2,2,20)
            x = np.zeros_like(z)
            y = np.zeros_like(z)
            sol = Solenoid(n=40)
            sol.exportField("output.txt",x,y,z)
        """
        
        Bx, By, Bz = self.field(x,y,z)
        
        with open(filename,'w') as f:
            for i in np.arange(len(x)):
                f.write(str(x[i])+';'+str(y[i])+';'+str(z[i])+';'+str(Bx[i])+';'+str(By[i])+';'+str(Bz[i])+'\n')
    
    def plotFieldMainAxis(self,zmin,zmax,nbpoints=100,figsize=(8,5)):
        """
        To plot the field on the main axis
        
        * Arguments
            - zmin: float
                the z min coordinate
            - zmax: float
                the z max coordinate
            - nbpoints: int
                number of points of evaluation
            - figsize: (float,float)
                the size of the figure
                
        * Returns
            - fig: matplotlib.pyplot.figure
                the figure
                
        * Example
            sol = Solenoid(n = 1000, I = 100,L = 5, z0 = 33)
            fig = sol.plotFieldMainAxis(zmin=-sol.L,zmax=sol.L)
            fig.savefig("axis_sol.png")
        """
        
        nbpoints = int(nbpoints)
        z = np.linspace(zmin,zmax,nbpoints)+self.z0
        x = np.zeros_like(z)+self.x0
        y = np.zeros_like(z)+self.y0
        
        Bx, By, Bz = self.field(x,y,z)

        fig = plt.figure(figsize=figsize)

        plt.plot(z,Bz)
        plt.xlabel(r"$z$ $(m)$",fontsize=15)
        plt.ylabel(r"$B_z$ $(T)$",fontsize=15)
        plt.title("Magnetic field on the main axis",fontsize=15)
        plt.axis([min(z),max(z),min(Bz),max(Bz)*1.1])
        plt.grid()

        
        plt.tight_layout()
        
        return fig
    
    def colormapField(self, figsize=(6,5), nbpoints=200):
        """
        To do a colormap of the field
        
        * Arguments
            - figsize: (float,float)
                the size of the figure
            - nbpoints: int
                number of points of evaluation
                
        * Returns
            - fig1,fig2,fig3: 3 matplotlib.pyplot.figure
                the figure
        
        * Example
            sol = Solenoid(n=50,x0=2,L=5)
            fig1, fig2, fig3 = sol.colormapField()
            fig1.savefig("colomap1.png")
            fig2.savefig("colomap2.png")
            fig3.savefig("colomap3.png")
        """
        
        d = np.linspace(-self.L,self.L,200)
        x, z = np.meshgrid(d,d)
        y = np.zeros_like(x)
        x += self.x0
        y += self.y0
        y += self.y0

        Bx, By, Bz = self.field(x,y,z)
        B = np.sqrt(Bx**2+By**2+Bz**2)

        m = np.max(np.abs(Bz))
        x01 = - self.r0
        z01 = - self.L/2
        x02 = self.r0
        z02 = self.L/2

        fig1 = plt.figure(figsize=(6,5))
        im = plt.imshow(Bx,cmap=plt.cm.seismic, extent=(-self.L,self.L,-self.L,self.L), origin='lower',vmin=-m,vmax=m)
        plt.plot([x01,x01],[z01,z02],lw=2,color='black')
        plt.plot([x02,x02],[z01,z02],lw=2,color='black')
        plt.colorbar(im)
        plt.title(r"$Br$",fontsize=15)
        plt.xlabel(r"$r$",fontsize=15)
        plt.ylabel(r"$z$",fontsize=15)
        plt.tight_layout()


        fig2 = plt.figure(figsize=(6,5))
        im = plt.imshow(Bz,cmap=plt.cm.seismic, extent=(-self.L,self.L,-self.L,self.L), origin='lower',vmin=-m,vmax=m)
        plt.plot([x01,x01],[z01,z02],color='black')
        plt.plot([x02,x02],[z01,z02],color='black')
        plt.colorbar(im)
        plt.title(r"$B_z$",fontsize=15)
        plt.xlabel(r"$r$",fontsize=15)
        plt.ylabel(r"$z$",fontsize=15)
        plt.tight_layout()

        fig3 = plt.figure(figsize=(6,5))
        im = plt.imshow(B,cmap=plt.cm.seismic, extent=(-self.L,self.L,-self.L,self.L), origin='lower',vmin=-m,vmax=m)
        plt.plot([x01,x01],[z01,z02],color='black')
        plt.plot([x02,x02],[z01,z02],color='black')
        plt.colorbar(im)
        plt.title(r"$|B|$",fontsize=15)
        plt.xlabel(r"$r$",fontsize=15)
        plt.ylabel(r"$z$",fontsize=15)
        plt.tight_layout()
        return fig1, fig2, fig3
        
        