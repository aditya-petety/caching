#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 13:38:35 2022

@author: adityapetety
"""

import numpy as np
import random
from scipy.stats import rv_continuous

def updated_distribution(l, y):
    class exponential_dis(rv_continuous):
        def _pdf(self,x):
            return np.exp(-x**2/2.) / np.sqrt(2.0 * np.pi)
    dist = exponential_dis()    
    return max(dist.rvs(),0)  

def new_element(z, current_time):    
    return np.random.exponential(scale=scale_value[z], size=None)   

def evict(current_time,z):
    s = 10
    multiple_rp = []
    for j in range(s):
        p = {}
        for i in cache:
            p[i] = new_element(i, current_time) 
        sort_p = dict(sorted(p.items(), key=lambda x:x[1]))
        ranked = {}
        o=1
        for i in sort_p:
            ranked[i] = o
            o = o+1
        multiple_rp.append(ranked.copy()) 
        #print(ranked)
    prediction = {}
    for j in cache:
        sum = 0
        for i in range(s):
            sum = sum + multiple_rp[i][j]
        prediction[j] = sum/s
    cache.remove(max(prediction, key=prediction.get))      

    
data = np.loadtxt('DATASETS/citibike/201812-citibike-tripdata.csv', dtype='str',  delimiter= '/n')
seq = []
all_elements = []

cost = 0

for i in range(25000):
    seq.append(float(data[i+1]))
    
for i in seq:
    if i not in all_elements:
        all_elements.append(i)
        
k = 500

distribution = {}
scale_value = {}
for z in all_elements:
    scale_value[z] = 1/random.uniform(0.1, 30)
last_arrival = {}

cache = []

for i in range(len(seq)):
    z = seq[i]    
    last_arrival[z] = i   
    if len(cache) < k and z not in cache:
        cache.append(z)
        continue
    if len(cache) == k and z not in cache:
        b = evict(i, z)
        cache.append(z)
        cost = cost + 1
        
