


#palindrome
#

def is_odd(num:int)->bool:
    if num%2==0:
        return False
    else:
        return True


def is_even(num:int)->bool:
    if num%2==0:
        return True
    else:
        return False

num=11
print(is_odd(num))
print(is_even(num))


def reverse(string1:str)->str:
    rev_str=''
    for i in string1:
        rev_str=i+rev_str
    return rev_str


def is_palindrome(string1:str)->bool:
    rev_str=reverse(string1)
    if string1==rev_str:
        return True
    else:
        return False

print(is_palindrome('madam'))
    