
a1=100

def func1():
    print("This is func1 in file1.py")


class Circle:
    def __init__(self,radius):
        self.radius=radius

    def get_area(self):
        return 3.14*self.radius*self.radius


if __name__=="__main__":
    print('this is file1.py')

    print('abc')