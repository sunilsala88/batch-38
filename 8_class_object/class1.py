#class-> blueprint of object
#object-> instance of class
#attribute-> variable inside class
#class attribute-> variable inside class but outside method
#instance attribute-> variable inside class and inside method


class Student:
    school_name="ABC School"  #class variable
    dress_code="Blue"  #class variable

s1=Student()  #object of class Student
print(s1.school_name)  #accessing class variable using object
s2=Student()  #object of class Student
print(s2.dress_code)  #accessing class variable using object