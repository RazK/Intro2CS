#!/usr/bin/env python3

from autotest import filelist_test,res_code
from sys import argv

required = ["README",
            "bmi.py",
            "calculate_mathematical_expression.py",
            "convert_spoon_to_cup.py",
            "largest_and_smallest.py",
            "quadratic_equation.py",
            "shapes.py",
            ]

try:
    filelist_test(argv[1], required, format='zip')
except:
    res_code("zipfile",output="Testing zip file failed...")
    exit(-1)
