# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 10:36:57 2022

@author: aditya
"""

import numpy as np

counter = 0

def prediction(s, c):
    o = 0
    for j in range(c+1, len(seq1)):
        if seq1[j] == s:
            return j 
    return o 

def evict(s, c):
    p = {}
    global counter
    for j in cache:
        if j not in pred.keys():
            pred[j] = prediction(j, i)
            counter + counter + 1
        else:
            if pred[j] < c:
                pred[j] = prediction(j,i)
                counter = counter + 1
    p = {x: pred[x] for x in cache}  
    cache.remove(max(p, key = p.get))           

def recent(s, c):
    o = 0    
    for j in range(c-1, -1, -1):
        if seq1[j] == s:
            return j
    return o    
        
        
def lru(s, c):
    p = {x: recent(x,c) for x in s}
    cache.remove(min(p, key=p.get))   
    
data = np.loadtxt('DATASETS/citibike_updated.csv', dtype='str', delimiter = '/n')
seq1 = []
for i in range(25000):                                                            #extract first 25k starting location ids
    seq1.append(int(data[i+1]))   
k = 100   
cache = []    
pred = {}                                                                      #dictionary to keep the predictions
cost = 0
for i in range(len(seq1)):
    z = seq1[i]
    if len(cache) < k  and z not in cache:
        cache.append(z)
        continue
    r = np.random.choice([0,1], 1, p=[0.1,0.9])
    if len(cache) == k and z not in cache:
        if r[0] == 0:
            evict(cache, i)
            cost = cost + 1
            cache.append(z)
        else:
            lru(cache, i)
            cost = cost + 1
            cache.append(z)
