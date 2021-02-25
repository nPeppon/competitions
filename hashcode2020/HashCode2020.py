#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[209]:


filenames = ['data/a_example.txt', 'data/b_read_on.txt','data/c_incunabula.txt','data/d_tough_choices.txt','data/e_so_many_books.txt']

k = 3
print('Open file')
f = open(filenames[k])


# In[210]:


#Define objects involved
class Library():

    def __init__(self, index, signup_time, scannable__books_per_day, books_num, score = 1):
        self.index = index
        self.signup_time = signup_time
        self.scannable__books_per_day = scannable__books_per_day
        self.books_num = books_num
        self.books = []
        self.books_to_be_scanned = []
        self.score = score
        
    def addBook(self, book):
        self.books.append(book)
        self.books_to_be_scanned.append(book)
        
class Book:
    
    def __init__(self, index, score):
        self.index = index
        self.score = score


# In[211]:

print('Reading first line')
#Parse input file
line = f.readline()
books_num = int(line.split(' ')[0])
B = books_num
libs_num = int(line.split(' ')[1])
L = libs_num
days_num = int(line.split(' ')[2])
D = days_num

ALL_BOOKS = {}
index_to_book = {}
ALL_LIBS = []


# In[ ]:

print('Reading books:'+str(B))
line = f.readline()
for i in range(B):
    if i%1000 == 0:
        print(i)
    temp_book = Book(i, int(line.split(' ')[i]))
    ALL_BOOKS[temp_book] = 0
    index_to_book[i] = temp_book


# In[ ]:

print('Reading Libraries: '+str(L))
for i in range(L):
    if i%1000 == 0:
        print(i)
    line1 = f.readline().split('\n')[0].split(' ')
    temp_lib = Library(i, int(line1[1]), int(line1[2]), int(line1[0]))
    line2 = f.readline().split('\n')[0].split(' ')
#     print(line2)
#     print(line1[0])
    for j in range(int(line1[0])):
#         print(j)
#         print(line2[j])
        temp_lib.addBook(index_to_book[int(line2[j])])
    ALL_LIBS.append(temp_lib)


# In[ ]:


from operator import attrgetter

lista = [Book(1,2),Book(2,2)]
bb = max(lista, key=attrgetter('score'))

def chooseLibrary(libraries_still_to_sign):
    chosenLib = max(libraries_still_to_sign, key=attrgetter('score'))
    libraries_still_to_sign.remove(chosenLib)
    # print(chosenLib.signup_time)
    return chosenLib

def scanBooks(library, all_books):
    scanning_books = []
    while len(scanning_books) < library.scannable__books_per_day and len(library.books_to_be_scanned) > 0:
        book = max(library.books_to_be_scanned, key=attrgetter('score'))
        if ALL_BOOKS[book] == 0:
            scanning_books.append(book)
            ALL_BOOKS[book] = 1
        else:
            library.books_to_be_scanned.remove(book)
    return scanning_books
    


# In[ ]:





# In[ ]:


signup_running = False
libraries_ready = []
libraries_to_be_signed = ALL_LIBS.copy()
books_scanned_per_library = {}
current_signup_process_days_remaining = 0
library_signing_up = None
for d in range(D):
    print('Day '+str(d))
    if not signup_running and len(libraries_to_be_signed) > 0:
        library_signing_up = chooseLibrary(libraries_to_be_signed)
        current_signup_process_days_remaining = library_signing_up.signup_time
        signup_running = True
    
    for lib in libraries_ready:
        if len(lib.books_to_be_scanned) > 0:
            books_scanned_per_library[lib].extend(scanBooks(lib, ALL_BOOKS))
    
    if signup_running:
        current_signup_process_days_remaining-=1
        if current_signup_process_days_remaining == 0:
            if d != D-1 :
                libraries_ready.append(library_signing_up)
                books_scanned_per_library[library_signing_up] = []
            signup_running = False
            library_signing_up = None
#     print(libraries_ready)
#     print(books_scanned_per_library)


# In[ ]:


# books_scanned_per_library


# In[ ]:


filename = 'out'+str(k)+'.txt'
with open(filename, 'a') as out:
    to_print = ''
    to_print += str(len(libraries_ready))
    for i in range(len(libraries_ready)):
        lib = libraries_ready[i]
        books_for_lib = books_scanned_per_library[lib]
        if len(books_for_lib) > 0:
            to_print += '\n' + str(lib.index) + ' ' + str(len(books_for_lib)) + '\n'
            for j in range(len(books_for_lib)):
                to_print += str(books_for_lib[j].index)
                if (j==len(books_for_lib)):
                    to_print += '\n'
                else:
                    to_print += ' '
    to_print = to_print[:-1]
    print(to_print, file = out)


# In[ ]:





# In[ ]:




