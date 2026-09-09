from cryptography.fernet import Fernet


key = Fernet.generate_key()
cypher_suite = Fernet(key)

user_text = input("Enter a string to encrypt: ")
encoded_text = cypher_suite.encrypt(user_text.encode("utf-8"))
decoded_text = cypher_suite.decrypt(encoded_text).decode("utf-8")

print("Encoded text:", encoded_text)
print("Decoded text:", decoded_text)
