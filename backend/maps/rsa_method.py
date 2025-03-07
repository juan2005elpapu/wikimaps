from fifoQueue import FifoQueue

class Encrypter: 

    def __init__(self, password): 
        self.modulus = 3233
        self.publicExponent = 65537
        self.privateExponent = 2753  
        self.password = password

    def RSA_Encrypt(self): 
        listOfNum = FifoQueue()
        for letter in self.password: 
            letter = int.from_bytes(letter.encode(), 'big')
            listOfNum.enqueue(letter)

        final_Password = ''
        for Nums in listOfNum: 
            final_Num = (Nums**self.publicExponent) % self.modulus
            final_Password += str(hex(final_Num))+' '
        return final_Password.rstrip()
    
    def RSA_Decrypt(self, encripted): 
        encrypted_nums = encripted
        encrypted_nums = encrypted_nums.split(' ')

        decrypted_message = ''
        for encrypted_num_str in encrypted_nums:
            encrypted_num = int(encrypted_num_str, 16)
            decrypted_num = (encrypted_num ** self.privateExponent) % self.modulus
            decrypted_message += chr(decrypted_num)

        return decrypted_message
    
encriptador = Encrypter('hola')
print(encriptador.RSA_Encrypt())
print(encriptador.RSA_Decrypt(encriptador.RSA_Encrypt()))
