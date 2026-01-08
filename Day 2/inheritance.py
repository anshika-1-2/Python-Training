#types of inheritance

#single level
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):  
    def show_role(self):
        print(self.name, "is an employee")

emp = Employee("Sagar san")
print("Name:", emp.name)
emp.show_role()

#multi level
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):  
    def show_role(self):
        print(self.name, "is an employee")

class Manager(Employee):  
    def department(self, dept):
        print(self.name, "manages", dept, "department")

mng = Manager("Mayur san")
mng.show_role()
mng.department("python")


#heirarchical
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):  
    def role(self):
        print(self.name, "works as an employee")

class Intern(Person):  
    def role(self):
        print(self.name, "is an intern")

emp = Employee("Sagar san")
emp.role()

intern = Intern("Anshika san")
intern.role()