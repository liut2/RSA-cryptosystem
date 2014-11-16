#Functions that allow for implementation an RSA cryptosystem and testcode using a Voltaire quote
#By: Ben Wedin and Tao Liu

#Computes (b^e)mod n
def modExponentiate(b,e,n):
    if e==0:
        return 1
    elif e==1:
        return b%n
    elif e%2==0:
        x = modExponentiate(b,e/2,n)
        return (x**2)%n
    else:
        x = modExponentiate(b,e-1,n)
        return (b*x)%n
        
#Computes y,x,r such that gcd(n, m) = r = xn+ym using the extended Euclidean algorithm.
def extendedEuclid(n,m):
    if m%n==0:
        return 1,0,n
    else:
        x,y,r = extendedEuclid(m%n,n)
        y = y - (m/n)*x
        return y, x, r
        
#Computes multiplicative inverse of a in n, if it exists. Returns error if no inverse exists.
def multiplicativeInverse(a,n):
    x,y,r = extendedEuclid(a,n)
    if r==1:
        return x%n
    else:
        return "Error. No multiplicative inverse exists."
        
#Converts given string s into a list of integers, each of which is at most k.
def stringToIntList(s,k):
    index = 0
    intList = []
    while index<len(s):
        stringInt = ''
        for i in range(k/3):
            if index<len(s):
                conversion = ord(s[index])
                converted = str(conversion)
                
                #Adds extra zero's such that each ascii value is 3-digits
                if len(converted)==1:
                    converted = '00' + converted
                if len(converted)==2:
                    converted = '0' + converted
                stringInt = stringInt + converted
                index += 1
        intList.append(int(stringInt))
    return intList
    
#Converts given list of integers L into one string
def intListToString(L):
    list = L
    s = ''
    for item in list:
        intString = str(item)
        if len(intString)%3==1:
            intString = '00' + intString
        if len(intString)%3==2:
            intString = '0' + intString
        for i in range(len(intString)/3):
            letter = intString[3*i+0:3*i+3]
            letter = int(letter)
            letter = chr(letter)
            s = s + letter
    return s
    
#Finds gcd(n,m) using the Euclidean algorithm
def Euclid(n,m):
    if m%n==0:
        return n
    else:
        return Euclid(m%n,n)
        
#Generates and private RSA key
def keygen(p,q):
    n = p*q
    found = False
    i=3
    ePair = (p-1)*(q-1)
    while not found:
        gcd = Euclid(i, ePair)
        if gcd==1:
            found = True
        else:
            i += 2
    e = i
    d = multiplicativeInverse(e,ePair)
    public = [e,n]
    private = [d,n]
    return public, private
    
#Encrypts message m using RSA key publickey
def encrypt(m,publickey):
    list = stringToIntList(m,21)
    encryption = []
    e,n = publickey
    for item in list:
        encrypted = modExponentiate(item,e,n)
        encryption.append(encrypted)
    return encryption
    
#Decrypts message y using RSA key privatekey
def decrypt(y,privatekey):
    d,n = privatekey
    list = []
    for item in y:
        decrypted = modExponentiate(item,d,n)
        list.append(decrypted)
    return list
    
#Test code for encrypting and decrypting a message using an RSA keypair
def main():
    s= 'THE SECRET OF BEING BORING IS TO SAY EVERYTHING.'
    print 'Here is your secret message: ' , s
    public, private = keygen(5277019477592911,7502904222052693)
    y = encrypt(s,public)
    print 'Encrypting...'
    decrypted = decrypt(y, private)
    print 'Decrypting...'
    print 'Your decrypted message is: ' , intListToString(decrypted)
main()
