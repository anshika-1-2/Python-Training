#classes and objects
class Dog:
    species = "Canines"  

    def __init__(self, name, age):
        self.name = name  
        self.age = age  

dog1 = Dog("Rockie", 6)  
dog2 = Dog("Bo", 3)  

print(dog1.name, dog1.age, dog1.species)  
print(dog2.name, dog2.age, dog2.species)  
print(Dog.species)  