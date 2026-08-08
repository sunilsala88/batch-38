#txt,csv,html,exel


data='this is some import data'

# f1=open('data.txt','w')
# f1.write(data)  
# f1.close()



# f2=open('name.txt','r')
# n=f2.read()
# f2.close()


# f3=open('demo.txt','a')
# f3.write('tsla\n')
# f3.close()



stock_prices={'AAPL': 150, 'GOOG': 2800, 'MSFT': 300, 'AMZN': 3500, 'TSLA': 700}
print(stock_prices)

def get_portfolio(stock_prices:dict)->dict:
    portfolio={}
    while True:

        name=input('Enter stock name: (press q to quit) ').upper()

        if name=='Q':
            break

        price=stock_prices.get(name)

        if price is None:
            print('Stock not found. Please try again.')
        else:
            print(f'stock {name} is added to portfolio')
            portfolio.update({  name:price})
    return portfolio

portfolio=get_portfolio(stock_prices)
print('portfolio',portfolio)

def save_data(portfolio:dict)->None:
    f1=open('portfolio.txt','a')
    for stock,price in portfolio.items():
        f1.write(stock+':'+str(price)+'\n')
    f1.close()

save_data(portfolio)