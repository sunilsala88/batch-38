


n=20
fib=[0,1]

for i in range(n-2):
    prev=fib[-1]
    prev_prev=fib[-2]
    current=prev+prev_prev
    fib.append(current)
print(fib)