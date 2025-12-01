# 🚀 SecureScript AI System  
### *Revolutionizing Document Security with AI + Encryption*

SecureScript AI System is an intelligent platform designed to **generate, encrypt, hide, and securely access documents** using a combination of **Artificial Intelligence**, **AES encryption**, **Steganography**, **Biometrics**, and **OTP verification**.

This project showcases how **GenAI + Cybersecurity** can merge to build next-gen secure ecosystems that are **simple to use yet extremely hard to break**.

---

## 🛡️ Key Features

### 🔐 AES-128 Document Encryption
- Secures files using robust AES-128 cryptography  
- Ensures your confidential data remains protected end-to-end  

### 🤖 AI-Powered Document & Image Generation
- Generates documents/images through natural language prompts  
- Useful for automated reports, summaries, creative outputs, etc.

### 🖼️ Steganography (Key Hiding Inside Images)
- Hides encryption keys inside images (uploaded or AI-generated)  
- Secure embedding and extraction for untraceable key management  

### 👤 Biometric Authentication  
- **Face Recognition** via OpenCV + Facenet  
- **Voice Verification** using SpeechRecognition  
- Strong multi-factor access control  

### 🔑 OTP + Key-Based Secure Decryption
- OTP-based user verification  
- Extract hidden key from image  
- Safely decrypt documents using AES  

### 🖥️ Streamlit UI (Real-Time Interaction)
- Clean and simple user interface  
- Easy step-by-step flow: Generate → Encrypt → Hide Key → Authenticate → Decrypt  

---

## 🧠 Tech Stack

- **Python**
- **Streamlit**
- **OpenCV**
- **SpeechRecognition**
- **Cryptography (AES-128)**
- **Steganography**
- **AI/LLM Models**
- **Facenet**
- **OTP Integration**

---

## 🏗️ System Workflow

1. **User provides prompt** → AI generates document/image  
2. **AES encrypts** document  
3. **Key is hidden** within an image using steganography  
4. **User authentication**:
   - Facial recognition  
   - Voice verification  
   - OTP check  
5. **Document decrypted** only if all checks succeed  

This layered model ensures **no unauthorized user can bypass the system**.

---

## 🧩 Use Cases

- 🔒 Secure corporate documentation  
- 🏥 Confidential medical/financial record storage  
- 🎓 Tamper-proof academic certificates  
- 📁 Personal digital vault  
- 🕵️ Protected digital identity systems  

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/likhithanagasri/Secure-Script-Al-System
cd SecureScript-AI-System

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
