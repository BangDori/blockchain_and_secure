import time
import struct
import hashlib

def pow(msg, bits):
    bits = bytes.fromhex(bits)
    target = int.from_bytes(bits[1:], byteorder='big') << 8 * (bits[0] - 3)

    start = time.time()

    ext_nonce = int(time.time())
    nonce = 0

    data = msg.encode('utf-8') + struct.pack('<I', ext_nonce) + struct.pack('<I', nonce)
    data_hash = hashlib.sha256(hashlib.sha256(data).digest()).digest()

    while int.from_bytes(data_hash, byteorder='big') > target:
        nonce += 1

        if nonce >= 2**32:
            ext_nonce += 1
            nonce = 0

        data = msg.encode('utf-8') + struct.pack('<I', ext_nonce) + struct.pack('<I', nonce)
        data_hash = hashlib.sha256(hashlib.sha256(data).digest()).digest()

    end = time.time()
    execution_time = end-start

    print(f"Target: 0x{format(target, 'x').zfill(64)}")
    print(f'메시지: {msg}, Extra nonce: {ext_nonce}, nonce: {nonce}')
    print(f'실행 시간: {execution_time}초')
    print(f'Hash result: 0x{data_hash.hex()}')

if __name__ == '__main__':
    msg = input('메시지의 내용? ')
    bits = input('Target bits? ')

    pow(msg, bits)