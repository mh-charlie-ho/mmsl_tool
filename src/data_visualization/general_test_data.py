#!/usr/bin/env python
import random

class Generator():
    
    def __init__(self):
        self.__dict = {}

    def Do(self, num = 100):
        self.__dict["rowid"] = [random.randint(0, num) for _ in range(num)]
        self.__dict["range"] = [random.randint(0, num) for _ in range(num)]
        self.__dict["height"] = [random.randint(0, num) for _ in range(num)]
        self.__dict["type"] = [random.randint(0, num) for _ in range(num)]
        self.__dict["intensity"] = [random.randint(0, num) for _ in range(num)]
    
    def GetDict(self):
        return self.__dict
    
if __name__ == "__main__":
    generator = Generator()
    generator.Do()
    print(generator.GetDict())