import streamlit as st
import google.generativeai as genai

# Твой API ключ
MY_API_KEY = "AIzaSyBgRhRW6bjh57dz8neU6uZEyr8R_rovASM"

st.set_page_config(page_title="Stable AI", page_icon="✅")
st.title("🤖 Стабильный ИИ Ассистент")

# Настройка
try:
    genai.configure(api_key=MY_API_KEY)
    # МЫ МЕНЯЕМ МОДЕЛЬ НА ТУ, ЧТО ПОД НОМЕРОМ 21 В ТВОЕМ СПИСКЕ
    # У gemini-pro-latest отдельные лимиты, которые обычно не равны 0
    model = genai.GenerativeModel('gemma-3-4b-it')
except Exception as e:
    st.error(f"Ошибка настройки: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Напиши мне что-нибудь..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Прямой вызов
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Ошибка квоты или доступа")
            st.code(str(e))
            st.warning("Если лимит 0, попробуйте создать НОВЫЙ API-ключ на другой аккаунт Google.")