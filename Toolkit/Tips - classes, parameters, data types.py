# Data types

number: int = 10
decimal: float = 2.5
text: str = 'hello'

Active: bool = False

names: list = ['bob', 'maria', 'luigi']
cordinate: tuple = (1.5, 2.5)
unique: set = {1,2,3,4,5} #quase o mesmo que lsita, só não pode ter duplicatas
data: dict = {'name': 'bob', 'age': 20} # dicionários


#type anotations

name: str = 'Bob'
age: int = 'Eleven'

print(age)


from datetime import datetime

print('this is the current time:')
print(datetime.now())

print(f'this is the current time ({datetime.now()})')

#Parameters

def greet(name: str) -> None:
    print(f'hello ({name})')
    
greet('alex')

#Classes

class Car: 
    def __init__(self, model: str, colour: str, horsepower: int):
        self.colour = colour
        self.horsepower = horsepower
        self.model = model
    
    def drive(self):
        print(f'{self.colour} is driving!')        
        
    def get_info(self):
        print(f'{self.model} with {self.horsepower}')
        

volvo: Car = Car('XC60','red',200)
print(volvo.colour)
    
bmw: Car = Car('X5','blue', 340)
print(volvo.horsepower)


print(volvo.get_info())
    