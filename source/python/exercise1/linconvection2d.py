import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

###variable declarations
nx = 81
ny = 81
c = 1
dx = 2.0/(nx-1)
dy = 2.0/(ny-1)

dt = 5e-3
nt = 100

# Create X and Y values (the mesh)
x = np.linspace(0,2,nx)
y = np.linspace(0,2,ny)

# Array for results
u = np.ones((ny,nx)) 
un = np.ones((ny,nx)) ##

# Assign initial conditions: u(.5<=x<=1 && .5<=y<=1 ) is 2
u[.5/dy:1/dy+1,.5/dx:1/dx+1]=2 ##set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2

# loop across number of time steps
for n in range(nt+1): ##loop across number of time steps
    un[:] = u[:]
    u[1:,1:]=un[1:,1:]-(c*dt/dx*(un[1:,1:]-un[0:-1,1:]))-(c*dt/dy*(un[1:,1:]-un[1:,0:-1]))
    # Force boundary conditions
    u[0,:]  = 1
    u[-1,:] = 1
    u[:,0]  = 1
    u[:,-1] = 1
    

def plot_surface(x, y, u):
    fig = plt.figure(figsize=(11,7), dpi=100) # the figsize parameter can be used to produce different sized images
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(x,y)
    ax.plot_surface(X,Y,u)

plot_surface(x, y, u)

