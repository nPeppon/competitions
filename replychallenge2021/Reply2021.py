#!/usr/bin/env python
# coding: utf-8


import math
import numpy as np
import os
from operator import attrgetter
from sklearn.cluster import KMeans


letter = 'a'
challenge = 'replychallenge2021'
radius_threshold = 30


filenames = ['data/a.in',
             'data/b.in',
             'data/c.in',
             'data/d.in',
             'data/e.in',
             'data/f.in']
letter_to_int = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
int_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'f', 5: 'g'}


work_dir = os.path.join(os.getcwd(), challenge)
filename = os.path.join(work_dir, filenames[letter_to_int[letter]])

out_filename_relative = 'out/out_'+letter+'.txt'
out_filename = os.path.join(work_dir, out_filename_relative)


# Jupyter notebook does not handle absolute paths correctly, so going into relative
if not os.path.exists(filename):
    print('We are using Jupyter -> relative paths')
    filename = filenames[letter_to_int[letter]]
    out_filename = out_filename_relative


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


with open(filename, 'r') as file:
    buildings = []
    antennas = []
    antennas_withRadiusMoreTen = []
    antennas_withoutRadiusMoreTen = []
    for i, line in enumerate(file.readlines()):
        if i == 0:
            [W, H] = line.strip().split(' ')
        elif i == 1:
            [N, M, R] = line.strip().split(' ')
            input_coords = np.zeros((int(N), 2))
        elif i <= int(N) + 1:
            # processing buildings
            [bx, by, bl, bc] = line.strip().split(' ')
            build_temp = Building(int(bx), int(by), int(bl), int(bc))

            buildings.append(build_temp)
        else:
            # processing antennas
            [ar, ac] = line.strip().split(' ')

            antenna_temp = Antenna(int(ar), int(ac))
            if int(ar) >= radius_threshold:
                antennas_withRadiusMoreTen.append(antenna_temp)
            else:
                antennas_withoutRadiusMoreTen.append(antenna_temp)
            antennas.append(antenna_temp)


# Approach
# If num_build = num_antennas (input file c) then let's put an antenna for building
# Otherwise:
#  1. We assign the antennas with radius <= radius_threshold directly to the best building, so we are sure they are covered
#  2. The remaining antennas (with longer radius) are placed at the centroid of the clusters we find with kmeans


buildings.sort(key=lambda x: x.score, reverse=True)
antennas.sort(key=lambda x: x.ar, reverse=True)

# Let's sort the antennas with short range by connection speed since we will place them directly on the building
antennas_withoutRadiusMoreTen.sort(key=lambda x: x.ac, reverse=True)
# While the remainings by their radius
antennas_withRadiusMoreTen.sort(key=lambda x: x.ar, reverse=True)

# let's keep track of the points in the map where we put antennas, to not duplicate them
points_filled = {}


# Let's place the antennas with short range on the "most important" buildings
out_antennas_withoutRange = []
for i in range(len(antennas_withoutRadiusMoreTen)):
    # Let's remove the building from the list so it is not considered in subsequent clusterization
    choosen_building = buildings.pop(0)
    choosen_antenna = antennas_withoutRadiusMoreTen[i]
    choosen_antenna.assignCoord(choosen_building.x, choosen_building.y)
    points_filled[(choosen_building.x, choosen_building.y)] = 1
    out_antennas_withoutRange.append(choosen_antenna)


for i, build in enumerate(buildings):
    input_coords[i] = [build.x, build.y]


# We search for as many clusters as many antennas with long range we have. iterations and n_init to be tweaked
if len(antennas_withRadiusMoreTen) != 0:
    kmeans = KMeans(n_clusters=len(antennas_withRadiusMoreTen),
                    random_state=0, verbose=1, max_iter=25, n_init=3).fit(input_coords)
# kmeans.labels_
# kmeans.predict([[0, 0], [12, 3]])
# kmeans.cluster_centers_


# Let's place the antennas with long range into the centroids to which the most important buildings are placed,
# paying attention to not place an antenna over another, thus slightly changing the coords
out_antennas_withRange = []

if len(antennas_withRadiusMoreTen) != 0:
    assigned_centroids = {}
    for i in range(len(buildings)):
        choosen_building = buildings[i]
        centroid = kmeans.cluster_centers_[kmeans.labels_[i]]
        coord = (int(round(centroid[0], 0)), int(round(centroid[1], 0)))
        if kmeans.labels_[i] not in assigned_centroids:
            if coord in points_filled:
                if (coord[0]+1, coord[1]) not in points_filled:
                    coord = (coord[0]+1, coord[1])
                elif (coord[0]-1, coord[1]) not in points_filled:
                    coord = (coord[0]-1, coord[1])
                elif (coord[0], coord[1]+1) not in points_filled:
                    coord = (coord[0], coord[1]+1)
                elif (coord[0], coord[1]-1) not in points_filled:
                    coord = (coord[0], coord[1]-1)
                else:
                    print('non ho trovato niente')

            if coord not in points_filled:
                assigned_centroids[kmeans.labels_[i]] = 0
                points_filled[coord] = 1
                choosen_antenna = antennas_withRadiusMoreTen[len(
                    out_antennas_withRange)]
                choosen_antenna.assignCoord(coord[0], coord[1])
                out_antennas_withRange.append(choosen_antenna)
            else:
                pass
                print('Ancora già preso')

        if len(out_antennas_withRange) == len(antennas_withRadiusMoreTen):
            break


out_string = str(len(out_antennas_withRange) +
                 len(out_antennas_withoutRange)) + '\n'
for antenna in out_antennas_withRange:
    out_string += antenna.printAsSolution() + '\n'
for antenna in out_antennas_withoutRange:
    out_string += antenna.printAsSolution() + '\n'
out_string = out_string[:-1]


# print(out_string)


with open(out_filename, 'a') as out:
    print(out_string, file=out)
