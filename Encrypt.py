from cryptography.fernet import Fernet

class Encrypt:
    def encrypt(self, string: str) -> bytes:
        """Encrypt the provided string."""
        try:
            with open("secret.key", "rb") as key_file:
                key = key_file.read()

            cipher = Fernet(key)
            encrypted_string = cipher.encrypt(string.encode())
            return encrypted_string
        except Exception as e:
            print(f"Error during encryption: {e}")
            return None 

    def decrypt(self, string: bytes) -> str:
        """Decrypt the provided encrypted string."""
        try:
            with open("secret.key", "rb") as key_file:
                key = key_file.read()

            cipher = Fernet(key)
            decrypted_string = cipher.decrypt(string).decode()  
            return decrypted_string
        except Exception as e:
            print(f"Error during decryption: {e}")
            return None  
