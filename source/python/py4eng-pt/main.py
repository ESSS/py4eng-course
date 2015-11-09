# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plot

print("Executável Python")
input = input("Digite um número para plotar: ")
x = np.arange(float(input))
plot.plot(x)
plot.show()