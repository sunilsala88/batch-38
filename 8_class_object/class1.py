#class-> blueprint of object
#object-> instance of class
#attribute-> variable inside class
#class attribute-> variable inside class but outside method
#instance attribute-> variable inside class and inside method
#method-> function inside class


#object oreiented programming->we can create our own data type using class and object
class Student:
    school_name="ABC School"  #class variable
    dress_code="Blue"  #class variable

    def __init__(self,name,email,r):
        self.name=name
        self.email=email
        self.roll_no=r

    def get_student_details(self):
        print(f"student name is {self.name} and email is {self.email} and roll no is {self.roll_no}")

s1=Student('sam','sam@gmail.com',50)  #object of class Student
print(s1.school_name)  #accessing class variable using object
print(s1.name)
s2=Student('matt','matt@gmail.com',60)  #object of class Student
print(s2.dress_code)  #accessing class variable using object
print(s2.name)

s1.get_student_details()  #accessing method using object
s2.get_student_details()  #accessing method using object



l1=[22,33,44,55]


print(type(l1))
print(type(s1))



s1={3,4,5}
s2=set([1,2,4])
print(type(s1))
print(type(s2))

#structural programming-> we use built in data type like list,dict,set,tuple to store data and we use function to perform operation on data
student_info={'school_name': 'ABC School', 
              'dress_code': 'Blue', 'students': 
              [{'name': 'sam', 'email':'sam@gmail.com', 'roll_no': 50}, 
               {'name': 'matt', 'email':'matt@gmail.com', 'roll_no': 60},
                {}
               ]}