# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 11:05:33 2022

@author: aditya
"""

import numpy as np



def prediction(s, c):
    o = 0
    for j in range(c+1, len(seq1)):
        if seq1[j] == s:
            return j 
    return o    

def evict(s, c):
    p = {x: prediction(x,c) for x in s}       
    cache1[0].remove(max(p, key=p.get)) 
    
def recent(s, c):
    o = 0    
    for j in range(c-1, -1, -1):
        if seq1[j] == s:
            return j
    return o    
        
        
def lru(s, c):
    p = {x: recent(x,c) for x in s}
    cache1[1].remove(min(p, key=p.get))    
    
data = np.loadtxt('DATASETS/citibike/citibike_updated.csv', dtype='str', delimiter = '/n')
seq1 = []
for i in range(25000):                                                            #extract first 25k starting location ids
    seq1.append(int(data[i+1]))   
k = 100                                                #list of unmarked elements
cache1 = [[], []]
cache = []
cost1 = [0,0]
cost = 0
l = 0
r = 0
for i in range(len(seq1)):
    z = seq1[i]
    if len(cache) < k and z not in cache:
        cache1[0].append(z)
        cache1[1].append(z)
        cache.append(z)
        continue
    if z not in cache1[r]:
        cost = cost + 1
    if len(cache1[0]) == k and z not in cache1[0]:          #follow the prediction part
        evict(cache1[0], i)
        cost1[0] = cost1[0] + 1
        cache1[0].append(z)
    if len(cache1[1]) == k and z not in cache1[1]:         #LRU
        lru(cache1[1], i)
        cost1[1] = cost1[1] + 1
        cache1[1].append(z)
    r = l % 2  
    r1 = (l+1) % 2
    if cost1[r] > 2 ** l:
        f = 0
        for p in cache:
            if p not in cache1[r1]:
                f = f + 1
        cache = [j for j in cache1[r1]]
        l = l + 1
        r = l % 2
        cost = cost + f