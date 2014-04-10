"""

  To build an executable for this application, just open a 
  command prompt and run:
  
  > python setup.py build
  
  A directory "dist" will be created in the same with all necessary
  files for distribution.

"""
from guidata.disthelpers import Distribution


dist = Distribution()
dist.setup(name="Linear Convection 1D",
           version='1.0.0',
           description="",
           script="main.pyw",
           target_name="linconvection1d_gui.exe")
dist.add_modules('guidata')
dist.add_matplotlib()
dist.build('cx_Freeze')
