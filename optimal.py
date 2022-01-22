# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 01:11:31 2022

@author: aditya
"""

import numpy as np
import random

data = np.loadtxt('DATASETS/citibike/citibike_updated.csv', dtype='str',  delimiter= '/n') #load data set of citi bikes

def prediction(s, c):
    for j in range(c+1, len(seq1)):
        if seq1[j] == s:
            return j
        else:
            o = 0
    return o    
        
def evict(s, c):
    p = {x: prediction(x,c) for x in s}        
    cache.remove(max(p, key=p.get))        

seq1 = []
for i in range(25000):                                                            #extract first 25k starting location ids
    seq1.append(int(data[i+1]))
    
seq2 = [1 , 2,  3, 4, 5, 6, 1, 4, 5, 5, 6, 3, 4, 2]    
    
cache = []
cost = 0
k = 100

for i in range(len(seq1)):
    z = seq1[i]
    if z in cache:
        #print(cache)
        continue
    if i == 24999 and z not in cache:
        b = random.choice(cache)
        cache.remove(b)
        cost=cost+1
    if len(cache) < k and z not in cache:
        cache.append(z)
        #print(cache)
        continue
    if len(cache) == k and z not in cache:
        evict(cache,i)
        cache.append(z)
        cost = cost + 1
    #print(cache)  
    print(i)
print(cost)        