# 🔐 AES Text Encryption & Decryption

A Python-based desktop application that securely encrypts and decrypts text using the **Advanced Encryption Standard (AES-256)**. Built with **Tkinter** for the graphical user interface and the **Cryptography** library for secure password-based encryption.

## ✨ Features

- 🔒 AES-256 encryption
- 🔑 Password-based key derivation using PBKDF2-HMAC-SHA256
- 🧂 Random Salt generation for every encryption
- 🎲 Random Initialization Vector (IV)
- 📦 AES-CBC encryption mode
- 📝 Encrypt and decrypt plain text
- 🖥️ Simple and user-friendly Tkinter GUI
- 🔐 Secure Base64 encoded output

---

## 🛠️ Technologies Used

- Python 3
- Tkinter
- Cryptography
- AES-256
- PBKDF2-HMAC-SHA256
- Base64

---

## 📂 Project Structure

```
AES-Encryption/
│── AES.py
│── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/Soumya-CSE/aes-encryption-decryption.git
```

### Navigate to the project

```bash
cd aes-encryption-decryption
```

### Install dependencies

```bash
pip install cryptography
```

or

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python AES.py
```

---

## 🚀 How to Use

### Encrypt Text

1. Enter a password.
2. Type the text you want to encrypt.
3. Click **Encrypt Text**.
4. Copy the generated:
   - Encrypted Text
   - IV
   - Salt

### Decrypt Text

1. Enter the same password.
2. Paste the encrypted output in the following format:

```
Encrypted Text: <encrypted_text>
IV: <iv>
Salt: <salt>
```

3. Click **Decrypt Text** to recover the original message.

---

## 🔐 Encryption Workflow

```
Password
   │
   ▼
PBKDF2-HMAC-SHA256
   │
   ▼
AES-256 Key
   │
   ▼
Random Salt + Random IV
   │
   ▼
AES-CBC Encryption
   │
   ▼
Base64 Encoded Ciphertext
```

---

## 📸 Application Preview



images/
<img width="1920" height="1080" alt="encryption" src="https://github.com/user-attachments/assets/fd01e25e-c474-437b-90ae-ab8b6a503925" />

<img width="1920" height="1080" alt="decryption" src="https://github.com/user-attachments/assets/35f1f2ff-bbd7-4feb-9460-8a4cac87e130" />




---

## 🔒 Security Features

- AES-256 Encryption
- PBKDF2 Key Derivation
- SHA-256 Hashing
- 100,000 PBKDF2 Iterations
- Random Salt
- Random IV
- PKCS7 Padding
- Password-Based Encryption

---

## 📋 Requirements

- Python 3.8+
- cryptography

Install using:

```bash
pip install cryptography
```

---

## 🚀 Future Enhancements

- File encryption and decryption
- Dark mode
- Copy-to-clipboard button
- Export encrypted text
- Password strength checker
- Drag-and-drop support
- AES-GCM support

---

## 👨‍💻 Author

**Soumya Hazra**

- GitHub: https://github.com/Soumya-CSE


---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub!
