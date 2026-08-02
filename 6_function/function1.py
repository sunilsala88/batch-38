


prices=[10, 20, 30, 40, 50]

returns=[10, 20, 30, 40, 50]

# total1=0
# for i in prices:
#     total1+=i
# avg=total1/len(prices)
# print("Average of prices:", avg)


# total2=0
# for i in returns:
#     total2+=i
# avg2=total2/len(returns)
# print("Average of returns:", avg2)


def average(lst):
    total=0
    for i in lst:
        total+=i
    avg=total/len(lst)
    return avg


print("Average of prices:", average(prices))
print("Average of returns:", average(returns))


str1='hello'
n=len(str1)
print(n)

def length(abc:str)->int:
    count=0
    for i in abc:
        count+=1
    return count

n1=length(str1)
print(n1)

l1=[1,2,3,4,5]

def reverse1(xyz:list)->list:
    l2=[]
    for i in range(-1,-(len(xyz)+1),-1):
        l2.append(xyz[i])
    return l2

l2=reverse1(l1)
print(l2)


def fibonacci(n:int)->list:
    fib=[0,1]
    for i in range(n-2):
        prev=fib[-1]
        prev_prev=fib[-2]
        current=prev+prev_prev
        fib.append(current)
    return fib


fl=fibonacci(20)
print(fl)


def add(num1:int,num2:int)->float:
    total=num1+num2
    return total

def main():
    num1=10
    num2=20
    result=add(num1,num2)
    print(result)


main()

#add,sub,mul div