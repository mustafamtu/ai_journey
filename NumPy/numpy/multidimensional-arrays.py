import numpy as np

array = np.array([[['A','B','C'],['D','E','F'],['G','H','I']],
                 [['J','K','L'],['M','N','O'],['P','Q','R']],
                 [['S','T','U'],['V','W','X'],['Y','Z',' ']]])

# print(array.shape)

# print(array[2][1][0]) # chain index
# print(array[2,1,0])  # multidimensional index

word = array[1,0,0] + array[1,1,2] + array[0,0,1]
print(word) 