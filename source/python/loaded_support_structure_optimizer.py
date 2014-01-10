# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:57:13 2014

@author: igor
"""
import subprocess
import os
import re
from string import Template
from scipy.optimize import minimize


class LoadedSupportStructureOptimizer(object):
    
    def __init__(self):
        self.stress_ratio = 3.0
        self.max_iterations = 40
        self.working_dir = ""
        
        
    def create_from_template(self, template_filename, output_filename, keyword_values):
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
            

    def run_ansys(self, input_filename, output_filename):
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
        
        
    def read_stress(self, output_filename):
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


    def evaluate_stress_ratio(self, values):
        areas = {}
        areas["copper_area"] = values[0]
        areas["steel_area"] = values[1]
        
        dat_file = r"C:\Users\igor\course\vm3.dat"
        output_file = r"C:\Users\igor\course\vm3.out"
        self.create_from_template(r"C:\Users\igor\course\vm3.tpl", dat_file, areas)
        self.run_ansys(r"C:\Users\igor\course\vm3.dat", output_file)
        try:
            copper, steel = self.read_stress(output_file)
        except AttributeError:
            return 100
        return abs(steel / copper - 3)
        
        
    def optimize(self):
        res = minimize(
                self.evaluate_stress_ratio,
                (0.2, 0.5),
                method="COBYLA",
                constraints =[{'type': 'ineq', 'fun': lambda x: x[0] - 0.1},
                              {'type': 'ineq', 'fun': lambda x: x[1] - 0.1},
                              {'type': 'ineq', 'fun': lambda x: 1 - x[0]},
                ],
                options={'disp': True, 'maxiter': 20},
                )
        return res

if __name__ == "__main__":
    sup = LoadedSupportStructureOptimizer()
    sup.optimize()
