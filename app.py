from flask import Flask, render_template, request, jsonify

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import os
import base64


app = Flask(__name__)


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

    # Generate random salt
    salt = os.urandom(16)

    # Generate AES-256 key
    key = derive_key(password, salt)

    # PKCS7 padding
    padder = padding.PKCS7(128).padder()

    padded_data = (
        padder.update(plaintext.encode())
        + padder.finalize()
    )

    # Generate random IV
    iv = os.urandom(16)

    # AES-256 CBC
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

    return {
        "encrypted_text": encrypted_text,
        "iv": iv_text,
        "salt": salt_text
    }


# ==========================================================
# DECRYPTION
# ==========================================================

def decrypt_data(
    encrypted_text,
    password,
    iv_text,
    salt_text
):

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

    # AES-256 CBC
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    decrypted_data = (
        decryptor.update(encrypted_data)
        + decryptor.finalize()
    )

    # Remove PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()

    decrypted_data = (
        unpadder.update(decrypted_data)
        + unpadder.finalize()
    )

    return decrypted_data.decode()


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ==========================================================
# ENCRYPT API
# ==========================================================

@app.route("/encrypt", methods=["POST"])
def encrypt():

    try:

        data = request.get_json()

        plaintext = data.get(
            "text",
            ""
        ).strip()

        password = data.get(
            "password",
            ""
        )

        # Validate password
        if not password:

            return jsonify({
                "success": False,
                "message": "Please enter a password."
            }), 400

        # Validate plaintext
        if not plaintext:

            return jsonify({
                "success": False,
                "message": "Please enter text to encrypt."
            }), 400

        # Encrypt
        result = encrypt_data(
            plaintext,
            password
        )

        return jsonify({
            "success": True,
            "message": "Encryption successful.",
            "encrypted_text": result["encrypted_text"],
            "iv": result["iv"],
            "salt": result["salt"]
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Encryption failed."
        }), 500


# ==========================================================
# DECRYPT API
# ==========================================================

@app.route("/decrypt", methods=["POST"])
def decrypt():

    try:

        data = request.get_json()

        encrypted_text = data.get(
            "encrypted_text",
            ""
        ).strip()

        iv = data.get(
            "iv",
            ""
        ).strip()

        salt = data.get(
            "salt",
            ""
        ).strip()

        password = data.get(
            "password",
            ""
        )

        # Validate password
        if not password:

            return jsonify({
                "success": False,
                "message": "Please enter the password."
            }), 400

        # Validate encrypted data
        if not encrypted_text or not iv or not salt:

            return jsonify({
                "success": False,
                "message": "Encrypted text, IV and salt are required."
            }), 400

        # Decrypt
        decrypted = decrypt_data(
            encrypted_text,
            password,
            iv,
            salt
        )

        return jsonify({
            "success": True,
            "message": "Decryption successful.",
            "decrypted_text": decrypted
        })

    except Exception:

        return jsonify({
            "success": False,
            "message": "Wrong password or corrupted encrypted data."
        }), 400


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
    