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
    for j in range(c+1, len(seq1)):
        if seq1[j] == s:
            return max(j , 0)

def evict(s, c):
    p = {x: prediction(x,c) for x in s}        
    cache.remove(max(p, key=p.get)) 
    unmarked.remove(max(p, key=p.get))


data = np.loadtxt('DATASETS/citibike/citibike.csv', dtype='str',  delimiter= ',') #load data set of citi bikes

seq1 = []
for i in range(25000):                                                            #extract first 25k starting location ids
    seq1.append(int(data[i+1][3]))                                                   #list of unmarked elements
marked = []
cache = []
k = 100
cost = 0
H_k = 5.187
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
    if len(cache) == k and len(marked) == k:
        r = r + 1
        q.append(0)
        n.append(0)
        S = cache
        unmarked = marked
        marked = []
    if z not in S:
        q[r] = q[r] + 1
        n[r] = 1
        unmarked = [j for j in cache if j not in marked]
        evict(unmarked, i)          #evict unmarked element with highest predicted time
        print(2)
        cache.append(z)
        if z not in marked:
            marked.append(z)
        cost  = cost + 1
    elif z in S:
        n[r] = n[r] + 1
        if n[r] <= H_k:
            unmarked = [j for j in cache if j not in marked]
            evict(unmarked, i)
            print(1)
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