
#keys are always unique
stock_prices={'tsla':1000,'apple':2000,'microsoft':3000,'google':4000}
stock_number={1:'tsla',2:'apple',3:'microsoft',4:'google',5:True,4:'kgoogle'}
print(stock_number)

#access
v1=stock_prices.get('apple')
print(v1)

v2=stock_prices['microsoft']
print(v2)

#add
a1=stock_prices.update({'nifty':5000})

stock_prices['banknifty']=900
print(stock_prices)



#update
a1=stock_prices.update({'google':6000})
stock_prices['tsla']=2000
print(stock_prices)

#remove
r1=stock_prices.pop('tsla')
del stock_prices['google']
print(stock_prices)

