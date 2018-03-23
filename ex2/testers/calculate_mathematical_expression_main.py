#!/usr/bin/env python3

from calculate_mathematical_expression import calculate_from_string

if __name__=="__main__":
    print('The answer is:',calculate_from_string(input('Enter expression string: ')))
