#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np


# In[25]:


filenames = ['a_example.txt', 'b_lovely_landscapes.txt','c_memorable_moments.txt','d_pet_pictures.txt','e_shiny_selfies.txt']

k = 1

f = open(filenames[k])


# In[26]:


class Image():
    
    def __init__(self, typo, tags,ID):
        self.typo = typo
        self.tags = tags
        self.ID=ID
        
    def update_score(self, score_dict):
        score = 0
        self.dict_score = {}
        for t in self.tags:
            self.dict_score[t] = score_dict[t]
            score += score_dict[t]
        self.score = score
        
    def get_score(self, len_weigth, tags_score_weigth):
        return (len_weigth*len(self.tags) + tags_score_weigth*self.score)

class Slide():
    
    def __init__(self, images):
        self.tags = []
        if len(images) == 1:
            self.tags = images[0].tags
            self.score = images[0].score
        else:
            for im in images:
                for t in im.tags:
                    if t not in self.tags:
                        self.tags.append(t)
            self.score = 0
            for t in self.tags:
                if t in list(images[0].dict_score.keys()):
                    self.score += images[0].dict_score[t]
                if t in list(images[1].dict_score.keys()):
                    self.score += images[1].dict_score[t]
        self.images = images
        
    
def score_intra_slides(slide1, slide2):
    same = []
    just_first = []
    just_second = []
    tags1 = slide1.tags.copy()
    tags2 = slide2.tags.copy()
    for t in tags1:
        if t in tags2:
            same.append(t)
            tags1.remove(t)
            tags2.remove(t)
        else:
            just_first.append(t)
    n_same = len(same)
    n_first = len(just_first)
    n_second = len(tags2)
    
    return min(n_same, n_first, n_second)

def score_intra_images(im1, im2):
    tags = []
    for im in [im1,im2]:
        for t in im.tags:
            if t not in tags:
                tags.append(t)
    score = 0
    for t in tags:
        if t in list(im1.dict_score.keys()):
            score += im1.dict_score[t]
        if t in list(im2.dict_score.keys()):
            score += im2.dict_score[t]
    return score


# In[ ]:


images = []

tags_occurences = {}
tags_score = {}

n_photos = int(f.readline())
for i in range(n_photos):
    line = f.readline()
    line = line[:-1]
    parts = line.split(" ")
    typo = parts[0]
    n_tags = int(parts[1])
    tags = parts[2:]
    for t in tags:
        if t in list(tags_occurences.keys()):
            tags_occurences[t] = tags_occurences[t] + 1
        else:
            tags_occurences[t] = 1
    images.append(Image(typo, tags,i))
for key in list(tags_occurences.keys()):
    tags_score[key] = tags_occurences[key]/n_photos


# In[ ]:





# In[ ]:


for i in range(len(images)):
    images[i].update_score(tags_score)


# In[ ]:


s1 = Slide([images[0], images[1]])
s2 = Slide([images[3]])


# In[ ]:


len(images)
images[1].typo


# In[ ]:


slides = []
print(k)
actual_images = images.copy()
for im in actual_images:
    best_score = 0
    best_image = None
    if im.typo == 'V':
        for im2 in actual_images:
            if im2.typo is 'V' and im2 is not im:
                score = score_intra_images(im, im2)
                if score > best_score:
                    best_score = score
                    best_image = im2
        actual_images.remove(im)
        actual_images.remove(best_image)
        slides.append(Slide([im,best_image]))
for im in actual_images:
    slides.append(Slide([im]))


# In[ ]:


temp = slides.copy()
scores = np.array([sl.score for sl in temp])
best = temp[scores.argmax()]        
sorted(temp, key=lambda x: tuple(scores))

slideshow = [best]
temp.remove(best)
for sl in temp:
    left = score_intra_slides(slideshow[0], sl)
    right = score_intra_slides(slideshow[-1], sl)
    if left >= right:
        slideshow.insert(0, sl)
    else:
        slideshow.append(sl)


# In[ ]:


filename = 'out'+str(k)+'.txt'
with open(filename, 'a') as out:
    to_print = ''
    to_print += str(len(slideshow))+'\n'
    for sl in slideshow:
        if len(sl.images) == 1:
            to_print += str(sl.images[0].ID)+'\n'
        else:
            for i in range(len(sl.images)):
                to_print += str(sl.images[i].ID)
                if i != len(sl.images)-1:
                    to_print += ' '
                else:
                    to_print += '\n'
    to_print = to_print[:-1]
    print(to_print, file = out)


# In[ ]:





# In[ ]:





# In[191]:


print(to_print)


# In[ ]:




