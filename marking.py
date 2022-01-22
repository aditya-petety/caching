# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 22:19:47 2022

@author: aditya
"""
import numpy as np
import random
from collections import Counter

def compare(s,t):
    return Counter(s) == Counter(t)

data = np.loadtxt('DATASETS/citibike_updated.csv', dtype='str',  delimiter= ',') #load data set of citi bikes

seq1 = []
for i in range(25000):                                                            #extract first 25k starting location ids
    seq1.append(int(data[i+1]))
unmarked = []                                                    #list of unmarked elements
marked = []
cache1 = []
cache2 = []
cache = []
k = 100 
cost1 = 0
cost2 = 0
cost = 0
r = 0
for i in range(25000):
    req = seq1[i]
    if req not in cache and len(cache) < k:
        cache.append(req)
        marked.append(req)
        continue
    if req in cache and req not in marked:
        marked.append(req)
        continue
    if req not in cache:
        if len(cache) == k and len(marked) == k:
            r = r + 1
            unmarked = [j for j in marked]
            marked = []
        else:
            unmarked = [j for j in cache if j not in marked]
        b = random.choice(unmarked)
        unmarked.remove(b)
        cache.remove(b)
        cache.append(req)
        marked.append(req)
        cost = cost + 1
