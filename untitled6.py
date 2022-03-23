# -*- coding: utf-8 -*-


import numpy as np
import random
from scipy.special import zeta
import scipy.special as sc
import math

def prediction(s, c):                     #follow the prediction (optimal)
    o =1000
    for j in range(c+1, len(seq)):
        if seq[j] == s:
            return j
    return o  
        
def evict2(s, c):
    p = {x: prediction(x,c) for x in s}        
    cache2.remove(max(p, key=p.get))  


def recent(s, c):                                  #lru
    o = 0    
    for j in range(c-1, -1, -1):
        if seq[j] == s:
            return j
    return o    
        
        
def lru(s, c):                                     #lru
    p = {x: recent(x,c) for x in s}
    cache1.remove(min(p, key=p.get))

def calc_gen_harmonic(k,n):
    return sum(1/d**n for d in range(1,k+1))

def new_element(z, current_time):    
    if dist_type[z] == 0:    
        s = zeta_values[z]                                                        #conditional for zipf
        elements = []
        probabilities = []
        diff = current_time - last_arrival[z]
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
        return c - diff
    else:    
        s = poisson_values[z]
        diff = current_time-last_arrival[z]
        elements = []
        probabilities = []
        for i in range(100):
            elements.append(i+diff)
            if sc.gammaincc(elements[i]+1, s) == 1:
                d=0
            else:
                d = s**(elements[i])*math.exp(-s)/(math.factorial(elements[i])*(1-sc.gammaincc(elements[i]+1,s)))
            if d < 0:
                d = 0
            if sum(probabilities) + d > 1:
                d = 1 - sum(probabilities)
            probabilities.append(d)
        l = sum(probabilities)
        elements.append(100+diff)
        probabilities.append(1-l)
        c = np.random.choice(elements, p = probabilities)  
        return c - diff    

def evict1(current_time,z):                                                            #evicting max expected rank
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

def expected_arrival(current_time, z):
    if dist_type[z] == 0:    
        s = zeta_values[z]                                                        #conditional for zipf
        elements = []
        probabilities = []
        diff = current_time - last_arrival[z]
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
        val = sum([elements[i]*probabilities[i] for u in range(len(elements))])
        return val
    else:    
        s = poisson_values[z]
        diff = current_time-last_arrival[z]
        elements = []
        probabilities = []
        for i in range(100):
            elements.append(i+diff)
            if sc.gammaincc(elements[i]+1,s) == 1:
                d=0
            else:    
                d = s**(elements[i])*math.exp(-s)/(math.factorial(elements[i])*(1-sc.gammaincc(elements[i]+1,s)))
            if d < 0:
                d = 0
            if sum(probabilities) + d > 1:
                d = 1 - sum(probabilities)
            probabilities.append(d)
        l = sum(probabilities)
        elements.append(100+diff)
        probabilities.append(1-l)    
        val = sum([elements[i]*probabilities[i] for u in range(len(elements))])
        return val


    
def evict(current_time,z):                                                             #used for evicting max expected arrivaql time
     exp_arrival = {}
     for a in cache:
         #print(a)
         exp_arrival[a] = expected_arrival(current_time, a)
     cache.remove(max(exp_arrival, key=exp_arrival.get))
                  
zeta_values = {}
poisson_values = {}
dist_type = {}

for j in range(100):                                                                 #randomly assigning a distribution to each of the 100 elements
    if random.randint(1,1) == 0:
        zeta_values[j] = random.uniform(1.5,3)
        dist_type[j] = 0
    else:
        poisson_values[j] = random.uniform(30,80)
        dist_type[j] = 1

seq = []

next_arrival = {}

for j in range(100):                                                                 #sampling the next arrival time
    if j in zeta_values.keys():
        next_arrival[j] = np.random.zipf(zeta_values[j])
    else:
        next_arrival[j] = np.random.poisson(poisson_values[j])

while len(seq) < 1000:                                                               #constructing the sequence
    for j in range(100):
        a = min(next_arrival, key=next_arrival.get)
    seq.append(a)
    if a in zeta_values.keys():
        next_arrival[a] = next_arrival[a] + np.random.zipf(zeta_values[a])
    elif a in poisson_values.keys():
        next_arrival[a] = next_arrival[a] + np.random.poisson(poisson_values[a])   
        
cache = []
cost = 0     
k = 50    
last_arrival = {}
        
for i in range(len(seq)):
    z = seq[i]    
    last_arrival[z] = i  
    #print(i)
    if len(cache) < k and z not in cache:
        cache.append(z)
        continue
    if len(cache) == k and z not in cache:
        b = evict1(i, z)
        cache.append(z)
        cost = cost + 1     
        
cost1 = 0
cache1 = []

for i in range(len(seq)):                                                            #lru
    z = seq[i]
    if z not in cache1 and len(cache1) < k:
        cache1.append(z)
    if z not in cache1 and len(cache1) == k:
        lru(cache1,i)
        cost1 = cost1+1
        cache1.append(z)        
        
cost2 = 0
cache2 = []    

for i in range(len(seq)):                                                              #optimum
    z = seq[i]
    if z in cache2:
        #print(cache)
        continue
    if i == 999 and z not in cache2:
        b = random.choice(cache2)
        cache2.remove(b)
        cost2=cost2+1
    if len(cache2) < k and z not in cache2:
        cache2.append(z)
        #print(cache)
        continue
    if len(cache2) == k and z not in cache2:
        evict2(cache2,i)
        cache2.append(z)
        cost2 = cost2 + 1    
        
print("Cost of optimum is:", cost2  )
print("Cost of LRU is:", cost1)
print("Cost of algorithm is :", cost)        