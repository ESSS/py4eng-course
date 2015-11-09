# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

  
includes = [
    "matplotlib.backends.backend_qt4agg",
]

setup(
    name='My Script',
    console = [{
        'dest_base'      : 'my_script',
        'script'         : 'main.py',
    }],
    options = {
        "py2exe": {
#            "bundle_files" : 2, 
		'includes'     : includes,
		'compressed'   : True,  # Compressed executable
        }
    },
	# Uncomment the line below if you are using matplotlib
	#data_files=matplotlib.get_py2exe_datafiles(),
    zipfile= 'library.zip', 
)