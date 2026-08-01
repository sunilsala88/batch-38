


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

def length(n):
    count=0
    for i in str1:
        count+=1
    return count

n1=length(n)
print(n1)

l1=[1,2,3,4,5]

def reverse1(lst):
    l2=[]
    for i in range(-1,-(len(lst)+1),-1):
        l2.append(lst[i])
    return l2

l2=reverse1(l1)
print(l2)


fl=fibonacci(10)