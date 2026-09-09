#this is a simple program to encrypt and decrypt a string using the cryptography library

from cryptography.fernet import Fernet

key = Fernet.generate_key()
cypher_suite = Fernet(key)

encoded_text = cypher_suite.encrypt(b"Hello, World!")
print("Encoded text:", encoded_text)
decoded_text = cypher_suite.decrypt(encoded_text)
print("Decoded text:", decoded_text)
