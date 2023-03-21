import os, random, time, hashlib, copy

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
e1 = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 개인키 생성
def generate_private_key():
    while True:
        # 무작위 문자열 생성
        random_str = str(os.urandom(32)) + str(random.random()) + str(time.time())

        # 256 비트의 난수 생성
        sha256_bytes = hashlib.sha256(random_str.encode()).hexdigest()

        # 비교
        if int(sha256_bytes, 16) < p:
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
        m = ((3 * x1 * x1) * Extended_Euclidian(p, (2 * y1))) % p
    else:
        m = ((y2 - y1) * Extended_Euclidian(p, (x2 - x1))) % p

    x = (m ** 2 - x1 - x2) % p
    y = (m * (x1 - x) - y1) % p

    return (x, y)

def sign(M, d):
    k = 0

    # 랜덤 값 k 생성
    while k == 0:
        k = int.from_bytes(os.urandom(32) + str(random.random()).encode() + str(time.time()).encode(), byteorder="big") % q

    R = double_and_add(e1, k)
    r = R[0] % q

    # 해시한 값을 정수로 변환
    h = int(hashlib.sha256(M.encode()).hexdigest(), 16)
    s = (Extended_Euclidian(q, k) * (h + int(d, 16) * r)) % q

    return (r, s)

def verify(M, S1, S2, e2):
    # r, s가 q사이의 값인지 체크
    if (S1 <= 0) or (S1 >= q) or (S2 <= 0) or (S2 >= q):
        return False

    h = int.from_bytes(hashlib.sha256(M.encode()).digest(), byteorder="big")

    # s의 역원 구하기
    w = Extended_Euclidian(q, S2) % q
    A = (h * w) 
    B = (S1 * w)

    P = addition(double_and_add(e1, A), double_and_add(e2, B))

    if P == (0, 0):
        return False
    
    # ECDSA 공개키 출력
    print("\tA = ", hex(A))
    print("\tB = ", hex(B))

    return S1 == (P[0] % q)

if __name__ == "__main__":
 d = generate_private_key() # 개인 키
 e2 = double_and_add(e1, int(d, 16)) # 공개 키
 
 M = input("메시지? ")
 S1, S2 = sign(M, d)
 print("1. Sign:")
 print("\tS1 =", hex(S1)) # 서명 데이터 값 S1
 print("\tS2 =", hex(S2)) # 서명 데이터 값 S2
 
 print("2. 정확한 서명을 입력할 경우:")
 if verify(M, S1, S2, e2) == True:
    print("검증 성공")
 else:
    print("검증 실패")
 
 print("3. 잘못된 서명을 입력할 경우:")
 if verify(M, S1-1, S2-1, e2) == True:
    print("검증 성공")
 else:
    print("검증 실패")