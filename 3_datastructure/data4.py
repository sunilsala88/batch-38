
#tuple->immutable
t=(10,20,30,40,50)
print(t)

#set->unique
s={10,20,30,40,50,10}
print(s)

s.add(100)
print(s)

s.remove(20)
print(s)    



s1='nifty,banknifty,tsla,apple'
l=s1.split(',')
print(l)

l1=['nifty','banknifty','tsla','apple']
s2=','.join(l1)
print(s2)


