

import streamlit as st
from PIL import Image
import io
import os
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
import requests
import speech_recognition as sr
import cv2
from deepface import DeepFace
from fpdf import FPDF

# ---------------------- Session State Initialization ----------------------
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False
if "face_decrypt_verified" not in st.session_state:
    st.session_state.face_decrypt_verified = False

# ---------------------- UI Config ----------------------
st.set_page_config(page_title="SecureScript AI", layout="centered", page_icon="🔐")
st.markdown("""
    <style>
    .main { background-color: #111827; color: white; }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 5px 0;
    }
    .stDownloadButton>button {
        background-color: #10B981;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 5px 0;
    }
    .stTextInput>div>input, .stTextArea textarea {
        background-color: #1F2937;
        color: white;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Together.ai API ----------------------
TOGETHER_API_KEY = "16fe845937edfc5513d5a3adca83f7d53f207fe64aa32da3672e2fa224fa0579"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

def generate_document(prompt: str, model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1") -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You generate clean, professional documents from prompts."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    try:
        response = requests.post(TOGETHER_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠ Error: {e}"

def text_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    font_path = "DejaVuSans.ttf"
    if os.path.exists(font_path):
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=12)
    else:
        pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest='S').encode("latin1")

# ---------------------- Voice Auth ----------------------
def verify_voice_command(expected_phrase="unlock secure system"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎤 Say your secret phrase...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            if expected_phrase.lower() in command:
                st.success("✅ Voice matched. Access granted.")
                return True
            else:
                st.error("❌ Voice command did not match.")
        except Exception as e:
            st.error(f"❌ Voice error: {e}")
    return False

# ---------------------- Face Auth ----------------------
def handle_face_authentication(mode):
    stframe = st.empty()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Cannot access webcam")
        return False
    st.info(f"📸 {'Registering' if mode == 'register' else 'Verifying'} face...")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        st.error("❌ Failed to capture image")
        return False
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    stframe.image(frame_rgb, channels="RGB")
    save_dir = "captured_faces"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "registered_face.jpg")
    if mode == "register":
        cv2.imwrite(save_path, frame)
        st.success(f"✅ Face registered and saved to `{save_path}`")
        return False
    elif mode == "verify":
        if not os.path.exists(save_path):
            st.error("⚠️ No registered face found. Please register a face first.")
            return False
        try:
            result = DeepFace.verify(img1_path=save_path, img2_path=frame, enforce_detection=False)
            return result["verified"]
        except Exception as e:
            st.error(f"⚠️ Face verification failed: {e}")
            return False

# ---------------------- AES + Stego ----------------------
def generate_aes_key(): return get_random_bytes(16)
def encrypt_pdf(pdf_bytes, key):
    cipher = AES.new(key, AES.MODE_CBC); iv = cipher.iv
    return iv + cipher.encrypt(pad(pdf_bytes, AES.block_size))
def decrypt_pdf(encrypted_data, key):
    try:
        iv = encrypted_data[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
    except Exception as e:
        raise ValueError(f"❌ Decryption failed: {e}")

def embed_key_in_image(image_bytes, aes_key):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    key_bin = ''.join(format(byte, '08b') for byte in aes_key) + '11111110'
    pixels = list(img.getdata()); new_pixels = []; idx = 0
    for pixel in pixels:
        r, g, b = pixel
        if idx < len(key_bin): r = (r & ~1) | int(key_bin[idx]); idx += 1
        if idx < len(key_bin): g = (g & ~1) | int(key_bin[idx]); idx += 1
        if idx < len(key_bin): b = (b & ~1) | int(key_bin[idx]); idx += 1
        new_pixels.append((r, g, b))
    img.putdata(new_pixels)
    out = io.BytesIO(); img.save(out, format="PNG")
    return out.getvalue()

def extract_key_from_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    binary = ''.join(str(value & 1) for pixel in img.getdata() for value in pixel)
    byte_list = [binary[i:i+8] for i in range(0, len(binary), 8)]
    result = bytearray()
    for b in byte_list:
        if b == '11111110': break
        result.append(int(b, 2))
    return bytes(result)

# ---------------------- UI ----------------------
st.title("🔐 SecureScript AI System")

st.markdown("### 🛡️ Authenticate First")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🖍️ Register Face"):
        handle_face_authentication("register")
with col2:
    if st.button("🧑 Face Access"):
        if handle_face_authentication("verify"):
            st.session_state.access_granted = True
            st.success("🔓 Face Access Granted.")
            st.rerun()
with col3:
    if st.button("🎤 Voice Access"):
        if verify_voice_command():
            st.session_state.access_granted = True
            st.rerun()

if st.session_state.access_granted:
    menu = st.sidebar.selectbox("Choose Action", [
        "📄 Generate Document", "📂 Upload PDF","🌚 Encrypt PDF",
        "🕛 Stego Image", "🕵️ Extract AES Key", "🗂️ Decrypt PDF"])

    if menu == "📄 Generate Document":
        prompt = st.text_area("Enter your prompt")

        # Initialize session state variables if not already set
        if "pdf_data" not in st.session_state:
            st.session_state.pdf_data = None
        if "generated_key" not in st.session_state:
            st.session_state.generated_key = None

        if st.button("📄 Generate Document"):
            if prompt:
                content = generate_document(prompt)
                st.session_state.pdf_data = text_to_pdf(content)
                st.session_state.generated_key = generate_aes_key()
                st.success("📄 Document generated successfully!")
            else:
                st.warning("⚠️ Please enter a prompt.")

        if st.session_state.pdf_data and st.session_state.generated_key:
            st.download_button(
                "📅 Download PDF", 
                data=io.BytesIO(st.session_state.pdf_data), 
                file_name="secure_doc.pdf"
            )
            st.download_button(
                "🔑 Download AES Key", 
                data=io.BytesIO(st.session_state.generated_key), 
                file_name="aes_key.key"
            )
    elif menu == "📂 Upload PDF":
        uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_pdf:
            key = generate_aes_key()
            st.download_button("🔑 Download AES Key", io.BytesIO(key), file_name="aes_key.key")

    elif menu == "🌚 Encrypt PDF":
        uploaded_pdf = st.file_uploader("Upload PDF to Encrypt", type=["pdf"])
        aes_key_file = st.file_uploader("Upload AES Key", type=["key"])
        if uploaded_pdf and aes_key_file:
            encrypted = encrypt_pdf(uploaded_pdf.read(), aes_key_file.read())
            st.download_button("Download Encrypted PDF", encrypted, file_name="encrypted_doc.enc")

    elif menu == "🕛 Stego Image":
        image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        aes_key_file = st.file_uploader("Upload AES Key", type=["key"])
        if image_file and aes_key_file:
            stego = embed_key_in_image(image_file.read(), aes_key_file.read())
            st.download_button("Download Stego Image", stego, file_name="stego_image.png")

    elif menu == "🕵️ Extract AES Key":
        image_file = st.file_uploader("Upload Stego Image", type=["png"])
        if image_file:
            key = extract_key_from_image(image_file.read())
            st.download_button("Download Extracted Key", key, file_name="extracted_key.key")

    elif menu == "🗂️ Decrypt PDF":
        st.subheader("🔐 Face Verification for Decryption")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🖍️ Register Face (For Decryption)"):
                handle_face_authentication("register")
        with col2:
            if st.button("🧑 Face Access (To Decrypt)"):
                if handle_face_authentication("verify"):
                    st.session_state.face_decrypt_verified = True
                    st.success("✅ Face verified for decryption")

        if st.session_state.face_decrypt_verified:
            encrypted_file = st.file_uploader("📂 Upload Encrypted PDF", type=["enc"])
            aes_key_file = st.file_uploader("🔑 Upload AES Key", type=["key"])
            if encrypted_file and aes_key_file:
                try:
                    decrypted = decrypt_pdf(encrypted_file.read(), aes_key_file.read())
                    st.download_button("📥 Download Decrypted PDF", decrypted, file_name="decrypted_doc.pdf")
                except Exception as e:
                    st.error(str(e))
        else:
            st.info("🔐 Please complete Face Access first to view decryption inputs.")
else:
    st.info("🔐 Please authenticate first using face or voice.")
