# 🔐 CyberCrypt — AES-256 Encryption & Decryption Tool

CyberCrypt is a lightweight web-based cryptography application built with **Python, Flask, HTML, CSS, and JavaScript**.

It provides a simple interface for encrypting and decrypting text using **AES-256-CBC** with **PBKDF2-HMAC-SHA256** key derivation.

> ⚠️ **Disclaimer:** This project is developed for educational and cybersecurity learning purposes.

---

## 🚀 Features

- 🔐 AES-256-CBC encryption
- 🔓 AES-256-CBC decryption
- 🔑 PBKDF2-HMAC-SHA256 password-based key derivation
- 🧂 Random salt generation
- 🎲 Random IV generation
- 🔢 100,000 PBKDF2 iterations
- 📋 Copy encrypted/decrypted output
- 👁️ Show/Hide password
- 🔢 Character counter
- ⚡ Real-time operation status
- 💻 Cybersecurity-themed user interface
- 🌐 Flask-based web application
- 📁 Separate HTML, CSS, and JavaScript files
- 🖥️ Responsive web interface

---

## 🛡️ Cryptographic Workflow

```text
                 Master Password
                       │
                       ▼
              PBKDF2-HMAC-SHA256
                 100,000 iterations
                       │
                       ▼
                  AES-256 Key
                       │
                       ▼
                  AES-256-CBC
                       │
                       ▼
                Encrypted Data
                       │
                       ▼
                    Base64
````

A new random **salt** and **IV (Initialization Vector)** are generated for every encryption operation.

---

## 🧰 Technologies Used

### Backend

* Python
* Flask
* Cryptography

### Frontend

* HTML5
* CSS3
* JavaScript

### Cryptography

* AES-256-CBC
* PBKDF2-HMAC-SHA256
* SHA-256
* PKCS7 Padding
* Base64 Encoding
* Random Salt
* Random IV

---

## 📂 Project Structure

```text
CyberCrypt-AES/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── assets/
│   └── screenshots/
│       ├── home.png
│       ├── encryption.png
│       └── decryption.png
│
└── venv/
```

> `venv/` should be excluded from Git using `.gitignore`.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Soumya-CSE/CyberCrypt-AES.git
```

```bash
cd CyberCrypt-AES
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Flask server:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

## 🔐 Encryption Process

To encrypt text:

1. Enter a password.
2. Enter the plaintext.
3. Click **ENCRYPT**.
4. CyberCrypt generates a random salt.
5. CyberCrypt generates a random IV.
6. PBKDF2-HMAC-SHA256 derives the AES-256 key.
7. AES-256-CBC encrypts the plaintext.
8. The encrypted result is displayed.

### Encryption Flow

```text
Plaintext
    │
    ▼
Password
    │
    ▼
PBKDF2-HMAC-SHA256
    │
    ▼
AES-256 Key
    │
    ▼
AES-256-CBC
    │
    ▼
Ciphertext
    │
    ▼
Base64 Output
```

---

## 🔓 Decryption Process

To decrypt text:

1. Enter the same password used for encryption.
2. Enter the encrypted text.
3. Provide the required IV and salt.
4. Click **DECRYPT**.
5. PBKDF2 derives the AES-256 key.
6. AES-256-CBC decrypts the ciphertext.
7. The original plaintext is displayed.

### Decryption Flow

```text
Encrypted Data
      │
      ├──────── IV
      │
      ├──────── Salt
      │
      └──────── Password
                    │
                    ▼
           PBKDF2-HMAC-SHA256
                    │
                    ▼
               AES-256 Key
                    │
                    ▼
              AES-256-CBC
                    │
                    ▼
             Original Text
```

---

## 🖥️ Screenshots

### 🏠 Home Interface

<img width="1897" height="960" alt="Home" src="https://github.com/user-attachments/assets/d47a9d8c-c6fa-4b58-b95b-9bf80b55a26d" />


### 🔐 Encryption Interface

<img width="1901" height="901" alt="Encryption" src="https://github.com/user-attachments/assets/33ebd48c-e87f-4571-8f3c-e14e4492a60a" />

### 🔓 Decryption Interface

<img width="1907" height="902" alt="Decryption" src="https://github.com/user-attachments/assets/791d7690-1d15-45cd-abba-7f6702f7a086" />



---

## 🔒 Security Details

### AES-256

CyberCrypt uses **AES-256**, a symmetric encryption algorithm using a 256-bit encryption key.

### PBKDF2-HMAC-SHA256

The user's password is not directly used as the AES encryption key.

Instead:

```text
Password
   │
   ▼
