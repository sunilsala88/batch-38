
try:
    with open(r'/Users/algo trading 2026/batc 38/7_files_exception/portfolio.txt','r') as f1:
        data=f1.read()
        print(data)

    with open('portfolio1.txt','w') as f2:
        f2.write(data)

except FileNotFoundError:
    print('file not found error')
