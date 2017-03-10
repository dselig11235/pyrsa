from random import randint
from miller_rabin import is_prime
import base64

def gcd(x, y):
   """This function implements the Euclidian algorithm
   to find G.C.D. of two numbers"""

   while(y):
       x, y = y, x % y

   return x

# define lcm function
def lcm(x, y):
   """This function takes two
   integers and returns the L.C.M."""

   lcm = (x*y)//gcd(x,y)
   return lcm

def seq(i, m):
    while i<m:
        yield i
        i = i+1

def factor(n):
    factors = []
    while(n>1):
        for div in seq(2, n+1):
            if n % div == 0:
                n = n/div
                factors.append(div)
                break
    fset = set(factors)
    return [(x, factors.count(x)) for x in fset]

def euler_phi(n):
    phi = n
    for f in factor(n):
        phi = int(phi*(1 - 1.0/f[0]))
    return phi

def getParams(x, y, z):
    p = primes[x]
    q = primes[y]
    tot = lcm(p-1, q-1)
    e = primes[z]
    d = (e**(euler_phi(tot) -1)) % tot
    return {
                'p': p,
                'q': q,
                'tot': tot,
                'e': e,
                'd': d,
                'n': p*q
            }

def random_prime(bits):
    min = 6074001000 << (bits-33)
    max = (1<<bits) - 1
    while True:
        p = randint(min, max)
        if(is_prime(p)):
            return p

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

class RSAKey:
    def __init__(self, e = 0, n = 1):
        self.n = n
        self.e = e
    def encrypt(self, msg):
        return pow(strToInt(msg), self.e, self.n)
    def decrypt(self, msg):
        return intToStr(pow(msg, self.e, self.n))
    def encrypt64(self, msg):
        return base64.b64encode(intToStr(self.encrypt(msg)))
    def decrypt64(self, msg):
        return self.decrypt(strToInt(base64.b64decode(msg)))
    def tostr(self):
        return '{},{}'.format(base64.b64encode(intToStr(self.n)), base64.b64encode(intToStr(self.e)))
    def fromstr(self, str):
        (n, e) = str.split(',')
        self.n = strToInt(base64.b64decode(n))
        self.e = strToInt(base64.b64decode(e))

class RSAParams:
    def generate(self, keysize):
        e = 65537
        while True:
            p = random_prime(keysize/2)
            q = random_prime(keysize/2)
            tot = lcm(p - 1, q - 1)
            if gcd(e, tot) == 1 and (keysize/2-100 < 0 or (abs(p-q) >> (keysize/2-100)) > 1):
                self.p = p
                self.q = q
                self.n = p*q
                self.e = e
                self.d = modinv(e, tot)
                self.public = RSAKey(e, self.n)
                self.private = RSAKey(self.d, self.n)
                return (self.public, self.private)

def strToInt(msg):
    return int(msg.encode('hex'), 16)

def intToStr(msg):
    encoded = format(msg, 'x')
    l = len(encoded)
    encoded = encoded.zfill(l + l%2)
    return encoded.decode('hex')
    #return hex(msg)[2:].rstrip('L').decode('hex')


