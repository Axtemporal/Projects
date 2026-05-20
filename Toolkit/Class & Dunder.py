# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Microwave:
    def __init__(self, brand: str, power_rating: str) -> None:
        self.brand = brand
        self.power_rating = power_rating
        self.turned_on: bool = False
        
    def turn_on(self) -> None:
        if self.turned_on:
            print(f'Microwave ({self.brand}) already turned on')
        else:
            self.turned_on = True
            print(f'Microwave ({self.brand}) now is turned on')
            
    def turn_off(self) -> None:
        if self.turned_on:
            self.turned_on = False
            print(f'Microwave ({self.brand}) is now turned off')
        else:
            self.turned_on = True
            print(f'Microwave ({self.brand})is alerady turned on')   
    
    def run(self, seconds: int) -> None:
        if self.turned_on:
            print(f'Running ({self.brand}) now for ({seconds}) seconds') 
        else: 
            print(f'A mystical force whispers: "Turn on your microwave first..."')
            
    def __add__ (self, other):
        return print(f'{self.brand} + {other.brand}')
    
    def __mul__ (self, other):
        return print(f'{self.brand} * {other.brand}')
    
    def __repr__(self) -> str:
        return 'REPR'
        return 'f({self.brand}), class: ({self.power_rating}))'
    

smeg: Microwave = Microwave('Smeg','B')
bosch: Microwave = Microwave('Bosch', 'A')

smeg.turn_on()
smeg.turn_on()
smeg.run(30)
smeg.turn_off()
smeg.run(30)
smeg + bosch
smeg * bosch

print(smeg)

# print(smeg + bosch) não funciona posi é necessário definir uma dunder method "__add__"

#dunder methods tem "__" na frente, são funções internas do python
# __init__quando você cria o objeto com Microwave()
#__str__quando você faz print(smeg)
#__len__quando você faz len(smeg) define 
#       def __len__(self):
#           return len(self.programas)  # define o que "tamanho" significa pra esse objeto
#__add__quando você faz smeg + outro


#__eq__quando você faz smeg == outro


class Ativo:
    def __init__ (self, ticker, preço, volatilidade) -> None:
        self.ticker = ticker
        self.preço = preço
        self.volatilidade = volatilidade
    def __add__(self,other):
        #soma 2 ativos em uma carteira
        return self.preço + other.preço
    
    def __gt__(self,other):
        #compara qual ativo pe mais caro
        return self.preço > other.preço
    
petr4 = Ativo('PETR4', 38.50, 5)
vale3 = Ativo('VALE3', 62.10, 3)

#print (petr4 < vale3)        
