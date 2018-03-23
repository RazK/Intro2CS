#!/usr/bin/env python3

from autotest import filelist_test,res_code
from sys import argv

required = ["README",
            "hello_turtle.py",
            "math_print.py",
            ]

try:
    filelist_test(argv[1], required, format='zip')
except:
    res_code("zipfile",output="Testing zip file failed...")
    exit(-1)
