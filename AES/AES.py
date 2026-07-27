import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import base64


# Function to derive a key from the password using PBKDF2
def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 bytes for AES-256
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    return key


# Encrypt the input text using AES
def encrypt_text(plaintext: str, password: str):
    try:
        # Generate a random salt for each encryption
        salt = os.urandom(16)

        # Derive the AES key from the password and salt
        key = derive_key(password, salt)

        # Padding the plaintext to be a multiple of the AES block size (16 bytes)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        # Generate a random IV
        iv = os.urandom(16)

        # Set up AES in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        # Encrypt the data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Return the encrypted data, IV, and salt, all encoded in base64
        return base64.b64encode(encrypted_data), base64.b64encode(iv), base64.b64encode(salt)
    except Exception as e:
        print(f"Error during encryption: {e}")
        return None, None, None


# Decrypt the input text using AES
def decrypt_text(encrypted_text: str, password: str, iv_b64: str, salt_b64: str):
    try:
        # Decode the encrypted text, IV, and salt from base64
        encrypted_data = base64.b64decode(encrypted_text)
        iv = base64.b64decode(iv_b64)
        salt = base64.b64decode(salt_b64)

        # Derive the AES key from the password and salt
        key = derive_key(password, salt)

        # Set up AES in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        # Decrypt the data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

        # Return the decrypted text
        return decrypted_data.decode()
    except Exception as e:
        print(f"Error during decryption: {e}")
        return None


# GUI Application
class TextEncryptDecryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Encryption & Decryption")
        self.root.geometry("600x400")

        # Setup the GUI components
        self.setup_ui()

    def setup_ui(self):
        # Title label
        tk.Label(self.root, text="AES Text Encryption & Decryption", font=("Arial", 16)).pack(pady=10)

        # Password entry
        self.password_var = tk.StringVar()
        tk.Label(self.root, text="Enter Password:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.password_var, show="*", width=40).pack(padx=10, pady=5)

        # Text input field
        tk.Label(self.root, text="Enter Text to Encrypt/Decrypt:").pack(pady=5)
        self.text_input_field = tk.Text(self.root, height=5, width=50)
        self.text_input_field.pack(padx=10, pady=10)

        # Output text field
        tk.Label(self.root, text="Output (Encrypted/Decrypted Text):").pack(pady=5)
        self.output_field = tk.Text(self.root, height=5, width=50)
        self.output_field.pack(padx=10, pady=10)

        # Encrypt Button
        tk.Button(self.root, text="Encrypt Text", command=self.encrypt_text).pack(pady=10)

        # Decrypt Button
        tk.Button(self.root, text="Decrypt Text", command=self.decrypt_text).pack(pady=10)

    def encrypt_text(self):
        password = self.password_var.get()
        plaintext = self.text_input_field.get("1.0", tk.END).strip()

        if not password or not plaintext:
            messagebox.showerror("Error", "Please enter both password and text.")
            return

        encrypted_text, iv, salt = encrypt_text(plaintext, password)

        if encrypted_text:
            # Show the encrypted text in the output field
            self.output_field.delete(1.0, tk.END)
            self.output_field.insert(tk.END, f"Encrypted Text: {encrypted_text.decode()}\n")
            self.output_field.insert(tk.END, f"IV: {iv.decode()}\n")
            self.output_field.insert(tk.END, f"Salt: {salt.decode()}\n")
            messagebox.showinfo("Success", "Text encrypted successfully!")

    def decrypt_text(self):
        password = self.password_var.get()
        encrypted_input = self.text_input_field.get("1.0", tk.END).strip()

        if not password or not encrypted_input:
            messagebox.showerror("Error", "Please enter both password and encrypted text.")
            return

        try:
            # Extract the base64 encoded parts (Encrypted text, IV, and Salt) from the user input
            lines = encrypted_input.split("\n")

            encrypted_text = lines[0].split(":")[1].strip()
            iv = lines[1].split(":")[1].strip()
            salt = lines[2].split(":")[1].strip()

            # Decrypt the text
            decrypted_text = decrypt_text(encrypted_text, password, iv, salt)

            if decrypted_text:
                self.output_field.delete(1.0, tk.END)
                self.output_field.insert(tk.END, f"Decrypted Text: {decrypted_text}")
                messagebox.showinfo("Success", "Text decrypted successfully!")
            else:
                messagebox.showerror("Error", "Decryption failed!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract IV and Salt for decryption: {e}")


if __name__ == "__main__":
    # Create Tkinter root window
    root = tk.Tk()

    # Create app instance
    app = TextEncryptDecryptApp(root)

    # Run the app
    root.mainloop()
    