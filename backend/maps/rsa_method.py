class Encrypter: 

    def __init__(self, password): 

        self.modulus = 2491
        self.publicExponent = 37 
        self.privateExponent = 937 
        self.password = password

    def From_String_To_RSA(self):

        listOfNum=[]
        for letter in self.password: 
            letter = int.from_bytes(letter.encode(), 'big')
            listOfNum.append(letter)
        return listOfNum
    
    def RSA_Encrypt(self): 

        listOfNum = self.From_String_To_RSA()
        final_Password = ''
        for Nums in listOfNum: 
            final_Num = (Nums**self.publicExponent) % self.modulus
            final_Password = final_Password+str(hex(final_Num))+' '
        return final_Password
    
    def RSA_dencrypt(self):

        final_Password = self.RSA_Encrypt()
        listOfHeX = final_Password.strip().split(' ')
        listOfNum = []
        listOfFinal = []
        for numsHex in listOfHeX: 
            numDec = int(str(numsHex), 16)
            final_Num = pow(numDec, self.privateExponent)
            listOfNum.append(numDec)
            listOfFinal.append(final_Num)
        print(listOfNum)
        return listOfNum


encriptador = Encrypter('hola')
print(encriptador.From_String_To_RSA())
print(encriptador.RSA_Encrypt())
print(encriptador.RSA_dencrypt())