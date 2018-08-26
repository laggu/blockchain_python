from bitcoin import *

priv = sha256('a')
pubk = privtopub(priv)
addr = pubtoaddr(pubk)




print(priv)
print(pubk)
print(addr)
print()

priv = sha256('b')
pubk = privtopub(priv)
addr = pubtoaddr(pubk)
print(priv)
print(pubk)
print(addr)
print()

priv = sha256('c')
pubk = privtopub(priv)
addr = pubtoaddr(pubk)
print(priv)
print(pubk)
print(addr)
print()

priv = sha256('d')
pubk = privtopub(priv)
addr = pubtoaddr(pubk)
print(priv)
print(pubk)
print(addr)
print()