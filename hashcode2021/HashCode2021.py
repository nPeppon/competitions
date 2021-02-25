#!/usr/bin/env python
# coding: utf-8

# In[30]:


import numpy as np
from operator import attrgetter


# In[422]:


filenames = ['data/a.txt',
             'data/b.txt',
             'data/c.txt',
             'data/d.txt',
             'data/e.txt',
             'data/f.txt']


# In[487]:


l = 'f'

int_to_letter = {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'f', 5 : 'g'}
letter_to_int = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5}

f = open(filenames[letter_to_int[l]])


# In[488]:


#Define objects involved
class Street():
    
    def __init__(self, index, intersection_start, intersection_end, street_name, time_needed_to_ride):
        self.index = index
        self.intersection_start = intersection_start
        self.intersection_end = intersection_end
        self.street_name = street_name
        self.time_needed_to_ride = time_needed_to_ride
        self.optimal_out_green_time = []
        self.loop = -1
        self.window = -1
        self.offset = -1
        
    def addGreenTimeCarScore(self, green_time, car_score):
        self.optimal_out_green_time.append((green_time, car_score))
        
    def computeLoop(self):
        time_set = list(set([x[0] for x in self.optimal_out_green_time]))
        time_set.sort(key=lambda x: x, reverse=False)
        if (len(time_set) == 0):
            pass
        elif (len(time_set) == 1):
            self.loop = time_set[0]
            self.offset = 0
            self.window = 1
        else:
            self.offset = time_set[0]
            temp_sum = 0
            for i in range(1, len(time_set)):
                temp_sum += (time_set[i] - time_set[i - 1])
            loop = temp_sum / (len(time_set) - 1)
            self.loop = int(loop)
            resto = loop % self.loop
            resto = abs(0.5 - resto)

            if (resto < 0.1):
                self.window = int(self.loop / 2)
            elif (resto < 0.3):
                self.window = int(self.loop / 3)
            else:
                self.window = 1
        
    def sortTimeCarScoreList():
        self.optimal_out_green_timer_list.sort(key=lambda x: x[0], reverse=False)

        
class Car():
    
    def __init__(self, index, num_streets_to_cross):
        self.index = index
        self.num_streets_to_cross = num_streets_to_cross
        self.streets_list = []
        self.total_minimum_time = 0
        self.score = 0
        
    def addStreetToList(self, street):
        self.streets_list.append(street)
        if (len(self.streets_list) != 1):
            self.total_minimum_time += street.time_needed_to_ride
        
    def computeScore(self, total_time):
        self.score = (total_time - self.total_minimum_time)/total_time
        
class Intersection():
    
    def __init__(self, index):
        self.index = index
        self.streets = []
        self.time_map = {}
        self.loop = -1
        self.window = -1
        self.offset = -1
        self.out = {}
        
    def addStreet(self, street):
        self.streets.append(street)
                
    def addTimeWithCarScoreAndStreet(self, time, car_score, street):
        if time in self.time_map:
            current_tuple = self.time_map.get(time)
            if current_tuple[0] < car_score:
                self.time_map[time] = (car_score, street)
        else:
            self.time_map[time] = (car_score, street)
            
#     def addOptimalGreenTimeForCarScoreStreet(self, green_time, car_score, street):
#         self
        
class Triple():
    
    def __init__(self, green_time, car_score):
        self.green_time = green_time
        self.car_score = car_score
        
def getMostRecurringStreet(time_street_map):
    track={}

    for key,value in time_street_map.items():
        if value not in track:
            track[value]=0
        else:
            track[value]+=1

    return max(track,key=track.get)
    


# In[489]:


#Parse input file
print('Reading first line')
line = f.readline()
D = int(line.split(' ')[0])
I = int(line.split(' ')[1])
S = int(line.split(' ')[2])
V = int(line.split(' ')[3])
F = int(line.split(' ')[4])

duration = D
num_intersection = I
num_streets = S
num_cars = V
bonus = F


# In[490]:


# Looping through streets
street_list = []
streets_map = {}
intersection_map = {}
for s in range(S):
    line = f.readline()
    lineSplit = line.split(' ')
    intersection_start = int(lineSplit[0])
    intersection_end = int(lineSplit[1])
    name = lineSplit[2]
    time_needed = int(lineSplit[3])
    street = Street(s, intersection_start, intersection_end, name, time_needed)
    street_list.append(street)
    streets_map[name] = street
    
    if (intersection_end in intersection_map):
        intersection_map.get(intersection_end).addStreet(street)
    else:
        intersection_out_object = Intersection(intersection_end)
        intersection_out_object.addStreet(street)
        intersection_map[intersection_end] = intersection_out_object
    


# In[491]:


# print(intersection_map)


# In[492]:


# Looping through cars
car_list = []

for v in range(V):
    line = f.readline()
    # Split first the newline to avoid it
    lineSplit = line.split('\n')[0].split(' ')
    num_streets = int(lineSplit[0])
    car = Car(v, num_streets)
    for i in range(num_streets):
        car.addStreetToList(streets_map.get(lineSplit[i + 1]))
    car.computeScore(duration)
    car_list.append(car)


# In[493]:


#Sort car list based on their score

car_list.sort(key=lambda x: x.score, reverse=True)
# newlist = sorted(ut, key=lambda x: x.count, reverse=True)


# In[494]:


# print([x.score for x in car_list])


# In[495]:


for car in car_list:
    if (car.score >= 0):
        time = 0
        for i, street in enumerate(car.streets_list):
            if i != 0:
                time += street.time_needed_to_ride
            street.addGreenTimeCarScore(time, car.score)
            intersection_map.get(street.intersection_end).addTimeWithCarScoreAndStreet(time, car.score, street)


# In[496]:


filename = 'out_'+l+'.txt'

num_of_actual_inter = num_intersection
to_print = ''
with open(filename, 'a') as out:
    for idx,inter in intersection_map.items():
        if (len(inter.time_map) != 0):
            to_print += str(idx) + '\n'
            most_recurring_street = getMostRecurringStreet(inter.time_map)
            most_recurring_street[1].computeLoop()
            found = False
            num_added_streets = 1
            street_string = ''
            current_offset = most_recurring_street[1].offset
            if current_offset > 0 :
                for idxx,street in enumerate(inter.streets):
#                     print(idxx)
                    street.computeLoop()
                    if street.window != -1 and street != most_recurring_street[1] and street.offset < current_offset:
#                         print('Sono entrato')
                        num_added_streets += 1
                        duration = 0
                        if idxx == (len(inter.streets) - 1):
#                             print('Trovato ultima strada')
                            duration = current_offset
                            current_offset = 0
                        else:
                            duration = current_offset - street.offset
                            current_offset = street.offset
                        street_string = street.street_name + ' ' + str(duration) + '\n' + street_string               
            street_string += most_recurring_street[1].street_name +  ' ' + str(most_recurring_street[1].window) + '\n'
            to_print += str(num_added_streets) + '\n' + street_string
        else:
            num_of_actual_inter -= 1
    to_print = str(num_of_actual_inter) + '\n' + to_print
            
    
    to_print = to_print[:-1]
    print(to_print, file = out)
    
    


# In[ ]:





# In[ ]:




