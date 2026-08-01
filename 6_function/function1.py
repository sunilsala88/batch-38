


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