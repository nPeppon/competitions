#!/usr/bin/env python
# coding: utf-8

# In[134]:


import numpy as np
from operator import attrgetter
import random
import os
import sys
import getopt


# In[181]:
debug = False
l = 'a'
simple = True
try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:l:s:", [
                               "iDebug=", "iFilenameLetter=", "iSimple"])
except getopt.GetoptError:
    print('test.py -d <isToDebug> -l <filenameLetter>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('test.py -d <isToDebug> -l <filenameLetter>')
        sys.exit()
    elif opt in ("-d", "--iDebug"):
        debug = bool(arg)
    elif opt in ("-l", "--iFilenameLetter"):
        l = str(arg)
    elif opt in ("-s", "--iSimple"):
        simple = bool(arg)

print('Debug ' + str(debug))
print('Simple ' + str(simple))

filenames = ['data/a_solar.txt',
             'data/b_dream.txt',
             'data/c_soup.txt',
             'data/d_maelstrom.txt',
             'data/e_igloos.txt',
             'data/f_glitch.txt']


int_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'f', 5: 'g'}
letter_to_int = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}

f = open(filenames[letter_to_int[l]])

print('Processing file: '+str(filenames[letter_to_int[l]]))


# In[182]:


class Person():
    def __init__(self, index, company, bonus):
        self.index = index
        self.company = company
        self.bonus = bonus
        self.placed = 0
        self.coord = []

    def getScoreWith(self, otherPerson):
        if (otherPerson != None and self.company == otherPerson.company):
            return self.bonus * otherPerson.bonus
        return 0

    def toString(self):
        return 'Id: '+str(self.index)+'\tCompany: '+str(self.company)+'\tBonus: '+str(self.bonus)


class Developer(Person):

    def __init__(self, index, company, bonus, skills):
        super(Developer, self).__init__(index, company, bonus)
        self.skills = skills
        self.numSkills = len(skills)

    def getScoreWith(self, otherPerson):
        bonus = super().getScoreWith(otherPerson)
        if (otherPerson != None and isinstance(otherPerson, Developer)):
            numCommonSkills = len(
                set(self.skills).intersection(otherPerson.skills))
            numDifferentSkills = len(self.skills) + \
                len(otherPerson.skills) - 2*numCommonSkills
            return bonus + (numCommonSkills*numDifferentSkills)
        return bonus

    def toString(self):
        return 'Dev\t'+super().toString()+'\tSkills: '+str(self.skills)


class ProjectManager(Person):
    def __init__(self, index, company, bonus):
        super(ProjectManager, self).__init__(index, company, bonus)

    def toString(self):
        return 'PM \t'+super().toString()


def convertCharForMap(char):
    if (char == '#'):
        return 0
    elif (char == '_'):
        return 1
    else:
        return 2


# Parse input file
line = f.readline()
W = int(line.split(' ')[0])
H = int(line.split(' ')[1])

office_map = np.zeros((H, W))

for h in range(H):
    line = f.readline()
    for w in range(W):
        office_map[h, w] = convertCharForMap(line[w])


companies = {}
peoplePerCompany = {}
companiesSkills = {}
companiesSkillPerPerson = {}

# Developers
line = f.readline()
D = int(line)
developers = []
for d in range(D):
    line = f.readline()
    lineSplit = line.split(' ')
    company = lineSplit[0]
    bonus = int(lineSplit[1])
    numSkills = int(lineSplit[2])
    skills = []
    for i in range(3, numSkills + 3):
        skill = lineSplit[i]
        if i == numSkills + 2:
            skill = skill[:-1]
        skills.append(skill)
    dev = Developer(d, company, bonus, skills)
    developers.append(dev)
    if company in companies:
        companies[company].append(dev)
        peoplePerCompany[company] += 1
        companiesSkills[company] += len(skills)
    else:
        companies[company] = [dev]
        peoplePerCompany[company] = 1
        companiesSkills[company] = len(skills)


