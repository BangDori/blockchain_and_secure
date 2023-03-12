import os, random, time
import copy, hashlib

ZERO_COEF = 0x7
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
	0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

# 개인키 생성
def generator_private_key():
    while True:
        # 무작위 문자열 생성
        random_str = str(os.urandom(32)) + str(random.random()) + str(time.time())

        # 256 비트의 난수 생성
        sha256_bytes = hashlib.sha256(random_str.encode()).hexdigest()

        # 비교
        if int(sha256_bytes, 16) < P:
            return sha256_bytes

# Extended Euclidian 알고리즘을 이용하여 곱셈의 역원을 계산
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

# 곱하기 연산
def double_and_add(G, x):
    point = copy.deepcopy(G)
    binary = format(x, 'b')

    for bit in binary[1: ]:
        point = addition(point, point)

        # bit가 1일 경우 실행
        if bit == '1':
            point = addition(point, G)

    return point

# 더하기 연산
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

private_key = generator_private_key()
public_key = double_and_add(G, int(private_key, 16))

print(f"개인키(16진수): {hex(int(private_key, 16))}")
print(f"개인키(10진수): {int(private_key, 16)}")
print(f"공개키(16진수): ({hex(public_key[0])}, {hex(public_key[1])})")
print(f"공개키(10진수): {public_key}")