#!/usr/bin/env python3

from math_print import task_1,task_2,task_3,task_4,task_5,task_6

from sys import argv

if __name__=="__main__":
    tasks=[None,task_1,task_2,task_3,task_4,task_5,task_6]
    tasks[int(argv[1])]()
