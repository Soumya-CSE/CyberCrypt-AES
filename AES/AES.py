import tkinter as tk
from tkinter import messagebox

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import os
import base64


# ==========================================================
# KEY DERIVATION
# ==========================================================

def derive_key(password, salt):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,              # AES-256
        salt=salt,
        iterations=100000
    )

    return kdf.derive(password.encode())


# ==========================================================
# ENCRYPTION
# ==========================================================

def encrypt_data(plaintext, password):

    try:

        # Random salt
        salt = os.urandom(16)

        # Generate AES key
        key = derive_key(password, salt)

        # Padding
        padder = padding.PKCS7(128).padder()

        padded_data = (
            padder.update(plaintext.encode())
            + padder.finalize()
        )

        # Random IV
        iv = os.urandom(16)

        # AES CBC
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv)
        )

        encryptor = cipher.encryptor()

        encrypted_data = (
            encryptor.update(padded_data)
            + encryptor.finalize()
        )

        # Convert to Base64
        encrypted_text = base64.b64encode(
            encrypted_data
        ).decode()

        iv_text = base64.b64encode(iv).decode()

        salt_text = base64.b64encode(salt).decode()

        return encrypted_text, iv_text, salt_text

    except Exception as e:

        print("Encryption Error:", e)

        return None, None, None


# ==========================================================
# DECRYPTION
# ==========================================================

def decrypt_data(encrypted_text, password, iv_text, salt_text):

    try:

        # Convert Base64 back to bytes
        encrypted_data = base64.b64decode(
            encrypted_text
        )

        iv = base64.b64decode(
            iv_text
        )

        salt = base64.b64decode(
            salt_text
        )

        # Generate same key
        key = derive_key(
            password,
            salt
        )

        # AES CBC
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv)
        )

        decryptor = cipher.decryptor()

        decrypted_data = (
            decryptor.update(encrypted_data)
            + decryptor.finalize()
        )

        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()

        decrypted_data = (
            unpadder.update(decrypted_data)
            + unpadder.finalize()
        )

        return decrypted_data.decode()

    except Exception as e:

        print("Decryption Error:", e)

        return None


# ==========================================================
# GUI APPLICATION
# ==========================================================

class CyberCryptApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "CyberCrypt - AES Security Tool"
        )

        self.root.geometry(
            "900x650"
        )

        self.root.configure(
            bg="#08110D"
        )

        self.root.resizable(
            False,
            False
        )

        self.create_ui()


    # ======================================================
    # USER INTERFACE
    # ======================================================

    def create_ui(self):

        # ---------------- HEADER ----------------

        header = tk.Frame(
            self.root,
            bg="#0D1914",
            height=90
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔐 CYBERCRYPT",
            font=("Consolas", 24, "bold"),
            fg="#00FF88",
            bg="#0D1914"
        ).pack(
            anchor="w",
            padx=30,
            pady=(12, 0)
        )

        tk.Label(
            header,
            text="AES-256 TEXT ENCRYPTION & DECRYPTION TOOL",
            font=("Consolas", 10),
            fg="#6AFFB0",
            bg="#0D1914"
        ).pack(
            anchor="w",
            padx=32
        )


        # ---------------- STATUS ----------------

        status_frame = tk.Frame(
            self.root,
            bg="#08110D"
        )

        status_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.status_label = tk.Label(
            status_frame,
            text="● SYSTEM SECURE",
            font=("Consolas", 10, "bold"),
            fg="#00FF88",
            bg="#08110D"
        )

        self.status_label.pack(
            side="left"
        )

        tk.Label(
            status_frame,
            text="AES-256 | PBKDF2-SHA256 | CBC",
            font=("Consolas", 9),
            fg="#718078",
            bg="#08110D"
        ).pack(
            side="right"
        )


        # ---------------- PASSWORD ----------------

        password_frame = tk.Frame(
            self.root,
            bg="#111D17",
            highlightbackground="#1F4D39",
            highlightthickness=1
        )

        password_frame.pack(
            fill="x",
            padx=30,
            pady=5
        )

        tk.Label(
            password_frame,
            text="🔑 MASTER PASSWORD",
            font=("Consolas", 10, "bold"),
            fg="#00FF88",
            bg="#111D17"
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        self.password_entry = tk.Entry(
            password_frame,
            show="*",
            font=("Consolas", 11),
            bg="#070B09",
            fg="#00FF88",
            insertbackground="#00FF88",
            relief="flat"
        )

        self.password_entry.pack(
            fill="x",
            padx=15,
            pady=(0, 12),
            ipady=8
        )


        # ---------------- TEXT AREAS ----------------

        main_frame = tk.Frame(
            self.root,
            bg="#08110D"
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )


        # INPUT PANEL

        input_frame = tk.Frame(
            main_frame,
            bg="#111D17",
            highlightbackground="#1F4D39",
            highlightthickness=1
        )

        input_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        tk.Label(
            input_frame,
            text="INPUT BUFFER",
            font=("Consolas", 10, "bold"),
            fg="#00FF88",
            bg="#111D17"
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        self.input_text = tk.Text(
            input_frame,
            height=12,
            font=("Consolas", 10),
            bg="#070B09",
            fg="#D7FFE8",
            insertbackground="#00FF88",
            selectbackground="#145C3A",
            relief="flat",
            wrap="word"
        )

        self.input_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )


        # OUTPUT PANEL

        output_frame = tk.Frame(
            main_frame,
            bg="#111D17",
            highlightbackground="#1F4D39",
            highlightthickness=1
        )

        output_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        tk.Label(
            output_frame,
            text="SECURE OUTPUT",
            font=("Consolas", 10, "bold"),
            fg="#00FF88",
            bg="#111D17"
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        self.output_text = tk.Text(
            output_frame,
            height=12,
            font=("Consolas", 10),
            bg="#070B09",
            fg="#00FF88",
            insertbackground="#00FF88",
            selectbackground="#145C3A",
            relief="flat",
            wrap="word"
        )

        self.output_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )


        # ---------------- BUTTONS ----------------

        button_frame = tk.Frame(
            self.root,
            bg="#08110D"
        )

        button_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )


        tk.Button(
            button_frame,
            text="⚡ ENCRYPT",
            command=self.encrypt,
            font=("Consolas", 11, "bold"),
            bg="#00A85A",
            fg="white",
            activebackground="#00FF88",
            activeforeground="black",
            relief="flat",
            cursor="hand2",
            width=20,
            pady=8
        ).pack(
            side="left",
            padx=(0, 10)
        )


        tk.Button(
            button_frame,
            text="🔓 DECRYPT",
            command=self.decrypt,
            font=("Consolas", 11, "bold"),
            bg="#164D38",
            fg="#00FF88",
            activebackground="#00FF88",
            activeforeground="black",
            relief="flat",
            cursor="hand2",
            width=20,
            pady=8
        ).pack(
            side="left"
        )


        tk.Button(
            button_frame,
            text="✕ CLEAR",
            command=self.clear,
            font=("Consolas", 11, "bold"),
            bg="#2A302D",
            fg="#D7FFE8",
            activebackground="#444C48",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=15,
            pady=8
        ).pack(
            side="right"
        )


        # ---------------- BOTTOM STATUS ----------------

        bottom = tk.Frame(
            self.root,
            bg="#0D1914"
        )

        bottom.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        self.operation_status = tk.Label(
            bottom,
            text="STATUS: READY | Waiting for operation...",
            font=("Consolas", 9),
            fg="#6AFFB0",
            bg="#0D1914"
        )

        self.operation_status.pack(
            pady=8
        )


    # ======================================================
    # ENCRYPT BUTTON
    # ======================================================

    def encrypt(self):

        password = self.password_entry.get()

        plaintext = self.input_text.get(
            "1.0",
            tk.END
        ).strip()


        if not password:

            messagebox.showerror(
                "Security Error",
                "Please enter a password."
            )

            return


        if not plaintext:

            messagebox.showerror(
                "Security Error",
                "Please enter text to encrypt."
            )

            return


        encrypted, iv, salt = encrypt_data(
            plaintext,
            password
        )


        if encrypted is None:

            messagebox.showerror(
                "Error",
                "Encryption failed."
            )

            return


        # Clear output
        self.output_text.delete(
            "1.0",
            tk.END
        )


        # Display encrypted package
        self.output_text.insert(
            tk.END,
            "Encrypted Text:\n"
        )

        self.output_text.insert(
            tk.END,
            encrypted
        )

        self.output_text.insert(
            tk.END,
            "\n\nIV:\n"
        )

        self.output_text.insert(
            tk.END,
            iv
        )

        self.output_text.insert(
            tk.END,
            "\n\nSalt:\n"
        )

        self.output_text.insert(
            tk.END,
            salt
        )


        self.operation_status.config(
            text="STATUS: ENCRYPTION SUCCESSFUL | AES-256 CBC",
            fg="#00FF88"
        )


        messagebox.showinfo(
            "Success",
            "Text encrypted successfully!"
        )


    # ======================================================
    # DECRYPT BUTTON
    # ======================================================

    def decrypt(self):

        password = self.password_entry.get()

        data = self.input_text.get(
            "1.0",
            tk.END
        ).strip()


        if not password:

            messagebox.showerror(
                "Security Error",
                "Please enter the password."
            )

            return


        if not data:

            messagebox.showerror(
                "Security Error",
                "Please paste encrypted data."
            )

            return


        try:

            # Find the required sections
            lines = data.splitlines()

            encrypted_text = ""
            iv = ""
            salt = ""

            current_section = None


            for line in lines:

                line = line.strip()


                if line == "Encrypted Text:":
                    current_section = "encrypted"

                elif line == "IV:":
                    current_section = "iv"

                elif line == "Salt:":
                    current_section = "salt"

                elif line:

                    if current_section == "encrypted":
                        encrypted_text += line

                    elif current_section == "iv":
                        iv += line

                    elif current_section == "salt":
                        salt += line


            if not encrypted_text or not iv or not salt:

                raise ValueError(
                    "Invalid encrypted data format."
                )


            # Decrypt
            decrypted = decrypt_data(
                encrypted_text,
                password,
                iv,
                salt
            )


            if decrypted is None:

                self.operation_status.config(
                    text="STATUS: DECRYPTION FAILED",
                    fg="#FF5555"
                )

                messagebox.showerror(
                    "Decryption Failed",
                    "Wrong password or corrupted encrypted data."
                )

                return


            # Display result
            self.output_text.delete(
                "1.0",
                tk.END
            )

            self.output_text.insert(
                tk.END,
                "DECRYPTED TEXT:\n\n"
            )

            self.output_text.insert(
                tk.END,
                decrypted
            )


            self.operation_status.config(
                text="STATUS: DECRYPTION SUCCESSFUL | AES-256 CBC",
                fg="#00FF88"
            )


            messagebox.showinfo(
                "Success",
                "Text decrypted successfully!"
            )


        except Exception as e:

            self.operation_status.config(
                text="STATUS: INVALID ENCRYPTED DATA",
                fg="#FF5555"
            )

            messagebox.showerror(
                "Invalid Data",
                str(e)
            )


    # ======================================================
    # CLEAR BUTTON
    # ======================================================

    def clear(self):

        self.password_entry.delete(
            0,
            tk.END
        )

        self.input_text.delete(
            "1.0",
            tk.END
        )

        self.output_text.delete(
            "1.0",
            tk.END
        )

        self.operation_status.config(
            text="STATUS: READY | Waiting for operation...",
            fg="#6AFFB0"
        )


# ==========================================================
# START APPLICATION
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CyberCryptApp(root)

    root.mainloop()


