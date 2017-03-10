#!/usr/bin/python

from pyrsa import RSAParams

from sys import argv
(keysize, publicname, privatename) = argv[1:]

p = RSAParams()
p.generate(1024)
with open(publicname, 'w') as f:
    f.write(p.public.tostr() + '\n')
with open(privatename, 'w') as f:
    f.write(p.private.tostr() + '\n')
