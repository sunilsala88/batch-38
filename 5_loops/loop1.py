
# #type 1
# l1=[33,44,55,66,77]
# for i in l1:
#     print(i)

# #type 2
# for i in range(10):
#     print('hello')

# #type 3
# for i in range(len(l1)):
#     print(l1[i])

#typ3 4

#not type 4
stock_prices={'AAPL': 200, 'GOOG': 300, 'MSFT': 400}
# for i in stock_prices:
#     print(i, stock_prices.get(i))

print('-------------------')
print(list(stock_prices.keys()))
print(list(stock_prices.values()))
print(list(stock_prices.items()))

#type 4
total=0
for i,j in stock_prices.items():
    print(i,j)
    total=total+j
    print(total)

print('Total:', total)

