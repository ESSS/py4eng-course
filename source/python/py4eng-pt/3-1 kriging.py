# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 16:37:45 2015

@author: itghisi
"""
import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
          

workdir = os.path.expanduser(r"~\Documents\pycurso")
if not os.path.isdir(workdir):
    os.mkdir(workdir)

krig_exe = os.path.join(workdir, "kb2d.exe")
krig_par = os.path.join(workdir, "kb2d.par")
krig_out = os.path.join(workdir, "kb2d.out")
    
subprocess.check_output(krig_exe + " < " + krig_par, shell=True, cwd=workdir)


ntg = np.zeros(25*25, "f64")
with open(krig_out) as ntg_file:
    for i in range(4):
        ntg_file.readline()
    for i, line in enumerate(ntg_file):
        estimation, variance = line.split()            
        ntg[i] = float(estimation.strip())


xi = np.linspace(0, 25 * 2.0, 25)
yi = np.linspace(0, 45 * 106.2447, 45)
plt.contourf(xi, xi, ntg.reshape(25,25))    
plt.colorbar()
plt.savefig("result.png")
