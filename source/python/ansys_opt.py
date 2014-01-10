# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\igor\WinPython\settings\.spyder2\.temp.py
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 07 16:27:44 2014

@author: igor
"""
import subprocess
import os
import re
from string import Template
import numpy as np
from scipy.optimize import minimize


stress_ratio = 3.0

def create_from_template(template_filename, output_filename, keyword_values):
    """
    Create a new file by replacing keywords in a given template file
    """
    template_file = open(template_filename, "r")
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
    subprocess.call(cmd_params, cwd=os.path.dirname(input_filename))
    
    
def read_stress(output_filename):
    output_file = open(output_filename)
    try:
        output = output_file.read()
    finally:
        output_file.close()
        
    m_steel = re.search("STRSS_ST \(psi\)\s+(.+)\s", output)
    strss_steel = float(m_steel.group(1))
    m_copper = re.search("STRSS_CO \(psi\)\s+(.+)\s", output)
    strss_copper = float(m_copper.group(1))
    
    return strss_copper, strss_steel
    
    
def evaluate_structure_cost(values):
    print values
    areas = {}
    areas["copper_area"] = values[0]
    areas["steel_area"] = values[1]
    create_from_template("vm3.tpl", "vm3.dat", areas)
    run_ansys(r"C:\Users\igor\course\vm3.dat", "vm3.out")
    copper, steel = read_stress("vm3.out")
    if copper > 5e3 or steel > 15e3:
        return 100
    steel_cost = 0.6
    copper_cost = 3.33
    cost = ( areas["copper_area"] * copper_cost * 20) + (areas["steel_area"] * steel_cost * 10)
    print "$%f" %cost
    print
    return cost
    
    
def evaluate_stress_difference(values):
    areas = {}
    areas["copper_area"] = values[0]
    areas["steel_area"] = values[1]
    create_from_template("vm3.tpl", "vm3.dat", areas)
    run_ansys(r"C:\Users\igor\course\vm3.dat", "vm3.out")
    try:
        copper, steel = read_stress("vm3.out")
    except AttributeError:
        return 100
    return abs(steel / copper - 3)


def optimize():
    res = minimize(
            evaluate_stress_difference,
            (0.2, 0.5),
            method="COBYLA",
            constraints =[{'type': 'ineq', 'fun': lambda x: x[0] - 0.1},
                          {'type': 'ineq', 'fun': lambda x: x[1] - 0.1},
                          {'type': 'ineq', 'fun': lambda x: 1 - x[0]},
            ],
            options={'disp': True, 'maxiter': 20},
            )
    return res
        