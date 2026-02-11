import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="English AI Tutor", page_icon="🇬🇧")

# Sidebar untuk API Key dan Pengaturan
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.info("AI ini diset khusus untuk menjawab dalam Bahasa Inggris.")

# --- SYSTEM PROMPT ---
# Instruksi ini memastikan AI selalu menjawab dalam Bahasa Inggris
SYSTEM_INSTRUCTION = "You are a helpful English assistant. Always respond in English. If the user asks in another language, translate your answer to English and provide a brief explanation if necessary."

if api_key:
    genai.configure(api_key=api_key)
    
    # Inisialisasi model dengan instruksi sistem
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("🇬🇧 English AI Assistant")

    # Tampilkan chat yang sudah ada
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Logika Chat
    if prompt := st.chat_input("Type something in English..."):
        # Simpan pesan user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Respon AI
        with st.chat_message("assistant"):
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("Please enter your API Key in the sidebar to start.")
