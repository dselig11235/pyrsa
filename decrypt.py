#!/usr/bin/python

from pyrsa import RSAKey

from sys import argv
(keyfile, msg) = argv[1:]

key = RSAKey()
with open(keyfile, 'r') as f:
    key.fromstr(f.read().strip())

print key.decrypt64(msg)
