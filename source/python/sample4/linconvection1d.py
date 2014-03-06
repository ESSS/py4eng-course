# -*- coding: utf-8 -*-
import numpy as np

# solution parameters
nx = 41
c = 1
dx = 2.0/(nx-1)
dt = .025


def solve(nt):
    # solution domain
    x = np.linspace(0,2,nx)
    
    # Initialize solution vector with 1's
    u = np.ones(nx)
    # Assign initial conditions: u(.5<=x<=1 && .5<=y<=1 ) is 2
    for i in range(nx):
        if x[i] >= 0.5 and x[i] <= 1:
            u[i] = 2
    un = np.array(u)
    
    for t in range(nt):
        # Copy u values into un
        un[:] = u[:]
        u[1:] = un[1:] - c * dt/dx * (un[1:] - un[:-1])
    return x, u
