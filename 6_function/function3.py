
a=30

def fun1():
    global a
    print(temp)
    a=20
    print(a)
    b=20

temp='some value'
fun1()

print(a)

def average(lst):
    total=0
    for i in lst:
        total+=i
    avg=total/len(lst)
    return avg

list=[10,20,30,40,50]
avg=average(list)
print(avg)