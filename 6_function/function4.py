


#argument ,parameter


def fun1(a,b):#2,3
    n=a**2 +b
    return n


def fun2(x,y): #2,3
    z=fun1(x,y) #7
    return z+y #7+3

def fun3(p,q):
    r=fun2(p,q) #10
    u=fun1(p,q) #7
    return r+u

print(fun3(2,3))

#1. Positional Arguments
def greet_user(name, age):
    print(f"Hello {name}, you are {age} years old.")

greet_user(25,"Alice")


#Default Arguments
def greet(name='User'):
    print("Hello", name)
greet()

#. Keyword Arguments