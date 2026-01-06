#Types of Polymorphism

#overloading in classes
#example 1
class MathOperations:
    def add(self, a, b, c=0):
        return a + b + c
math_op = MathOperations()
print("Sum of 2 numbers:", math_op.add(5, 10))
print("Sum of 3 numbers:", math_op.add(5, 10, 15))

#example 2
class Calculator:
    def multiply(self, a=1, b=1, *value):
        result = a * b
        for num in value:
            result *= num
        return result

calc = Calculator()
print(calc.multiply())            
print(calc.multiply(4))           
print(calc.multiply(2, 3))       
print(calc.multiply(2, 3, 4))


#overriding in classes
class Animal:
    def sound(self):
        return "Some sound"

class Dog(Animal):
    def sound(self):
        return "Bark"

class Cat(Animal):
    def sound(self):
        return "Meowwwwww"

animals = [Dog(), Cat(), Animal()]
for animal in animals:
    print(animal.sound())
