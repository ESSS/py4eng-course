#### Building linconvection1d Application

This is a sample application which solves a linear convection 1D problem in an 
interactive way (you can change the *Num. Steps* variable and see the results).

The application entry point is the file `main.pyw`. It ends with the `pyw` 
extension so our executable generator recognize it as a GUI application
(not a console one).

To build an executable from this code, just run
 
    python setup.py build

in this directory. A directory "dist" will be created with all necessary files
for distribution.