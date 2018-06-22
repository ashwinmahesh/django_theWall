def createHash(toHash):
    output=17456
    for i in toHash:
        output+=17*ord(i)+99*ord(i)
        output-=32*ord(toHash[3])
    return output

def compare(unhashed, hashed):
    if(createHash(unhashed)==hashed):
        return True
    return False

if(__name__=='__main__'):
    b=createHash('hello%')
    print(b)
