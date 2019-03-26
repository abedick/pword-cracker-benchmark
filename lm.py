# from passlib.hash import lmhash
import hashlib
# print(lmhash.hash("password"))
print(hashlib.sha1(bytes("password", 'utf-8')).hexdigest())
