# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:56:38 2015

@author: igor
"""

import numpy as np
import matplotlib.pyplot as plot
from scipy.optimize import curve_fit, root, fixed_point
from scipy.integrate import quad

def well_flow(t, qi, ai, n):
    return qi / (1 + n * ai * t) ** (1 / n)
    

t = np.arange(0, 6)
ofr = well_flow(t, 100, 0.28, 1/2)
history_data = [
    100,
    77,
    61,
    49.5,
    41,
    34.5,
]

params, _ = curve_fit(well_flow, t, history_data, p0=[100, 0.5, 1/3])
print(params)

plot.plot(t, well_flow(t, *params))
plot.plot(t, history_data, "ro")
plot.ylim(0, 100)

plot.show()

objfunc = lambda x: well_flow(x, 100, 0.28, 0.5) - 5
sol = root(objfunc, 10)
print(sol.x)


sol = fixed_point(well_flow, [5], (100, 0.28, 0.5))
print(sol)


y, _ = quad(well_flow, 0, 24.8, (100, 0.28, 1/2))
print(y*365)
