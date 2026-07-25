

# number=0

# while True:
#     print(number)
#     number=number+1
#     if number>100:
#         break


# for i in range(101):
#     print(i)


l1=[33,44,55,66,77]
# max=l1[0]
# for i in l1:
#     if i>max:
#         max=i
# print('Max:', max)

#type 3
max=l1[0]
for i in range(len(l1)):
    if l1[i]>max:
        max=l1[i]
print('Max:', max)


index=0
max=l1[0]
while True:
    if l1[index]>max:
        max=l1[index]
    index=index+1
    if index>=len(l1):
        break
print('Max:', max)

