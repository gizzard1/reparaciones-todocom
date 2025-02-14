import streamlit as st
import json
import random
from streamlit_chat import message
import unidecode

def load_intents():
    with open("intents.json", "r", encoding="utf-8") as file:
        return json.load(file)

intents = load_intents()

if 'contexto_actual' not in st.session_state:
    st.session_state.contexto_actual = None
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []
if 'historial' not in st.session_state:
    st.session_state.historial = []

def buscar_intent(mensaje):
    for intent in intents:
        for pattern in intent['patterns']:
            if pattern.lower() in mensaje.lower():
                return intent
    return None

def manejar_mensaje(mensaje):
    mensaje = unidecode.unidecode(mensaje)
    intent = buscar_intent(mensaje)
    
    if st.session_state.contexto_actual:
        intent = next((i for i in intents if i['tag'] == st.session_state.contexto_actual), None)
    
    if not intent:
        return "Lo siento, no entiendo tu pregunta."
    
    st.session_state.respuestas.append((st.session_state.contexto_actual, mensaje))
    
    if st.session_state.contexto_actual == "equipo_caida_encendido":
        if "no" in mensaje.lower():
            respuesta = "Lo siento, no podemos ayudar con eso. ¿Hay algo más con lo que pueda ayudarte?"
        elif "si" in mensaje.lower():
            respuesta = random.choice(intent["responses"])
        else:
            respuesta = "Por favor, responde con 'Sí' o 'No'. ¿El equipo enciende?"
    else:
        respuesta = random.choice(intent["responses"])
        st.session_state.contexto_actual = intent.get('context', [None])[0]

    st.session_state.historial.append(('bot', respuesta))
    return respuesta

if 'past' not in st.session_state:
    st.session_state.past = []
if 'generated' not in st.session_state:
    st.session_state.generated = []

def on_input_change():
    user_input = st.session_state.user_input.strip()
    if user_input:
        st.session_state.historial.append(('user', user_input))
        respuesta = manejar_mensaje(user_input)
        
        st.session_state.past.append(user_input)
        st.session_state.generated.append({'type': 'normal', 'data': respuesta})

def on_btn_click():
    st.session_state.past.clear()
    st.session_state.generated.clear()
    st.session_state.user_input = ""


st.title("Reparaciones de computadoras")

chat_placeholder = st.empty()

with chat_placeholder.container():
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True
        )

st.button("Limpiar chat", on_click=on_btn_click)
st.text_input("Escribe aquí:", on_change=on_input_change, key="user_input")
