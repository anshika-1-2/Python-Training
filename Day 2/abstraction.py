#abstraction 

# bank account example

from abc import ABC, abstractmethod

class BankAccount(ABC):
    @abstractmethod
    
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

class SavingsAccount(BankAccount):
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(dep, amount):
        dep.balance += amount
        print(f"Amount deposited : {amount}, New Balance : {dep.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            print(f"Amount withdrawn : {amount}, New Balance : {self.balance}")
savings = SavingsAccount(100)
savings.deposit(5000)
savings.withdraw(500)
savings.withdraw(200)
