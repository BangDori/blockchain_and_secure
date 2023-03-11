from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import os

os.chdir('./week 2')

plain_text = input('평문 입력: ').encode()

key = Fernet.generate_key()
fernet = Fernet(key)

with open('public_key.pem', 'rb') as f:
    public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

with open('private_key.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

# A. AES를 이용한 암호화
enc_msg  = fernet.encrypt(plain_text)

# B. 공개키를 이용한 AES 키 암호화
enc_key = public_key.encrypt(
    key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()), 
        algorithm=hashes.SHA256(),
        label=None
    )
)

# C. enc_msg와 enc_key 출력
# print(f"암호화된 메시지: {enc_msg}")
# print(f"암호화된 AES 키: {enc_key}")

# D. 개인키를 이용하여 enc_key 복호화
aes_key = private_key.decrypt(
    enc_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

fernet = Fernet(aes_key)
# E. aes_key를 이용하여 enc_msg 복호화
decrypt_text = fernet.decrypt(enc_msg)

print(f"복호화된 메시지: {decrypt_text.decode('utf-8')}")