import streamlit as st
st.set_page_config(page_title="Advanced Image Steganography", layout="centered")

from PIL import Image
import hashlib
import numpy as np
import io
import base64

# PyCryptodome imports with fallback
try:
    from Crypto.Random import get_random_bytes
    from Crypto.Cipher import AES
    CRYPTO_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Crypto library missing: {e}")
    st.info("💡 Install with: `pip install pycryptodome`")
    st.stop()
    CRYPTO_AVAILABLE = False

# Noise functions (Pillow-only, no OpenCV)
def add_gaussian_noise(image, sigma=0.01):
    img_array = np.array(image, dtype=np.float32)
    noise = np.random.normal(0, sigma * 255, img_array.shape)
    noisy = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy)

def compute_psnr(img1, img2):
    img1 = np.array(img1).astype(np.float32)
    img2 = np.array(img2).astype(np.float32)
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    return 10.0 * np.log10((255.0 ** 2) / mse)

# AES Cipher Class
class AESCipher:
    def __init__(self, key):
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome required: pip install pycryptodome")
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = get_random_bytes(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return base64.b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = base64.b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

    def __pad(self, plain_text):
        padding_needed = self.block_size - len(plain_text) % self.block_size
        return plain_text + chr(padding_needed) * padding_needed

    @staticmethod
    def __unpad(plain_text):
        return plain_text[:-ord(plain_text[-1])]

# Helper Functions
def to_binary(data):
    if isinstance(data, str):
        return ''.join([format(ord(char), "08b") for char in data])
    return format(data, "08b")

def encode_message(image, message, aes_cipher):
    img = image.convert("RGB")
    encrypted_message = aes_cipher.encrypt(message) + "$$$"
    message_bin = to_binary(encrypted_message)
    width, height = img.size
    idx = 0

    for x in range(width):
        for y in range(height):
            if idx >= len(message_bin):
                return img
            r, g, b = img.getpixel((x, y))
            r = int(to_binary(r)[:-1] + message_bin[idx], 2)
            g = int(to_binary(g)[:-1] + (message_bin[idx + 1] if idx + 1 < len(message_bin) else '0'), 2)
            b = int(to_binary(b)[:-1] + (message_bin[idx + 2] if idx + 2 < len(message_bin) else '0'), 2)
            img.putpixel((x, y), (r, g, b))
            idx += 3
    return img

def decode_message(image, aes_cipher):
    binary_data = ""
    width, height = image.size
    
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            binary_data += to_binary(r)[-1] + to_binary(g)[-1] + to_binary(b)[-1]
            
            if len(binary_data) >= 24:  # Enough bits for "$$$"
                try:
                    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
                    decoded_text = "".join([chr(int(byte, 2)) for byte in all_bytes])
                    end_marker = decoded_text.find("$$$")
                    if end_marker != -1:
                        return aes_cipher.decrypt(decoded_text[:end_marker])
                except:
                    continue
    raise ValueError("No valid message found or incorrect key")

def encode_image(cover_image, secret_image):
    cover_img = cover_image.convert("RGB")
    secret_img = secret_image.resize(cover_img.size).convert("RGB")
    cover_pixels = np.array(cover_img)
    secret_pixels = np.array(secret_img) // 16
    encoded_pixels = (cover_pixels & 240) | secret_pixels
    return Image.fromarray(encoded_pixels.astype("uint8"), "RGB")

def decode_image(encoded_image, secret_size):
    encoded_img = np.array(encoded_image)
    secret_pixels = (encoded_img & 15) * 16
    return Image.fromarray(secret_pixels.astype("uint8"), "RGB").resize(secret_size)

# Main App
def main():
    st.markdown("""
    <style>
    .css-1d391kg {background: linear-gradient(to right, #ff7e5f, #feb47b);}
    .stButton>button {background-color: #ff6347; color: white; border-radius: 8px; padding: 10px 20px; font-size: 16px;}
    .stButton>button:hover {background-color: white;}
    h1, h2 {color: #ff6347;}
    </style>
    """, unsafe_allow_html=True)

    st.title("🔐 Advanced Image Steganography 🖼️")
    st.subheader("AES Encryption + LSB + Noise Analysis")

    action = st.radio("🎯 Choose Action:", ("Encode", "Decode"))

    if action == "Encode":
        encode_choice = st.radio("💬 Choose Encoding Type:", ("Message", "Image"))
        uploaded_file = st.file_uploader("Upload Cover Image 📷", type=["png", "jpg", "jpeg"])

        if encode_choice == "Message":
            message = st.text_area("Enter Message to Hide 📝")
            key = st.text_input("Enter Encryption Key 🔑")
            if st.button("Encode 📩") and uploaded_file and message and key:
                image = Image.open(uploaded_file)
                aes_cipher = AESCipher(key)
                encoded_img = encode_message(image, message, aes_cipher)
                buffer = io.BytesIO()
                encoded_img.save(buffer, format="PNG")
                st.download_button("Download Encoded Image 📥", buffer.getvalue(), "encoded_image.png", "image/png")
        elif encode_choice == "Image":
            secret_file = st.file_uploader("Upload Secret Image 🖼️", type=["png", "jpg", "jpeg"])
            if st.button("Encode 📩") and uploaded_file and secret_file:
                cover_image = Image.open(uploaded_file)
                secret_image = Image.open(secret_file)
                encoded_img = encode_image(cover_image, secret_image)
                buffer = io.BytesIO()
                encoded_img.save(buffer, format="PNG")
                st.download_button("Download Encoded Image 📥", buffer.getvalue(), "encoded_image.png", "image/png")

    elif action == "Decode":
        decode_choice = st.radio("🔍 Choose Decoding Type:", ("Message", "Image"))
        uploaded_file = st.file_uploader("Upload Encoded Image 📷", type=["png", "jpg", "jpeg"])

        if decode_choice == "Message":
            key = st.text_input("Enter Encryption Key 🔑")
            if st.button("Decode 🕵️‍♂️") and uploaded_file and key:
                image = Image.open(uploaded_file)
                aes_cipher = AESCipher(key)
                try:
                    decoded_message = decode_message(image, aes_cipher)
                    st.success("✅ Decoded Message:")
                    st.text_area("Decoded Message 📜:", decoded_message)
                except:
                    st.error("🚨 Decoding failed. Check key or image.")
        elif decode_choice == "Image":
            secret_size = st.slider("🔄 Resize Decoded Image", 50, 500, 200)
            if st.button("Decode 🕵️‍♂️") and uploaded_file:
                encoded_image = Image.open(uploaded_file)
                decoded_img = decode_image(encoded_image, (secret_size, secret_size))
                st.image(decoded_img, caption="Decoded Secret Image 🖼️", use_container_width=True)
                buffer = io.BytesIO()
                decoded_img.save(buffer, format="PNG")
                st.download_button("Download Decoded Image 📥", buffer.getvalue(), "decoded_image.png", "image/png")

    # Noise Resilience Demo
    st.markdown("---")
    st.header("🔬 Noise Resilience Analysis")
    uploaded_stego = st.file_uploader("Upload stego image for noise test", type=["png", "jpg"], key="noise_test")
    sigma_slider = st.slider("Gaussian noise σ", 0.0, 0.05, 0.01, 0.005)
    
    if uploaded_stego is not None:
        img = Image.open(uploaded_stego).convert("RGB")
        noisy_img = add_gaussian_noise(img, sigma_slider)
        psnr_val = compute_psnr(img, noisy_img)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Stego")
            st.image(img, use_container_width=True)
        with col2:
            st.subheader(f"Noisy Stego (σ={sigma_slider:.3f})")
            st.image(noisy_img, use_container_width=True)
        st.success(f"PSNR: **{psnr_val:.2f} dB**")

if __name__ == "__main__":
    main()
