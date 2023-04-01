import hashlib
import time

class BitcoinPOW:
    def __init__(self, message, target_bits):
        self.message = message
        self.target_bits = target_bits

    def _hash(self, extra_nonce, nonce):
        data = self.message.encode() + extra_nonce.to_bytes(4, byteorder='big') + nonce.to_bytes(4, byteorder='big')
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()

    def find_nonce(self):
        target = int(self.target_bits, 16)
        extra_nonce = int(time.time())
        nonce = 0
        start_time = time.time()

        while True:
            hash_value = int.from_bytes(self._hash(extra_nonce, nonce), byteorder='big')

            if hash_value < target:
                print(f"Target: 0x{self.target_bits:064x}")
                print(f"메시지: {self.message}, Extra nonce: {extra_nonce}, nonce: {nonce}")
                print(f"실행 시간: {time.time() - start_time:.9f}초")
                print(f"Hash result: {hash_value:064x}")
                return nonce

            nonce += 1

            if nonce == 2**32:
                nonce = 0
                extra_nonce += 1

if __name__ == '__main__':
    # 학번=123456
    message = input('메시지의 내용? ')
    # 1e00ffff
    target_bits = input('Target bits? ')
    pow_solver = BitcoinPOW(message, target_bits)
    pow_solver.find_nonce()