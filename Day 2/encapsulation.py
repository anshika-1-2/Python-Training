# encapsulation 

#public class

class Department:    #default is public
    def __init__(self, name):
        self.name = name  

    def display_name(self):   
        print(self.name)

dep = Department("AI")
dep.display_name()   



#private class
class Employee:
    def __init__(self, name, salary):
        self.name = name          # public method
        self.__salary = salary    # private method

    def display_salary(self):
        print("Salary:", self.__salary)

emp = Employee("Anshi", 10000)
print(emp.name)          
emp.display_salary()        



#protected class
class BankAccount:
    def __init__(self):
        self.balance = 10000

    def _show_balance(self):              # _ declares protected method
        print(f"Balance: ₹{self.balance}")  

    def __update_balance(self, amount):
        self.balance += amount             # Private 

    def deposit(self, amount):
        if amount > 0:
            self.__update_balance(amount)  
            self._show_balance()           # calling protected method
        else:
            print("Insufficient")
            
account = BankAccount()
account._show_balance()      
account.deposit(50)         