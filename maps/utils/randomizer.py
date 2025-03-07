from random import randint
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dataStructures.lifoStack import LifoStack

class Randomizer:
    def __init__(self) -> None:
        pass

    def logisticFunction(self, lamda, x):
        return lamda * x * (1 - x)

    def generateStar(self):
        r = 3.57  
        listOfNum = LifoStack()
        pop = 0.5

        for _ in range(1000):
            pop = self.logisticFunction(r, pop)

        # Generate values
        for _ in range(5000):
            listOfNum.push(pop)
            pop = self.logisticFunction(r, pop)

        random_index = randint(0, listOfNum.size() - 1)
        current = listOfNum.head
        for _ in range(random_index):
            current = current.next
        
        return current.value  # Return the randomly selected value

    def generateCode(self):
        code = ""
        for _ in range(24):
            numero = int(self.generateStar() * 10)
            code += str(numero)
        return code
    
rad = Randomizer()
print(rad.generateCode())