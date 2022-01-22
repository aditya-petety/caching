# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 17:55:50 2022

@author: aditya
"""

import numpy as np
import random

counter = 0


def prediction(s, c):
    o = 0
    for j in range(c+1, len(seq1)):
        if seq1[j] == s:
            return j  #np.random.lognormal(mean = 0, sigma=1, size = None)
    return o    

def evict(s, c):
    p = {x: prediction(x,c) for x in s}   
    global counter
    counter = counter + len(p)     
    cache.remove(max(p, key=p.get)) 
    unmarked.remove(max(p, key=p.get))


#data = np.loadtxt('DATASETS/citibike/citibike.csv', dtype='str',  delimiter= ',') #load data set of citi bikes
data = np.loadtxt('DATASETS/citibike/citibike_updated.csv', dtype='str', delimiter = '/n')
seq1 = []
for i in range(25000):                                                            #extract first 25k starting location ids
    seq1.append(int(data[i+1]))                                                   #list of unmarked elements
marked = []
cache = []
evicted = []
seq2 = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
k = 100
cost = 0
b = 1
r = 1    #phase counter r
S = []   #tracking set
for i in range(len(seq1)):
    z = seq1[i]
    if z not in cache and len(cache) < k:
        cache.append(z)
        marked.append(z)
        continue
    if z in cache and z not in marked:
        marked.append(z)
        continue
    if z in cache and z in marked:
        continue
    if z not in cache:
        if len(cache) == k and len(marked) == k:
            r = r + 1
            unmarked = []
            for u in marked:
                unmarked.append(u)
            marked = []
        else:
            unmarked = [j for j in cache if j not in marked]
            d = random.sample(unmarked, min(b,len(unmarked)))
            evict(d, i)
            marked.append(z)
            cache.append(z)
            cost = cost + 1
print(counter)            