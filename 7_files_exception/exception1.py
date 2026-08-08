
#edge case /corner case
# try:
#     num1=int(input("Enter a number:"))
#     num2=int(input("Enter another number:"))
#     div1=num1/num2
#     print(div1)
# except Exception as e:
#     print('error occured:', e)


try:
    num1=int(input("Enter a number:"))
    num2=int(input("Enter another number:"))
    div1=num1/num2
    print(div1)
except ZeroDivisionError as e:
    print('zero is not allowed:', e)
except ValueError as e:
    print('invalid input:', e)


print('------------------- important code -------------------')