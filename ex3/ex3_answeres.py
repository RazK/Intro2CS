#!/usr/bin/env python3

def create_list():
    return list(iter(input,''))

def concat_list(str_list):
    return ''.join(str_list)

def average(num_list):
    return sum(num_list)/len(num_list) if num_list else None

def cyclic(lst1,lst2):
    return (len(lst1)==len(lst2) and 
            (any(lst1==lst2[i:]+lst2[:i] for i in range(len(lst2))) or
             not lst1))

def histogram(n,num_list):
    return [num_list.count(i) for i in range(n)]

def prime_factors(n):
    res = []
    cur = 2
    while cur <= n:
        if n % cur:
            cur+=1
        else:
            res.append(cur)
            n //= cur
    return res

def cartesian(lst1, lst2):
    return [[a,b] for a in lst1 for b in lst2]

def pairs(n,num_list):
    return [[a,n-a] for a in num_list if a<n-a and n-a in num_list]
