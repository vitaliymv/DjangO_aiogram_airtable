import random
import string
from cryptography.fernet import Fernet
from django_aiogram_airtable.settings import CIPHER_KEY, table


def check_field(field):
    if field:
        return field
    else:
        return " "


def generate_password():
    password = ""
    for _ in range(1, 10):
        password += random.choice(string.ascii_letters + string.digits)
    return password


def encrypt(password):
    cipher = Fernet(CIPHER_KEY)
    encrypted_pass = cipher.encrypt(str.encode(password))
    return encrypted_pass.decode()


def decrypt(enc_pass):
    cipher = Fernet(CIPHER_KEY)
    decrypt_pass = cipher.decrypt(str.encode(enc_pass))
    return decrypt_pass.decode()


def check_exist(field):
    for records in table.iterate(page_size=100, max_records=1000):
        for record in records:
            if record.get("fields").get("username") == field:
                return True