PBKDF2-HMAC-SHA256
   │
   ▼
100,000 Iterations
   │
   ▼
256-bit AES Key
```

This makes password-based key derivation more computationally expensive.

### Random Salt

A random salt is generated for every encryption operation.

The salt is required during decryption to derive the same encryption key.

### Random IV

A new random 16-byte IV is generated for every encryption operation.

The IV is required during decryption.

### PKCS7 Padding

PKCS7 padding is used to ensure that plaintext is compatible with the AES block size.

---

## 📌 API Endpoints

### Encrypt

```text
POST /encrypt
```

Example request:

```json
{
    "text": "Hello World",
    "password": "myPassword"
}
```

Example response:

```json
{
    "success": true,
    "encrypted_text": "...",
    "iv": "...",
    "salt": "..."
}
```

### Decrypt

```text
POST /decrypt
```

Example request:

```json
{
    "encrypted_text": "...",
    "iv": "...",
    "salt": "...",
    "password": "myPassword"
}
```

Example response:

```json
{
    "success": true,
    "decrypted_text": "Hello World"
}
```

---

## 🧪 Example

### Original Text

```text
Hello CyberSecurity!
```

### Password

```text
MySecurePassword123
```

### Encryption

```text
Hello CyberSecurity!
        │
        ▼
PBKDF2-HMAC-SHA256
        │
        ▼
AES-256 Key
        │
        ▼
AES-256-CBC
        │
        ▼
Encrypted Data
```

### Decryption

```text
Encrypted Data
        │
        ├── Password
        ├── Salt
        └── IV
        │
        ▼
PBKDF2-HMAC-SHA256
        │
        ▼
AES-256 Key
        │
        ▼
AES-256-CBC Decryption
        │
        ▼
Hello CyberSecurity!
```

---

## ⚠️ Limitations

This project is designed primarily for **educational and cybersecurity learning purposes**.

* AES-CBC does not provide built-in authentication.
* The correct password is required for decryption.
* The IV and salt must be preserved.
* Password security depends on password strength.
* The application is primarily designed for text encryption.
* It should not be considered a production-grade secure messaging system.
* No permanent encrypted data storage is implemented.

For production applications, an authenticated encryption mode such as **AES-GCM** would generally be preferable.

---

## 🎯 Learning Objectives

This project demonstrates practical concepts including:

* Symmetric cryptography
* AES encryption
* AES-256
* CBC mode
* PBKDF2
* HMAC
* SHA-256
* Password-based key derivation
* Cryptographic salts
* Initialization Vectors
* PKCS7 padding
* Base64 encoding
* Flask web development
* REST-style API communication
* HTML5
* CSS3
* JavaScript
* Client-server communication
* Git
* GitHub

---

## 🔧 Requirements

The project requires **Python 3.x** and the dependencies listed in:

```text
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Development

Clone the repository:

```bash
git clone https://github.com/Soumya-CSE/CyberCrypt-AES.git
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

## 📈 Future Improvements

Possible future improvements include:

* 🔐 AES-GCM authenticated encryption
* 📁 File encryption and decryption
* 🔑 Password strength meter
* 📜 Encryption history
* 📥 Secure encrypted file export
* 📤 Encrypted file import
* 🌙 Dark/light theme
* 🔐 Multi-user authentication
* 🛡️ Improved error handling
* 📊 Security activity logging

---

## 👨‍💻 Author

### Soumya Kanti Hazra

Computer Science & Engineering Student

**GitHub:**
[https://github.com/Soumya-CSE](https://github.com/Soumya-CSE)

**LinkedIn:**
[https://www.linkedin.com/in/soumya-kanti-hazra-b20162374](https://www.linkedin.com/in/soumya-kanti-hazra-b20162374)

**TryHackMe:**
[https://tryhackme.com/p/soumyahazra](https://tryhackme.com/p/soumyahazra)

---

## 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

## ⭐ Support

If you found this project useful for learning **Cybersecurity, Cryptography, Python, or Flask**, consider giving the repository a ⭐ on GitHub.

---

```

```
```
