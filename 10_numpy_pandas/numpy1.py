import numpy as np

l1=[22,33,44,55,6.6]
print(l1)
ar1=np.array(l1,dtype=int)
print(ar1)

l1=range(10,20)
print(list(l1))

np1=np.arange(10,20)
print(np1)

np2=np.zeros(10,dtype=int)
print(np2)

np3=np.ones(10,dtype=int)
print(np3)

lm=[[1,2,3],[4,5,6],[7,8,9]]
print(lm)
npm=np.array(lm,dtype=int)
print(npm)
print(npm[2,2])

np5=np.arange(50,75)
print(np5)
np5=np5.reshape(5,5)
print(np5)
print(np5[4,3])