# Managers
line = f.readline()
M = int(line)
managers = []
for m in range(M):
    line = f.readline()
    lineSplit = line.split(' ')
    company = lineSplit[0]
    bonus = int(lineSplit[1])
    man = ProjectManager(m, company, bonus)
    managers.append(man)
    if company in companies:
        companies[company].append(man)
        peoplePerCompany[company] += 1
    else:
        companies[company] = [man]
        peoplePerCompany[company] = 1

for company in companies:
    companiesSkillPerPerson[company] = companiesSkills[company] / \
        peoplePerCompany[company]

companiesSkillPerPersonValuesArray = np.array(
    [companiesSkillPerPerson[k] for k in companiesSkillPerPerson])
peoplePerCompanyValuseArray = np.array(
    [peoplePerCompany[k] for k in peoplePerCompany])

peoplePerCompanyNorm = {}
companiesSkillPerPersonNorm = {}
companyScore = {}
for comp in companies:
    peoplePerCompanyNorm[comp] = peoplePerCompany[comp] / \
        max(peoplePerCompanyValuseArray)
    companiesSkillPerPersonNorm[comp] = companiesSkillPerPerson[comp] / \
        max(companiesSkillPerPersonValuesArray)
    companyScore[comp] = (peoplePerCompanyNorm[comp] +
                          companiesSkillPerPersonNorm[comp]) / 2

companyScoreValuesArray = np.array([companyScore[k] for k in companyScore])

mediumScorePerCompany = companyScoreValuesArray.mean()
percentile90 = np.percentile(companyScoreValuesArray, 80)

print('-----------------------')
print('Developers: '+str(D))
if debug:
    for d in developers:
        print(d.toString())
print('Managers: '+str(M))
if debug:
    for m in managers:
        print(m.toString())
if debug:
    print('Company skill per person ratio: '+str(companiesSkillPerPerson))
    print('PeoplePerCompany:\n'+str(peoplePerCompany))
    print('Company score: '+str(companyScore))
print('Percentile90: '+str(percentile90))
print('Medium score per company; '+str(mediumScorePerCompany))
print('-----------------------')
print('Map: ('+str(W)+', '+str(H)+')')
print('-----------------------')


def getBestForArg(listToChoseIn, other=None):
    bestPer = None
    if other != None:
        max_score = 0
        for per in listToChoseIn:
            if per.placed == 0:
                score = per.getScoreWith(other)
                if score > max_score:
                    max_score = score
                    bestPer = per
    return bestPer, max_score


def getBest(listToChoseIn, upperNei=None, leftNei=None):
    bestPer = None
    if upperNei != None or leftNei != None:
        max_score = 0
        for per in listToChoseIn:
            if per.placed == 0:
                score = per.getScoreWith(upperNei)
                score += per.getScoreWith(leftNei)
                if score > max_score:
                    max_score = score
                    bestPer = per
        if bestPer != None:
            bestPer.placed = 1
    return bestPer


def getBestDev(list_of_dev, upperNei=None, leftNei=None, threshold=mediumScorePerCompany, simple=True):
    if len(list_of_dev) > 0:
        choosen = getBest(list_of_dev, upperNei, leftNei)
        if choosen == None:
            if simple:
                choosen = next((x for x in list_of_dev if getScorePerCompanyOfPerson(
                    x) >= threshold), max(list_of_dev, key=attrgetter('numSkills')))
            else:
                choosen = next((x for x in list_of_dev if getScorePerCompanyOfPerson(x) >= threshold),
                               next((x for x in list_of_dev if getScorePerCompanyOfPerson(x) >= np.percentile(companyScoreValuesArray, 75)),
                                    next((x for x in list_of_dev if getScorePerCompanyOfPerson(x) >= np.percentile(companyScoreValuesArray, 50)), max(list_of_dev, key=attrgetter('numSkills'))))
                               )
            choosen.placed = 1
        list_of_dev.remove(choosen)
        return choosen
    return None


