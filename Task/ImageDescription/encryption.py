from cryptography.fernet import Fernet
import os


def generate_key():
    return Fernet.generate_key()


def encrypt_image(image_path):
    key = generate_key()
    cipher_suite = Fernet(key)

    with open(image_path, 'rb') as file:
        image_data = file.read()

    encrypted_data = cipher_suite.encrypt(image_data)
    encrypted_path = image_path.replace('original', 'encrypted') + '.enc'

    with open(encrypted_path, 'wb') as file:
        file.write(encrypted_data)

    return encrypted_path, key.decode()


def decrypt_image(encrypted_path, key):
    cipher_suite = Fernet(key.encode())

    with open(encrypted_path, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data)
    decrypted_path = encrypted_path.replace('encrypted', 'decrypted').replace('.enc', '')

    with open(decrypted_path, 'wb') as file:
        file.write(decrypted_data)

    return decrypted_path
