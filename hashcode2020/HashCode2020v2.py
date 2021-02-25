#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np


# In[19]:


filenames = ['data/a_example.txt', 'data/b_read_on.txt','data/c_incunabula.txt','data/d_tough_choices.txt','data/e_so_many_books.txt']

k = 2

f = open(filenames[k])


# In[20]:


#Define objects involved
class Library():

    def __init__(self, index, signup_time, scannable__books_per_day, books_num, score = 1):
        self.index = index
        self.signup_time = signup_time
        self.scannable__books_per_day = scannable__books_per_day
        self.books_num = books_num
        self.books = []
        self.books_to_be_scanned = []
        self.base_score = 0 - self.signup_time + self.scannable__books_per_day 
        self.score =self.base_score # qui aggiungi parte variabile
    def addBook(self, book):
        self.books.append(book)
        self.books_to_be_scanned.append(book)
    def update_score(self,variable_part):
        self.score = self.base_score + variable_part
    def normalize_scannable_books_per_day(self, ma, mi):
        self.scannable__books_per_day = (self.scannable__books_per_day - mi)/(ma-mi)
    def normalize_sign_up_time(self, ma, mi):
        self.signup_time = (self.signup_time- mi)/(ma-mi)
    def update_base_score(self):
        self.base_score = 0 - self.signup_time + self.scannable__books_per_day 
        
class Book:
    
    def __init__(self, index, score):
        self.index = index
        self.score = score
        self.scanned = 1
        # self.num_lib_signed_up_with_this = 0
        self.occorrenze_totale=0
    def updateOccorrenze_totale(self):
        self.occorrenze_totale +=1


# In[21]:


def choose_library(remaining_lib ,book_list):
    """
    remaining_lib [Library]
    """
    score_list = []
    for lib in remaining_lib:
        score = compute_lib_score(lib, book_list)
        score_list.append(score)
    lib_to_return = remaining_lib[score_list.index(max(score_list))]
    remaining_lib.remove(lib_to_return)
    return  lib_to_return


def compute_lib_score(lib, book_list):
    variable_part = 0
    for book in lib.books:
        variable_part += (book.score * (1 - book_list[book])) * (1/book.occorrenze_totale)
    score = lib.base_score + variable_part
    return score
    


# In[22]:


#Parse input file
print('Reading first line')
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


line = f.readline()
print('Reading books:'+str(B))
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
        index_to_book[int(line2[j])].updateOccorrenze_totale()
    ALL_LIBS.append(temp_lib)


# In[ ]:


from operator import attrgetter

lista = [Book(1,2),Book(2,2)]
bb = max(lista, key=attrgetter('score'))

def chooseLibrary(libraries_still_to_sign):
    chosenLib = max(libraries_still_to_sign, key=attrgetter('score'))
    libraries_still_to_sign.remove(chosenLib)
    print(chosenLib.signup_time)
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
        # library_signing_up = chooseLibrary(libraries_to_be_signed)
        library_signing_up = choose_library(libraries_to_be_signed, ALL_BOOKS)
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

for lib in libraries_ready:
    if books_scanned_per_library[lib] == 0:
        libraries_ready.remove(lib)

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





# In[2]:





# In[ ]:




