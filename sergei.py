# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 17:33:53 2022

@author: aditya
"""

import numpy as np
import random
from collections import Counter

def compare(s,t):
    return Counter(s) == Counter(t)

def prediction(s, c):
    o = 0
    for j in range(c+1, len(seq1)):
        if seq1[j] == s:
            return j
    return o    

def evict(s, c):
    p = {x: prediction(x,c) for x in s}        
    cache.remove(max(p, key=p.get)) 
    unmarked.remove(max(p, key=p.get))


#data = np.loadtxt('DATASETS/citibike/citibike.csv', dtype='str',  delimiter= ',') #load data set of citi bikes
data = np.loadtxt('DATASETS/citibike_updated.csv', dtype='str', delimiter = '/n')
seq1 = []
for i in range(25000):                                                            #extract first 25k starting location ids
    seq1.append(int(data[i+1]))                                                   #list of unmarked elements
marked = []
cache = []
seq2 = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
k = 100
cost = 0
H_k = 5
r = 1    #phase counter r
i = 1    #round counter i
q = []   #clean element counter
n = []
check = [0]
n.append(0)  #size of clean chain
n.append(0)
q.append(0)  
q.append(0) #q_1 = 0
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
            q.append(0)
            n.append(0)
            S = []
            for u in cache:        # S = cache
                S.append(u)
            unmarked = []
            for w in marked:
                unmarked.append(w)
            #unmarked = marked
            marked = []
       # print("S = ", S)   
        #print("Z=", z)
        #print("R=", r)
        if z not in S:
            q[r] = q[r] + 1
            n[r] = 1
            unmarked = [j for j in cache if j not in marked]
            evict(unmarked, i)          #evict unmarked element with highest predicted time
            #print(2)
            cache.append(z)
            if z not in marked:
                marked.append(z)
            cost  = cost + 1
        else:
            #print(1)
            n[r] = n[r] + 1
            if n[r] <= H_k:
                unmarked = [j for j in cache if j not in marked]
                evict(unmarked, i)
               # print(1)
                cost  = cost + 1
            else:
                unmarked = [j for j in cache if j not in marked]
                b = random.choice(unmarked)
                cache.remove(b)
                cost  = cost + 1
                unmarked.remove(b)
            cache.append(z) 
            if z not in marked:
                marked.append(z)
    if z not in marked:
        marked.append(z)
    #print("Cache=" ,cache)
    #print("marked",marked)
    #print("Stale (phase)", r ,S)
