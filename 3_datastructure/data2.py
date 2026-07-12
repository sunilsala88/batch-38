

l1=[33,44,55,66,55,66]
print(l1)
#add
l1.append(100)
l1.insert(1,200)
print(l1)

#index and slice (access)
print(l1[0])
print(l1[-2:])

#remove
l1.remove(66)
print(l1)
l1.pop(-1)
print(l1)


#update
l1[-1]=106
print(l1)


#index
print(l1.index(55))
print(l1)


#old way of removing element
del l1[1]
print(l1)