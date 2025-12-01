# 📜 SecureScript AI System  
### **Revolutionizing Document Security with AI + Encryption**

SecureScript AI System is an intelligent, multi-agent–powered platform designed to **securely generate, protect, store, and access confidential documents**.  
By combining **Generative AI**, **AES Encryption**, **Steganography**, **Biometrics**, and **Agent-Based Orchestration**, this project demonstrates how AI and cybersecurity together can create **next-generation secure digital ecosystems**.

---

# 🚀 Project Highlights

### ✅ **AES-128 Based Encryption**
Robust symmetric encryption for safeguarding sensitive documents with military-grade security.

### 🎨 **AI-Powered Document & Image Generation**
Generate documents and images from natural-language prompts using LLM-based agents.

### 🖼️ **Steganography Engine**
Hide secret AES keys inside images—either uploaded or AI-generated—using LSB steganography.

### 👁️‍🗨️ **Biometric Authentication**
- **Face Recognition** using OpenCV + deep learning  
- **Voice Verification** using SpeechRecognition

### 🔑 **Secure Decryption Workflow**
Multi-step unlocking using:  
✔ AES Key  
✔ OTP Authentication  
✔ Biometric Verification  

### 🖥️ **Streamlit Frontend**
Modern, interactive UI with real-time encryption, generation, and access workflows.

---

# 🧠 Multi-Agent Architecture (Aligned with Google GenAI Capstone Requirements)

This project integrates **multiple agents** to perform different tasks, demonstrating the core concepts taught in the Google GenAI 5-Day Agentic Program.

## 🧩 **1. Multi-Agent System**

### **🔶 Document Generation Agent (LLM-powered)**
- Creates summaries, confidential reports, templates.  
- Utilizes prompt engineering + sequential execution.

### **🔶 Image Generation Agent**
- Generates AI images for steganography or branding.  
- Runs in parallel to the document agent.

### **🔶 Encryption Agent**
- Handles document AES encryption/decryption.  
- Sequential workflow with OTP + biometric validation.

### **🔶 Steganography Agent**
- Embeds/extracts keys from images.

### **🔶 Authentication Agent**
- Handles Face + Voice biometric verification routines.

### **🔶 System Orchestrator Agent**
- Coordinates sequential + parallel agent operations.  
- Manages loops for retries & OTP expiration events.  

---

# 🛠️ **2. Tools Used (Google GenAI Requirement)**  

The system integrates multiple tool types:

### 🔧 **Custom MCP Tools**
- AES Encryption Tool  
- Steganography Encode/Decode Tool  
- Biometric Verification Tool  
- OTP Generator Tool  

### 🔧 **Built-in Tools**
- Code Execution (file processing, hashing, audio/image handling)  
- Optional: Google Search API for documentation templates  

### 🔧 **OpenAPI Tools**
- AI image generation models  
- Text generation / embedding tools for LLM-based agents  

---

# 🧬 **3. Memory & State Management (Google GenAI Requirement)**

### 🟦 Session Memory
Tracks user preferences, last accessed documents, and recent operations using in-memory session storage.

### 🟨 Long-Term Memory (Memory Bank)
Saves biometric profile, document access patterns, and commonly performed user tasks.

### 🟩 Context Engineering
Uses prompt compaction, reduced context windows, and pre-filled system prompts for agent efficiency.

---

# 📊 **4. Observability (Google GenAI Requirement)**  

Includes a complete observability layer:

- **Structured Logging**: Agent activity logs  
- **Tracing**: End-to-end tracking of encryption → biometric → stego workflows  
- **Metrics**:  
  - Encryption speed  
  - Biometric confidence scores  
  - OTP retry attempts  

---

# 🚀 **5. Agent Evaluation & Deployment**

### 🔄 **A2A Protocol**
Agents communicate using async message passing:
- Passing AES keys  
- Generating OTP  
- Triggering verification  
- Document routing  

### ☁️ Deployment Options
- Streamlit Cloud  
- HuggingFace Spaces  
- Docker / Render  
- Google Cloud VM / App Engine  

---

# 🧰 Tech Stack

### Languages & Frameworks  
- Python  
- Streamlit  
- OpenCV  
- SpeechRecognition  

### Security Components  
- AES-128 Encryption  
- Steganography (LSB method)  
- OTP-based Multi-factor Authentication  

### AI Components  
- LLM for content generation  
- Image models for custom assets  
- Facenet / CNN-based biometric models  

---

# 📁 Project Structure
```bash
SecureScript-AI/
│── agents/
│   ├── document_agent.py
│   ├── image_agent.py
│   ├── encryption_agent.py
│   ├── steganography_agent.py
│   ├── auth_agent.py
│   └── orchestrator_agent.py
│
│── tools/
│   ├── aes_tool.py
│   ├── otp_tool.py
│   ├── stego_tool.py
│   └── biometric_tool.py
│
│── ui/
│   └── streamlit_app.py
│
│── models/
│── data/
│── README.md

