import os
from cryptography.fernet import Fernet

os.chdir('./week 1')
rfile = open('data.txt', 'r')
content = rfile.read()

key = Fernet.generate_key()
fernet = Fernet(key)

token = fernet.encrypt(content.encode())

wfile = open('encrypted.txt', 'b+w')
wfile.write(token)
wfile.close()

rfile = open('encrypted.txt', 'b+r')
result = rfile.read()
result = fernet.decrypt(result)
rfile.close()   

print(result.decode('utf-8'))