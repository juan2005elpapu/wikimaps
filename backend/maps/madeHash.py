import math
import random
import string

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

if __name__ == "__main__":
    userPasswordHash = MadeHash(initialCapacity=10)
    
    print("Generando 10 usuarios aleatorios y sus contraseñas...")
    users = []
    for i in range(10):
        username = f"user_{i+1}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        users.append((username, password))
        userPasswordHash.insert(username, password)
        index = userPasswordHash._calculateIndex(username)
        print(f"Insertado: {username} -> {password} (Inicialmente Bucket: {index})")
    
    userPasswordHash.displayContents()
    
    print("\n" + "=" * 50)
    print("EXPLICACIÓN DE LA DISTRIBUCIÓN:")
    print("=" * 50)
    print("1. Los índices de los buckets van de 0 a capacidad-1 (en este caso, 0 a 9).")
    print("2. La función hash calcula el índice y se resuelven colisiones con sondeo lineal.")
    print("=" * 50)
    
    print("\nDemostrando los métodos principales:")
    randomUser = random.choice(users)[0]
    print(f"\n1. Buscando contraseña para {randomUser}")
    print(f"   Resultado: {userPasswordHash.findValue(randomUser)}")
    
    print("\n2. Buscando usuario inexistente 'noexiste'")
    print(f"   Resultado: {userPasswordHash.findValue('noexiste')}")
    
    print(f"\n3. Verificando si existe el usuario {randomUser}")
    print(f"   Resultado: {userPasswordHash.containsKey(randomUser)}")
    
    newPassword = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    print(f"\n4. Actualizando contraseña de {randomUser}")
    print(f"   Nueva contraseña: {newPassword}")
    userPasswordHash.updateValue(randomUser, newPassword)
    print(f"   Contraseña actualizada: {userPasswordHash.findValue(randomUser)}")
    
    userToRemove = users[3][0]
    print(f"\n5. Eliminando usuario {userToRemove}")
    userPasswordHash.removeEntry(userToRemove)
    print(f"   Usuario eliminado, búsqueda: {userPasswordHash.findValue(userToRemove)}")
    print(f"   Cantidad actual de entradas: {userPasswordHash.getTotalEntries()}")
    
    print("\nEstado final de la tabla hash:")
    userPasswordHash.displayContents()
