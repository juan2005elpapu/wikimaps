
class MadeHash:
    def __init__(self, initialCapacity=10):
        self.capacity = initialCapacity
        self.table = [None] * self.capacity
        self.itemCount = 0
        self.resizeThreshold = 0.7

    def _calculateIndex(self, keyString):
        if not isinstance(keyString, str):
            raise TypeError("Keys must be strings")
        hashValue = 0
        for character in keyString:
            hashValue = (hashValue * 31 + ord(character)) % self.capacity
        return hashValue

    def _expandCapacity(self, newCapacity):
        oldTable = self.table
        self.capacity = newCapacity
        self.table = [None] * self.capacity
        self.itemCount = 0
        for entry in oldTable:
            if entry is not None:
                self.insert(entry[0], entry[1])

    def insert(self, keyString, valueString):
        if not isinstance(keyString, str) or not isinstance(valueString, str):
            raise TypeError("Both keys and values must be strings")
        if self.itemCount / self.capacity > self.resizeThreshold:
            self._expandCapacity(self.capacity * 2)
        index = self._calculateIndex(keyString)
        start_index = index
        while self.table[index] is not None:
            if self.table[index][0] == keyString:
                self.table[index] = (keyString, valueString)
                return
            index = (index + 1) % self.capacity
            if index == start_index:
                # Esto no debería ocurrir ya que se expande la tabla
                raise Exception("Hash table is full")
        self.table[index] = (keyString, valueString)
        self.itemCount += 1

    def findValue(self, keyString):
        if not isinstance(keyString, str):
            raise TypeError("Keys must be strings")
        index = self._calculateIndex(keyString)
        start_index = index
        while self.table[index] is not None:
            if self.table[index][0] == keyString:
                return self.table[index][1]
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return None

    def removeEntry(self, keyString):
        if not isinstance(keyString, str):
            raise TypeError("Keys must be strings")
        index = self._calculateIndex(keyString)
        start_index = index
        while self.table[index] is not None:
            if self.table[index][0] == keyString:
                self.table[index] = None
                self.itemCount -= 1
                # Reubicar entradas de la misma cluster
                next_index = (index + 1) % self.capacity
                while self.table[next_index] is not None:
                    rehashKey, rehashVal = self.table[next_index]
                    self.table[next_index] = None
                    self.itemCount -= 1
                    self.insert(rehashKey, rehashVal)
                    next_index = (next_index + 1) % self.capacity
                return True
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return False

    def updateValue(self, keyString, newValueString):
        if not isinstance(keyString, str) or not isinstance(newValueString, str):
            raise TypeError("Both keys and values must be strings")
        index = self._calculateIndex(keyString)
        start_index = index
        while self.table[index] is not None:
            if self.table[index][0] == keyString:
                self.table[index] = (keyString, newValueString)
                return True
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return False

    def containsKey(self, keyString):
        return self.findValue(keyString) is not None

    def getTotalEntries(self):
        return self.itemCount

    def displayContents(self):
        print(f"\nHash Table Contents (Total Entries: {self.itemCount} | Capacity: {self.capacity}):")
        print("-" * 50)
        for i in range(self.capacity):
            if self.table[i] is not None:
                print(f"Bucket {i}: {self.table[i]}")
            else:
                print(f"Bucket {i}: Empty")
        loadFactor = self.itemCount/self.capacity
        print("-" * 50)
        print(f"Factor de carga: {loadFactor:.2f}")
