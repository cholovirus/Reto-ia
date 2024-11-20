import streamlit as st
import requests

# URL del backend FastAPI
with st.sidebar:
    FASTAPI_URL = st.text_input("Ingrese la URL de su API:", placeholder="API")+"/chat/"

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "En que te puedo ayudar?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    try:
        
        response = requests.post(FASTAPI_URL, json={
            "messages": st.session_state.messages,
            "model": "local-model",  
            "temperature": 0.2
        })

        data = response.json()
        if "response" in data:
            assistant_response = data["response"]
        else:
            assistant_response = "Error al obtener la respuesta."

        # Agregar la respuesta del asistente al historial
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.chat_message("assistant").write(assistant_response)

    except Exception as e:
        st.error(f"Error al conectar con el servidor: {e}")
