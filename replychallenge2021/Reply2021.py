#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import deque
from collections import defaultdict
import math
import numpy as np
import os
from operator import attrgetter


# In[2]:


filenames = ['data/a.in',
             'data/b.in',
             'data/c.in',
             'data/d.in',
             'data/e.in',
             'data/f.in']
letter_to_int = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5}
int_to_letter = {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'f', 5 : 'g'}


letter = 'd'

filename = filenames[letter_to_int[letter]]


# In[3]:


class Building:
    
    glob_index = 0
    
    def __init__(self, x: int, y: int, bl: int, bc: int):
        self.x = x
        self.y = y
        self.bl = bl
        self.bc = bc
        self.index = Building.glob_index
        Building.glob_index = Building.glob_index + 1
        self.score = bc - bl
#         self.score = bc
        
class Antenna:
    
    glob_index = 0

    def __init__(self, ar: int, ac: int):
        self.x = -1
        self.y = -1
        self.ar = ar
        self.ac = ac
        self.index = Antenna.glob_index
        Antenna.glob_index = Antenna.glob_index + 1
#         self.score = ac - ar
        self.score = ac

    def assignCoord(self, x, y):
        self.x = x
        self.y = y
        
    def printAsSolution(self):
        return str(self.index) + ' ' + str(self.x) + ' ' + str(self.y)


# In[4]:


with open(filename, 'r') as file:
    solution = None
    buildings = []
    antennas = []

    for i, line in enumerate(file.readlines()):
        if i == 0:
            [W, H] = line.strip().split(' ')
#                 solution = Solution(int(D),I,S,V,F)
        elif i == 1:
            [N, M, R] = line.strip().split(' ')
            input_coords = np.zeros((int(N), 2))
        elif i <= int(N) + 1:
            # processing buildings
            [bx, by, bl, bc] = line.strip().split(' ')
            build_temp = Building(int(bx), int(by), int(bl), int(bc))

            buildings.append(build_temp)
#             input_coords[build_temp.index] = [int(bx), int(by)]
        else:
            # processing antennas
            [ar, ac] = line.strip().split(' ')

            antenna_temp = Antenna(int(ar), int(ac))

            antennas.append(antenna_temp)


# In[5]:


# antennas[1654].index
# input_coords


# In[6]:


buildings.sort(key=lambda x: x.score, reverse=True)
antennas.sort(key=lambda x: x.score, reverse=True)

for i, build in enumerate(buildings):
    input_coords[i] = [build.x, build.y]


# In[7]:


# input_coords


# In[8]:


# out_antennas = []

# for i in range(int(M)):
#     choosen_building = buildings[i]
#     choosen_antenna = antennas[i]
#     choosen_antenna.assignCoord(choosen_building.x, choosen_building.y)
    
#     out_antennas.append(choosen_antenna)
    
# Building.glob_index = 0
# Antenna.glob_index = 0


# In[9]:


from sklearn.cluster import KMeans
import numpy as np

kmeans = KMeans(n_clusters=int(M), random_state=0, verbose=1, max_iter=25, n_init=3).fit(input_coords)
# kmeans.labels_
# kmeans.predict([[0, 0], [12, 3]])
# kmeans.cluster_centers_


# In[10]:


# kmeans.labels_


# In[11]:


out_antennas = []

assigned_centroids = {}
for i in range(int(N)):
#     print(i)
    choosen_building = buildings[i]
    centroid = kmeans.cluster_centers_[kmeans.labels_[i]]
    if kmeans.labels_[i] not in assigned_centroids:
        assigned_centroids[kmeans.labels_[i]] = 0
        choosen_antenna = antennas[len(out_antennas)]
        choosen_antenna.assignCoord(int(round(centroid[0], 0)), int(round(centroid[1], 0)))
        out_antennas.append(choosen_antenna)
    if len(out_antennas) == int(M):
        break


# In[12]:


out_string = str(len(out_antennas)) + '\n'
for antenna in out_antennas:
    out_string += antenna.printAsSolution() + '\n'
out_string = out_string[:-1]


# In[13]:


# print(out_string)


# In[14]:


filename = 'out/out_'+letter+'.txt'
with open(filename, 'a') as out:
    print(out_string, file = out)


# In[ ]:





# In[ ]:




