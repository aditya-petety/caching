# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 01:20:51 2022

@author: aditya
"""

import numpy as np
import random
from scipy.stats import rv_continuous
from scipy.special import zeta


def updated_distribution(l, y):
    class exponential_dis(rv_continuous):
        def _pdf(self,x):
            return np.exp(-x**2/2.) / np.sqrt(2.0 * np.pi)
    dist = exponential_dis()    
    return max(dist.rvs(),0)  

def calc_gen_harmonic(k,n):
    return sum(1/d**n for d in range(1,k+1))

def new_element(z, current_time):    
    if dist_type[z] == 0:
        elements = []
        probabilities = []
        diff = current_time - last_arrival[z]
        s = scale_value[z]
        for i in range(100):
            elements.append(i+diff)
            d = elements[i]**(-s)/(zeta(s)-calc_gen_harmonic(diff,s))
            if d < 0:
                d=0
            if sum(probabilities) + d > 1:
                d = 1 - sum(probabilities)
            probabilities.append(d)
        l = sum(probabilities)
        elements.append(100+diff)
        probabilities.append(1-l)
        c = np.random.choice(elements, p = probabilities)  
        return c-last_arrival[z]
    else:    
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

    
data = np.loadtxt('DATASETS/citibike/201803-citibike-tripdata.csv', dtype='str',  delimiter= '/n')
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
dist_type = {}
for z in all_elements:
    dist_type[z] = random.randint(0,1)
    if dist_type[z] == 0:
        scale_value[z] = random.uniform(1.01, 5)           #for zeta function s value
    else:    
        scale_value[z] = 1/random.uniform(0.1, 3)          # for exponential distribution
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
