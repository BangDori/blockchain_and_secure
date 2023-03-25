import hashlib
import base58check
import copy
from Crypto.Hash import RIPEMD160

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
	0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

def Extended_Euclidian(a, b):
    t1, t2 = a, b % a
    x, y = 0, 1

    while (t2 > 0):
        q = t1 // t2

        t = t1 - q * t2
        t1 = t2
        t2 = t

        z = x - q * y
        x = y
        y = z

    return x % a

def double_and_add(G, x):
    point = copy.deepcopy(G)
    binary = format(x, 'b')

    for bit in binary[1: ]:
        point = addition(point, point)

        if bit == '1':
            point = addition(point, G)

    return point

def addition(point1, point2):
    if point1 == (0, 0):
        return point2
    if point2 == (0, 0):
        return point1
    if (point1[0] == point2[0]) and (point1[1] != point2[1]):
        return point1
    
    x1, y1 = point1
    x2, y2 = point2

    if (point1 == point2):
        m = ((3 * x1 * x1) * Extended_Euclidian(P, (2 * y1))) % P
    else:
        m = ((y2 - y1) * Extended_Euclidian(P, (x2 - x1))) % P

    x = (m ** 2 - x1 - x2) % P
    y = (m * (x1 - x) - y1) % P

    return (x, y)

# 1. 개인키를 입력받습니다.
private_key = input("개인키 입력? ")
# private_key = '18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725'

# 공개키를 계산합니다.
Q = double_and_add(G, int(private_key, 16))

# 공개키를 압축합니다.
if Q[1] % 2 == 0:
    compressed_pubkey = b"\x02" + Q[0].to_bytes(32, byteorder="big")
else:
    compressed_pubkey = b"\x03" + Q[0].to_bytes(32, byteorder="big")

# 2. SHA-256 & 3. RIPEMD-160
pubkey_hash = RIPEMD160.new(hashlib.sha256(compressed_pubkey).digest()).digest()

# 4. 버전 바이트를 추가합니다.
address_bytes = b"\x00" + pubkey_hash

# 5. 6. SHA-256 & 7. 체크섬을 계산합니다.
checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]

# 8. 체크섬을 주소 바이트에 추가합니다.
address_bytes += checksum

# 9. Base58Check 인코딩 방식으로 주소를 생성합니다.
address = base58check.b58encode(address_bytes)

# 생성된 주소를 출력합니다.
print("공개키 hash =", pubkey_hash.hex())
print("비트코인 주소 =", address.decode())