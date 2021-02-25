import os

score = 1
l = 'e'
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


print(filename)