def getBestMan(list_of_managers, upperNei=None, leftNei=None, threshold=mediumScorePerCompany, simple=True):
    if len(list_of_managers) > 0:
        choosen = getBest(list_of_managers, upperNei, leftNei)
        if choosen == None:
            if simple:
                choosen = next((x for x in list_of_managers if getScorePerCompanyOfPerson(
                    x) >= threshold), max(list_of_managers, key=attrgetter('bonus')))
            else:
                choosen = next((x for x in list_of_managers if getScorePerCompanyOfPerson(x) >= threshold),
                               next((x for x in list_of_managers if getScorePerCompanyOfPerson(x) >= np.percentile(companyScoreValuesArray, 75)),
                                    next((x for x in list_of_managers if getScorePerCompanyOfPerson(x) >= np.percentile(companyScoreValuesArray, 50)), max(list_of_managers, key=attrgetter('bonus'))))
                               )
            choosen.placed = 1
        list_of_managers.remove(choosen)
        return choosen
    return None


def getScorePerCompanyOfPerson(person):
    return companyScore[person.company]


out_map = []
devsLeft = developers.copy()
mansLeft = managers.copy()
devsleft = sorted(devsLeft, key=lambda x: getScorePerCompanyOfPerson(x))
mansLeft = sorted(mansLeft, key=lambda x: getScorePerCompanyOfPerson(x))

score = 0
for r in range(H):
    out_map.append([])
    for c in range(W):
        percentage_of_cells_analyzed = (r*W + c)/(W*H)*100
        if (percentage_of_cells_analyzed % 5 == 0):
            print(str(percentage_of_cells_analyzed) +
                  ' %,\tr: '+str(r)+'\tc: '+str(c))
        upperNei = None
        leftNei = None
        if(r >= 1 and office_map[r-1, c] != 0 and out_map[r-1][c] != 'X'):
            upperNei = out_map[r-1][c]
        if (c >= 1 and office_map[r, c-1] != 0 and out_map[r][c-1] != 'X'):
            leftNei = out_map[r][c-1]
        if office_map[r, c] == 1:  # Dev
            dev = getBestDev(devsLeft, upperNei, leftNei, percentile90, simple)
            if dev != None:
                dev.coord = [r, c]
                out_map[r].append(dev)
                score += dev.getScoreWith(upperNei) + dev.getScoreWith(leftNei)
            else:
                out_map[r].append('X')
        if office_map[r, c] == 2:  # Manager
            man = getBestMan(mansLeft, upperNei, leftNei, percentile90, simple)
            if man != None:
                man.coord = [r, c]
                out_map[r].append(man)
                score += man.getScoreWith(upperNei) + man.getScoreWith(leftNei)
            else:
                out_map[r].append('X')
        if office_map[r, c] == 0:
            out_map[r].append('X')


# In[ ]:


# In[ ]:


# In[180]:

print('---------------------------')
print('Score: ' + str(score))
print('Processing file: '+str(filenames[letter_to_int[l]]))

i = 0
filename_without_score = 'out_'+l+'_'+str(i)

matches = [f for f in os.listdir() if f.startswith(filename_without_score)]
# while(os.path.exists(filename)):
#     i += 1
#     filename = 'out_'+l+'_'+str(i)+'.txt'
while len(matches) != 0:
    i += 1
    filename_without_score = 'out_'+l+'_'+str(i)
    matches = [f for f in os.listdir() if f.startswith(filename_without_score)]

filename = filename_without_score + '_s' + str(score) + '.txt'

with open(filename, 'w') as out:
    to_print = ''
    for dev in developers:
        if dev.placed == 0:
            to_print += 'X\n'
        else:
            to_print += str(dev.coord[1])+' '+str(dev.coord[0])+'\n'
    for man in managers:
        if man.placed == 0:
            to_print += 'X\n'
        else:
            to_print += str(man.coord[1])+' '+str(man.coord[0])+'\n'
    to_print = to_print[:-1]
    print(to_print, file=out)


print('Out file: '+str(filename))
