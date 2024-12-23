from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QVBoxLayout, QWidget
import sys
import random


# Helper functions for RSA
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Расширенный алгоритм Евклида для нахождения обратного элемента
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


# Модульное возведение в степень
def modexp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def generate_keypair():
    # For simplicity, small prime numbers are chosen, but you should use larger primes in real-world scenarios
    def get_prime():
        while True:
            num = random.randint(100, 300)
            if is_prime(num):
                return num

    p = get_prime()
    q = get_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    d = modinv(e, phi)
    return (e, n), (d, n)


def encrypt(public_key, plaintext):
    e, n = public_key
    return [modexp(ord(char), e, n) for char in plaintext]


# Расшифрование
def decrypt(private_key, ciphertext):
    d, n = private_key
    return ''.join([chr(modexp(char, d, n)) for char in ciphertext])


class RSAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSA Encryption")

        # Generate RSA keys
        self.public_key, self.private_key = generate_keypair()

        self.resize(800, 600)

        # Labels
        self.public_label = QLabel(f"Public Key: {self.public_key}")
        self.private_label = QLabel(f"Private Key: {self.private_key}")

        # Text areas
        self.text_to_encrypt = QTextEdit("Enter text to encrypt")
        self.encrypted_text = QTextEdit()
        self.decrypted_text = QTextEdit()

        # Buttons
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_message)

        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_message)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.public_label)
        layout.addWidget(self.private_label)
        layout.addWidget(self.text_to_encrypt)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.encrypted_text)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.decrypted_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def encrypt_message(self):
        plaintext = self.text_to_encrypt.toPlainText()
        encrypted = encrypt(self.public_key, plaintext)
        self.encrypted_text.setText(str(encrypted))

    def decrypt_message(self):
        encrypted = eval(self.encrypted_text.toPlainText())
        decrypted = decrypt(self.private_key, encrypted)
        self.decrypted_text.setText(decrypted)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec())
