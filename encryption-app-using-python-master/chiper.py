#import for ceasar
import string

#import for playfair
from string import ascii_uppercase as asc
from itertools import product as d
import re

#import for raps
import random


class chiper():
    def __init__(self,txt,key):
        self.text=txt
        self.key=key
    def encrypt(self):
        pass
    def decrypt(self):
        pass

class caesar(chiper):
    lowercase=string.ascii_lowercase
    uppercase=string.ascii_uppercase
    digit=string.digits
    special="""'!@#$%^&*()_+-<>?|":{}[]\/.,;= """
    letters=lowercase + uppercase + digit + special

    def encrypt(self):
        cipher=[]

        for c in self.text:
            pos=self.letters.find(c)
            new_pos=(pos+int(self.key))%len(self.letters)  
            encrypted_char=self.letters[new_pos]
            cipher.append(encrypted_char)

        return ''.join(cipher)


    def decrypt(self):
        plain_text=[]
        for c in self.text:
            position=self.letters.find(c)
            position=(position-int(self.key))%len(self.letters)
            plain_text.append(self.letters[position])
        return ''.join(plain_text)

class playfair(chiper):
    def encrypt(self):
        t=lambda x: x.upper().replace('J','I')
        s=[]
        for _ in t(self.key+asc):
            if _ not in s and _ in asc:
                s.append(_)
        m=[s[i:i+5] for i in range(0,len(s),5)]
        enc={row[i]+row[j]:row[(i+1)%5]+row[(j+1)%5] for row in m for i,j in d(range(5),repeat=2) if i!=j}
        enc.update({col[i]+col[j]:col[(i+1)%5]+col[(j+1)%5] for col in zip(*m) for i,j in d(range(5),repeat=2) if i!=j})
        enc.update({m[i1][j1]+m[i2][j2]:m[i1][j2]+m[i2][j1] for i1,j1,i2,j2 in d(range(5),repeat=4) if i1!=i2 and j1!=j2})
        l=re.findall(r'(.)(?:(?!\1)(.))?',''.join([_ for _ in t(self.text) if _ in asc]))
        encoded=''.join(enc[a+(b if b else 'X')] for a,b in l)
        return encoded

    def decrypt(self):
        t=lambda x: x.upper().replace('J','I')
        s=[]
        for _ in t(self.key+asc):
            if _ not in s and _ in asc:
                s.append(_)
        m=[s[i:i+5] for i in range(0,len(s),5)]
        enc={row[i]+row[j]:row[(i+1)%5]+row[(j+1)%5] for row in m for i,j in d(range(5),repeat=2) if i!=j}
        enc.update({col[i]+col[j]:col[(i+1)%5]+col[(j+1)%5] for col in zip(*m) for i,j in d(range(5),repeat=2) if i!=j})
        enc.update({m[i1][j1]+m[i2][j2]:m[i1][j2]+m[i2][j1] for i1,j1,i2,j2 in d(range(5),repeat=4) if i1!=i2 and j1!=j2})
        dec = dict((v, self.key) for self.key, v in enc.items())
        f=re.findall(r'(.)(?:(?!\1)(.))?',''.join([_ for _ in t(self.text) if _ in asc]))
        decoded=''.join(dec[a+(b if b else 'X')] for a,b in f)
        return decoded

class raps(chiper):
    key_list=[]
    key_list2=[]
    def __init__(self,txt,key):
        self.text=txt
        self.key=int(key)%8
        if self.key==0:
            self.key=1
    # second_key is also a list which consist the number 'num' which is used to decrypt
    def second_key(self,value,decimal):
        num=0
        flag='false'
        d,num=0,0
        flag='false'
        while flag=='false':
            d=((59*num+value)-self.key_list[len(self.key_list)-1])-64
            if(decimal==d):
                self.key_list2.append(num)
                flag='true' 
                break
            else:
                num+=1

    #frist_key is list consist of random number
    def frist_key(self):
        min, max,=64,123
        key=int(min+(random.random()*(max-min)))
        # key=random.randint(min,max)
        self.key_list.append(key)
        return key
    # binary to decimal
    @staticmethod 
    def binaryToDecimal(binary): 
        decimal, i= 0, 0
        while(binary != 0): 
            dec = binary % 10
            decimal = decimal + dec * pow(2, i) 
            binary = binary//10
            i += 1
        return decimal 

    # used of NOT gate to encrypt the binary 
    def binary_pattern(self,list):
        for index in range(0,len(list)):
            if(index<self.key):
                if(list[index]=='0'):
                    list[index]='1'
                elif(list[index]=='1'):
                    list[index]='0'
        return list
    # convert list(multiple integer) to single integer
    @staticmethod
    def convert(list): 
        # Converting integer list to string list 
        s = [str(i) for i in list] 
        # Join list items using join() 
        res = int("".join(s)) 
        return(res)
    # check whether if the binary is not 8 digits then add 0 from front to make 8 digits binary number
    @staticmethod
    def digitcount(bin_value):
        list=[]
        if(len(str(bin_value))<8):
            i=0
            while(len(str(bin_value))+i)!=8:
                list.append('0')
                i+=1
        for i in bin_value:
            if(i=='1' or i =='0'):
                list.append(i)
        return list
    def encrypt (self):
        chiper_text=[]
        for char in self.text:
            list=[]
            #converting ascii(decimal) to binary
            bin_value=bin(ord(char))
            bin_value=bin_value[2:]
            list=self.digitcount(bin_value)
            list=self.binary_pattern(list)
            b_num=self.convert(list)
            decimal=self.binaryToDecimal(b_num)
            k=self.frist_key()
            ascii=((decimal+k)%59)+64
            self.second_key(ascii,decimal)
            chiper_text.append(chr(ascii))
        chiper=''.join(chiper_text) 
        
        return chiper,self.key_list,self.key_list2

    # 1st decryption using the not gate and call 2nd decryption
    def decrypt(self,key_list,key_list2):
        plain_text=[]
        pointer=0
        for char in self.text:
            list=[]
            ascii_value=ord(char)
            final_ascii=((59*key_list2[pointer]+ascii_value)-key_list[pointer])-64
            bin_value=bin(final_ascii)
            bin_value=bin_value[2:]
            list=self.digitcount(bin_value)
            list=self.binary_pattern(list)
            b_num=self.convert(list)
            ascii=self.binaryToDecimal(b_num)
            plain_text.append(chr(ascii))
            pointer+=1
        message=''.join(plain_text)
        return message