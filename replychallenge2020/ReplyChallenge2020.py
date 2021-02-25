#!/usr/bin/env python
# coding: utf-8

# In[134]:


import numpy as np
from operator import attrgetter


# In[181]:


filenames = ['data/a_solar.txt', 
             'data/b_dream.txt',
             'data/c_soup.txt',
             'data/d_maelstrom.txt',
             'data/e_igloos.txt', 
             'data/f_glitch.txt']

l = 'c'

int_to_letter = {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'f', 5 : 'g'}
letter_to_int = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5}

f = open(filenames[letter_to_int[l]])


# In[182]:


class Person():
    def __init__(self, index, company, bonus):
        self.index = index
        self.company = company
        self.bonus = bonus
        self.placed = 0
        self.coord = []
        
    def getScoreWith(self, otherPerson):
        if (otherPerson != None and self.company == otherPerson.company) :
            return self.bonus * otherPerson.bonus
        return 0

class Developer(Person):
    
    def __init__(self, index, company, bonus, skills):
        super(Developer, self).__init__(index, company, bonus)
        self.skills = skills
        self.numSkills = len(skills)
    
    def getScoreWith(self, otherPerson):
        bonus = super().getScoreWith(otherPerson)
        if (otherPerson != None and isinstance(otherPerson, Developer)):
            numCommonSkills = len(set(self.skills).intersection(otherPerson.skills))
            numDifferentSkills = len(self.skills) + len(otherPerson.skills) - 2*numCommonSkills
            return bonus + (numCommonSkills*numDifferentSkills)
        return bonus
        
class ProjectManager(Person):
     def __init__(self, index, company, bonus):
        super(ProjectManager, self).__init__(index, company, bonus)

def convertCharForMap(char):
    if (char == '#'):
        return 0
    elif (char == '_'):
        return 1
    else:
        return 2
    
def getBestForArg(listToChoseIn, other = None):
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
     
def getBest(listToChoseIn, upperNei = None, leftNei = None):
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

def getBestDev(list_of_dev, upperNei = None, leftNei = None):
    if len(list_of_dev) > 0:
        choosen = getBest(list_of_dev, upperNei, leftNei)
        if choosen == None:
            choosen = max(list_of_dev, key=attrgetter('numSkills'))
            choosen.placed = 1
        list_of_dev.remove(choosen)
        return choosen
    return None

def getBestMan(list_of_managers, upperNei = None, leftNei = None):
    if len(list_of_managers) > 0:
        choosen = getBest(list_of_managers, upperNei, leftNei)
        if choosen == None:
            choosen = max(list_of_managers, key=attrgetter('bonus'))
            choosen.placed = 1
        list_of_managers.remove(choosen)
        return choosen
    return None


# In[183]:


#Parse input file
print('Reading first line')
line = f.readline()
W = int(line.split(' ')[0])
H = int(line.split(' ')[1])


# In[184]:


office_map = np.zeros((H,W))


# In[185]:


for h in range(H):
    line = f.readline()
    for w in range(W):
        office_map[h,w] = convertCharForMap(line[w])


# In[186]:


companies = {}


# In[188]:


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
        skills.append(lineSplit[i])
    developers.append(Developer(d, company, bonus, skills))


# In[189]:


# Managers
line = f.readline()
M = int(line)
managers = []
for m in range(M):
    line = f.readline()
    lineSplit = line.split(' ')
    company = lineSplit[0]
    bonus = int(lineSplit[1])
    managers.append(ProjectManager(m, company, bonus))


# In[ ]:





# In[190]:


out_map = []
devsLeft = developers.copy()
mansLeft = managers.copy()
score = 0
for r in range(H):
    if (r % 10 == 0):
        print('r: ' + str(r))
    out_map.append([])
    for c in range(W):
        if (c % 100 == 0):
            print('c: ' + str(c))
            pass
        upperNei = None
        leftNei = None
        if (r >= 1 and office_map[r - 1, c] != 0):
            upperNei = out_map[r - 1][c]
        if (c >= 1 and office_map[r, c - 1] != 0):
            leftNei = out_map[r][c - 1]
        if office_map[r, c] == 1:  # Dev
            dev = getBestDev(devsLeft, upperNei, leftNei)
            if dev != None:
                dev.coord = [r, c]
                out_map[r].append(dev)
                score += dev.getScoreWith(upperNei) + dev.getScoreWith(leftNei)
            else:
                out_map[r].append('X')
        if office_map[r, c] == 2:  # Manager
            man = getBestMan(mansLeft, upperNei, leftNei)
            if man != None:
                man.coord = [r, c]
                out_map[r].append(man)
                score += man.getScoreWith(upperNei) + man.getScoreWith(leftNei)
            else:
                out_map[r].append('X')
        if office_map[r, c] == 0:
            out_map[r].append('X')

print(score)
# In[ ]:





# In[ ]:





# In[180]:



filename = 'out_'+l+'.txt'
with open(filename, 'a') as out:
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
    print(to_print, file = out)


# In[ ]:




