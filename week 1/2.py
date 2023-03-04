from string import ascii_uppercase

alphabet = ascii_uppercase
alphabet_list = {}
for idx, alpha in enumerate(ascii_uppercase):
    alphabet_list[alpha] = idx

plain_text = input('평문 입력: ')
plain_text = plain_text.replace(" ", "").upper()

vigenere = input('Vigenere 암호? ').upper()
vigenere_cipher_text = list(plain_text)
for i in range(len(plain_text)):
    vigenere_cipher_text[i] = alphabet[(alphabet_list[plain_text[i]] + alphabet_list[vigenere[i % len(vigenere)]]) % 26]
print("* 암호문:", ''.join(map(str, vigenere_cipher_text)))

vigenere_decrypt_text = vigenere_cipher_text
for i in range(len(vigenere_cipher_text)):
    vigenere_decrypt_text[i] = alphabet[(alphabet_list[vigenere_cipher_text[i]] - alphabet_list[vigenere[i % len(vigenere)]]) % 26]
print("* 평문:", ''.join(map(str, vigenere_decrypt_text)))

auto_key = int(input('자동 키 암호? '))
auto_key_cipher_text = list(plain_text)
for i in range(len(plain_text)):
    if i == 0:
        auto_key_cipher_text[i] = alphabet[(alphabet_list[plain_text[i]] + auto_key) % 26]
    else:
        auto_key_cipher_text[i] = alphabet[(alphabet_list[plain_text[i]] + alphabet_list[plain_text[i-1]]) % 26]
print("* 암호문:", ''.join(map(str, auto_key_cipher_text)))

auto_key_decrypt_text = list(auto_key_cipher_text)
for i in range(len(auto_key_cipher_text)):
    if i == 0:
        auto_key_decrypt_text[i] = alphabet[(alphabet_list[auto_key_cipher_text[i]] - auto_key) % 26]
    else:
        auto_key_decrypt_text[i] = alphabet[(alphabet_list[auto_key_cipher_text[i]] - alphabet_list[auto_key_decrypt_text[i-1]]) % 26]
print("* 평문:", ''.join(map(str, auto_key_decrypt_text)))