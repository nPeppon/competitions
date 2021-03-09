import numpy as np
from operator import attrgetter
import os

filenames = ['data/a.txt',
             'data/b.txt',
             'data/c.txt',
             'data/d.txt',
             'data/e.txt',
             'data/f.txt']

l = 'd'

int_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'f', 5: 'g'}
letter_to_int = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}

work_dir = os.path.join(os.getcwd(), 'hashcode2021')
print(work_dir)

f = open(os.path.join(work_dir, filenames[letter_to_int[l]]))


# Define objects involved
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
        self.optimal_out_green_timer_list.sort(
            key=lambda x: x[0], reverse=False)


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
        self.solution_street_time = []

    def addStreet(self, street):
        self.streets.append(street)

    def addTimeWithCarScoreAndStreet(self, time, car_score, street):
        if time in self.time_map:
            current_tuple = self.time_map.get(time)
            if current_tuple[0] < car_score:
                self.time_map[time] = (car_score, street)
        else:
            self.time_map[time] = (car_score, street)

    def addSolution(self, street, time_duration):
        self.solution_street_time.insert(0, [street, time_duration])

    def printSolution(self):
        out_string = str(len(self.solution_street_time)) + '\n'
        for val in self.solution_street_time:
            out_string += val[0].street_name + ' ' + str(val[1]) + '\n'
        return out_string

#     def addOptimalGreenTimeForCarScoreStreet(self, green_time, car_score, street):
#         self


class Triple():

    def __init__(self, green_time, car_score):
        self.green_time = green_time
        self.car_score = car_score


def getMostRecurringStreet(time_street_map):
    track = {}

    for key, value in time_street_map.items():
        if value not in track:
            track[value] = 0
        else:
            track[value] += 1

    return max(track, key=track.get)


def removeElemFromMapByValue(map_to_update, value):
    # in this case the value reference only the second val of the tuple
    map_to_update = {key: val for key,
                     val in map_to_update.items() if val != value}
    return map_to_update


# Parse input file
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

print('Duration ' + str(duration))


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


# In[363]:


# print(intersection_map)


# In[364]:


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


# In[365]:


# Sort car list based on their score

car_list.sort(key=lambda x: x.score, reverse=True)
# newlist = sorted(ut, key=lambda x: x.count, reverse=True)


# In[ ]:


# In[366]:


# print([x.score for x in car_list])


# In[367]:


for car in car_list:
    if (car.score >= 0):
        time = 0
        for i, street in enumerate(car.streets_list):
            if i != 0:
                time += street.time_needed_to_ride
            street.addGreenTimeCarScore(time, car.score)
            intersection_map.get(street.intersection_end).addTimeWithCarScoreAndStreet(
                time, car.score, street)


# In[357]:


filename = 'out_'+l+'.txt'

num_of_actual_inter = num_intersection
to_print = ''

# intersections_with_solution = []
with open(filename, 'a') as out:
    for idx, inter in intersection_map.items():
        if (len(inter.time_map) > 0):
            # In this solution we are not considering car score so we exclude them
            time_street_map = {key: val[1]
                               for key, val in inter.time_map.items()}

            streets = {val: 0 for key, val in time_street_map.items()}
#             print('Streets num ' + str(len(streets)))
#             print(time_street_map)
            stillSomeStreetsLeft = True
            current_offset = duration
#             print('Time street map len: ' + str(len(time_street_map)))
            while (stillSomeStreetsLeft and current_offset != 0):
                most_recurring_street = getMostRecurringStreet(time_street_map)
                time_street_map = removeElemFromMapByValue(
                    time_street_map, most_recurring_street)
                streets.pop(most_recurring_street)
                most_recurring_street.computeLoop()
                if most_recurring_street.window != -1 and most_recurring_street.offset < current_offset:
                    duration_green = current_offset - most_recurring_street.offset
                    current_offset = most_recurring_street.offset
                    inter.addSolution(most_recurring_street, duration_green)
#                 print('Time street map len inside while: ' + str(len(time_street_map)))
                elif most_recurring_street.window != -1:
                    # we need to add it at least one sec because there is at least a car with score non maximum that needs it
                    #                     print('No window')
                    duration_green = 1
                    current_offset -= 1
                    inter.addSolution(most_recurring_street, duration_green)
                if len(streets) == 0:
                    #                     print('None left')
                    stillSomeStreetsLeft = False
#             print(inter.solution_street_time)
            if current_offset != 0 and len(inter.solution_street_time) > 0:
                inter.solution_street_time[0][1] += current_offset
                current_offset = 0
            if len(inter.solution_street_time) > 0:
                to_print += str(idx) + '\n'
                to_print += inter.printSolution()
            else:
                num_of_actual_inter -= 1
        else:
            num_of_actual_inter -= 1
    to_print = str(num_of_actual_inter) + '\n' + to_print

    to_print = to_print[:-1]
    print(to_print, file=out)


# In[358]:


print('Ended')


# In[369]:


len(intersection_map.get(26).streets)


# In[ ]:
