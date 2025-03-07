class LinkedArray:
    class ArrayNode:
        def __init__(self, value=None, next_node=None):
            self.value = value
            self.next = next_node

    def __init__(self, size):
        if size <= 0:
            raise ValueError("Size must be positive")
        self.size = size
        # Crear una cadena enlazada de nodos con valor inicial None
        self.head = LinkedArray.ArrayNode()
        current = self.head
        for _ in range(1, size):
            new_node = LinkedArray.ArrayNode()
            current.next = new_node
            current = new_node

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def set(self, index, value):
        node = self.get(index)
        node.value = value

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

class MadeHash:
    def __init__(self, initialCapacity=10):
        self.capacity = initialCapacity
        self.table = LinkedArray(initialCapacity)
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
        oldCapacity = self.capacity
        # Guardamos el contenido del arreglo antiguo
        old_entries = []
        for i in range(oldCapacity):
            cell = self.table.get(i).value
            if cell is not None:
                old_entries.append(cell)
        # Reemplazamos el arreglo por uno nuevo
        self.capacity = newCapacity
        self.table = LinkedArray(newCapacity)
        self.itemCount = 0
        for keyString, valueString in old_entries:
            self.insert(keyString, valueString)

    def insert(self, keyString, valueString):
        if not isinstance(keyString, str) or not isinstance(valueString, str):
            raise TypeError("Both keys and values must be strings")
        if self.itemCount / self.capacity > self.resizeThreshold:
            self._expandCapacity(self.capacity * 2)
        index = self._calculateIndex(keyString)
        start_index = index
        while self.table.get(index).value is not None:
            storedKey, _ = self.table.get(index).value
            if storedKey == keyString:
                self.table.set(index, (keyString, valueString))
                return
            index = (index + 1) % self.capacity
            if index == start_index:
                raise Exception("Hash table is full")
        self.table.set(index, (keyString, valueString))
        self.itemCount += 1

    def findValue(self, keyString):
        if not isinstance(keyString, str):
            raise TypeError("Keys must be strings")
        index = self._calculateIndex(keyString)
        start_index = index
        while self.table.get(index).value is not None:
            storedKey, storedValue = self.table.get(index).value
            if storedKey == keyString:
                return storedValue
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return None

    def removeEntry(self, keyString):
        if not isinstance(keyString, str):
            raise TypeError("Keys must be strings")
        index = self._calculateIndex(keyString)
        start_index = index
        while self.table.get(index).value is not None:
            storedKey, _ = self.table.get(index).value
            if storedKey == keyString:
                self.table.set(index, None)
                self.itemCount -= 1
                # Reubicar entradas en el mismo clúster
                next_index = (index + 1) % self.capacity
                while self.table.get(next_index).value is not None:
                    rehashKey, rehashVal = self.table.get(next_index).value
                    self.table.set(next_index, None)
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
        while self.table.get(index).value is not None:
            storedKey, _ = self.table.get(index).value
            if storedKey == keyString:
                self.table.set(index, (keyString, newValueString))
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
            cell = self.table.get(i).value
            if cell is not None:
                print(f"Bucket {i}: {cell}")
            else:
                print(f"Bucket {i}: Empty")
        loadFactor = self.itemCount / self.capacity
        print("-" * 50)
        print(f"Factor de carga: {loadFactor:.2f}")

if __name__ == "__main__":
    # Ejemplo de uso y prueba de MadeHash
    print("Creando MadeHash con capacidad inicial 10")
    hash_table = MadeHash(initialCapacity=10)

    print("\nInsertando 10 pares clave-valor:")
    for i in range(1, 11):
        key = f"user_{i}"
        value = f"pass_{i}"
        hash_table.insert(key, value)
        print(f"Insertado: {key} -> {value}")
    
    hash_table.displayContents()

    print("\nBuscando algunos valores:")
    print("user_5:", hash_table.findValue("user_5"))
    print("user_11 (no existe):", hash_table.findValue("user_11"))

    print("\nActualizando valor de user_3 a 'new_pass_3'")
    hash_table.updateValue("user_3", "new_pass_3")
    print("user_3:", hash_table.findValue("user_3"))
    
    print("\nEliminando user_4")
    hash_table.removeEntry("user_4")
    print("user_4:", hash_table.findValue("user_4"))
    
    print("\nContenido final de la tabla:")
    hash_table.displayContents()
