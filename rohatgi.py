# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 18:50:39 2022

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
    global counter
    p = {x: prediction(x,c) for x in s}
    counter = counter + len(p)     
    cache.remove(max(p, key=p.get)) 
    unmarked.remove(max(p, key=p.get))
    evicted.append(max(p,key=p.get))


#data = np.loadtxt('DATASETS/citibike/citibike.csv', dtype='str',  delimiter= ',') #load data set of citi bikes
data = np.loadtxt('DATASETS/citibike_updated.csv', dtype='str', delimiter = '/n')
seq1 = []
for i in range(25000):                                                            #extract first 25k starting location ids
    seq1.append(int(data[i+1]))                                                   #list of unmarked elements
marked = []
cache = []
evicted = []
seq2 = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
k = 100
cost = 0
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
            evicted = []
            S = []
            for u in cache:        # S = cache
                S.append(u)
            unmarked = []
            for w in marked:
                unmarked.append(w)
            marked = []
        if z not in S:
            unmarked = [j for j in cache if j not in marked]
            evict(unmarked, i)          #evict unmarked element with highest predicted time
            cache.append(z)
            if z not in marked:
                marked.append(z)
            cost  = cost + 1
        elif z in evicted:
            b = random.choice(cache)
            cache.remove(b)
            if b in marked:
                marked.remove(b)
            if b in unmarked:
                unmarked.remove(b)
            cache.append(z)
            marked.append(z)
            cost = cost + 1
        else:
            unmarked = [j for j in cache if j not in marked]
            d = random.choice(unmarked)
            cache.remove(d)
            unmarked.remove(d)
            cost += 1
            cache.append(z)
            marked.append(z)
