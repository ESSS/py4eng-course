# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# ## Exercise: 2-D Linear Convection PDE using Finite Difference method
# 
# <em>This exercise was based on the Notebook [12 steps to Navier-Stokes](http://lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/) from Prof. [Lorena A. Barba](https://twitter.com/LorenaABarba)</em>

# <markdowncell>

# The PDE governing 2-D Linear Convection is written as
# 
# $$\frac{\partial u}{\partial t}+c\frac{\partial u}{\partial x} + c\frac{\partial u}{\partial y} = 0$$

# <markdowncell>

# With that in mind, our discretization of the PDE should be relatively straightforward.  
# 
# $$\frac{u_{i,j}^{n+1}-u_{i,j}^n}{\Delta t} + c\frac{u_{i, j}^n-u_{i-1,j}^n}{\Delta x} + c\frac{u_{i,j}^n-u_{i,j-1}^n}{\Delta y}=0$$
# 
# As before, solve for the only unknown:
# 
# $$u_{i,j}^{n+1} = u_{i,j}^n-c \frac{\Delta t}{\Delta x}(u_{i,j}^n-u_{i-1,j}^n)-c \frac{\Delta t}{\Delta y}(u_{i,j}^n-u_{i,j-1}^n)$$
# 
# We will solve this equation with the following initial conditions:
# 
# $$u(x) = \begin{cases}
# \begin{matrix}
# 2\ \text{for} & 0.5 \leq x \leq 1 \cr
# 1\ \text{for} & \text{everywhere else}\end{matrix}\end{cases}$$
# 
# and boundary conditions:
# 
# $$u = 1\ \text{for } \begin{cases}
# \begin{matrix}
# x =  0,\ 2 \cr
# y =  0,\ 2 \end{matrix}\end{cases}$$

# <codecell>
from mpl_toolkits.mplot3d import Axes3D


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

###variable declarations
nx = 81
ny = 81
c = 1
dt = 5e-3


def solve(nt):
    dx = 2.0/(nx-1)
    dy = 2.0/(ny-1)

    x = np.linspace(0,2,nx)
    y = np.linspace(0,2,ny)
    
    u = np.ones((ny,nx)) ##create a 1xn vector of 1's
    un = np.ones((ny,nx)) ##
    ###Assign initial conditions
    u[.5/dy:1/dy+1,.5/dx:1/dx+1]=2 ##set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2


    for n in range(nt+1): ##loop across number of time steps
        un[:] = u[:]
        u[1:,1:]=un[1:,1:]-(c*dt/dx*(un[1:,1:]-un[0:-1,1:]))-(c*dt/dy*(un[1:,1:]-un[1:,0:-1]))
        u[0,:] = 1
        u[-1,:] = 1
        u[:,0] = 1
        u[:,-1] = 1
    return x, y, u
    

def update_mesh(t):
    global surf
    x, y, u = solve(t * 3)
    surf.remove()
    surf = ax.plot_surface(X,Y,u[:])



if __name__ == "__main__":
    fig = plt.figure(figsize=(11,7), dpi=100)  ##the figsize parameter can be used to produce different sized images
    ax = fig.gca(projection='3d')
    x, y, u = solve(0)
    X, Y = np.meshgrid(x,y)
    surf = ax.plot_surface(X,Y,u)
    ax.set_zlim3d(1.0, 2.0)
    line_anim = animation.FuncAnimation(fig, update_mesh, 100, interval=10, blit=False)        
    plt.show()   



