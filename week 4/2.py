import hashlib, random, time, copy, os
import base58check
from Crypto.Hash import RIPEMD160

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
	0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

def generator_private_key():
    while True:
        random_str = str(os.urandom(32)) + str(random.random()) + str(time.time())

        sha256_bytes = hashlib.sha256(random_str.encode()).hexdigest()

        if int(sha256_bytes, 16) < P:
            return sha256_bytes

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

        # bit가 1일 경우 실행
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

# 1. 희망하는 주소의 문자열을 입력 받습니다.
prefix = input('희망하는 주소의 문자열?')

while True:
    # 개인키를 생성합니다.
    private_key = generator_private_key()

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

    # 10. 생성된 주소가 사용자가 원하는 문자열로 시작하는지 확인합니다.
    if address.decode()[1:len(prefix)+1] == prefix:
        print("개인키:", private_key)
        print("공개키:", Q)
        print("주소:", address.decode())

        break
