# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\WinPython-32bit-2.7.6.2\settings\.spyder2\.temp.py

"""

import os

os.chdir("C:\py4eng")


from string import Template

def create_from_template(template_filename, output_filename, keyword_values):
    """
    Create a new file by replacing keywords in a given template file
    """
    template_file = open(template_filename, "r")
    # God Practice: always close a file
    try:
        template_content = template_file.read()
        template = Template(template_content)
        content = template.substitute(keyword_values)
    finally:
        template_file.close()
    
    output_file = open(output_filename, "w")
    try:
        output_file.write(content)
    finally:
        output_file.close()


import subprocess


def run_ansys(input_filename, output_filename):
    job_name = "vm3-optimz"
    cmd_params = [
        r"C:\Program Files\ANSYS Inc\v145\ANSYS\bin\winx64\ansys145.exe",
        "-b",
        "-p",
        "ane3fl",
        "-j",
        job_name,
        "-i",
        input_filename,
        "-o",
        output_filename,
    ]
    subprocess.call(cmd_params)
    
import re

def read_results(output_filename):
    output_file = open(output_filename)
    try:
        contents = output_file.read()
    finally:
        output_file.close()
    m = re.search("STRSS_ST \(psi\).*?([\d\.]+)", contents)
    steel_stress = float(m.group(1))
    m = re.search("STRSS_CO \(psi\).*?([\d\.]+)", contents)
    copper_stress = float(m.group(1))
    return steel_stress, copper_stress
    

def evaluate(optvars):
    areas = {}
    print "Cross-sections (Steel | Copper): {0:.3} | {1:.3}".format(*optvars)
    areas["steel_area"] = optvars[0]
    areas["copper_area"] = optvars[1]
    steel_area, copper_area = optvars
    create_from_template("vm3.tpl", "vm3.out.dat", areas)
    run_ansys("vm3.out.dat", "vm3.out")
    steel_stress, copper_stress = read_results(r"vm3.out")
    print "Stress (Steel | Copper): {0:.3f} | {1:3f}".format(steel_stress, copper_stress)
    minimize_function = abs(steel_stress/3.0 - copper_stress)
    print "Objective Function: {0:.3f}".format(minimize_function)
    print
    return minimize_function
    
    
from scipy.optimize import minimize
    
def optimize():
    res = minimize(
        evaluate, 
        (0.2, 0.5), # Initial values for section areas
        method="COBYLA",
        constraints =[{'type': 'ineq', 'fun': lambda x: x[0] - 0.1},
                      {'type': 'ineq', 'fun': lambda x: x[1] - 0.1},
                      {'type': 'ineq', 'fun': lambda x: 1 - x[0]},
        ],
        options={'disp': True, 'maxiter': 20},
        )
    return res


optimize()
