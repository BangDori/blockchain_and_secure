from string import ascii_lowercase
import random

random_list = list(ascii_lowercase)
random.shuffle(random_list)
E = {}
D = {}

for idx, alpha in enumerate(ascii_lowercase):
    E[alpha] = random_list[idx]
    D[random_list[idx]] = alpha

plain_text = input('평문 입력: ')

cipher_text = list(plain_text)

for i in range(len(cipher_text)):
    if cipher_text[i].isspace():
        continue
    cipher_text[i] = E[plain_text[i]]
print('암호문:', ''.join(map(str, cipher_text)))

decrypt_text = list(cipher_text)

for i in range(len(decrypt_text)):
    if decrypt_text[i].isspace():
        continue
    decrypt_text[i] = D[cipher_text[i]]
print('복호문:', ''.join(map(str, decrypt_text)))