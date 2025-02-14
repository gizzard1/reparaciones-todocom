import streamlit as st
import json
import random
from streamlit_chat import message
import unidecode

# Cargar el archivo JSON con preguntas y respuestas
def load_intents():
    with open("intents.json", "r", encoding="utf-8") as file:
        return json.load(file)

intents = load_intents()

# Inicializar estados en la sesión
if 'contexto_actual' not in st.session_state:
    st.session_state.contexto_actual = None
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []
if 'historial' not in st.session_state:
    st.session_state.historial = []

# Función para encontrar el intent
def buscar_intent(mensaje):
    for intent in intents:
        for pattern in intent['patterns']:
            if pattern.lower() in mensaje.lower():
                return intent
    return None

# Función para manejar el flujo del chatbot
def manejar_mensaje(mensaje):
    mensaje = unidecode.unidecode(mensaje)
    intent = buscar_intent(mensaje)
    
    # Si hay contexto, continuar con la rama correspondiente
    if st.session_state.contexto_actual:
        intent = next((i for i in intents if i['tag'] == st.session_state.contexto_actual), None)
    
    # Si no encuentra un intent, responder con un mensaje predeterminado
    if not intent:
        return "Lo siento, no entiendo tu pregunta."
    
    # Guardar respuesta en la rama actual
    st.session_state.respuestas.append((st.session_state.contexto_actual, mensaje))
    
    # Lógica para manejar las respuestas en base al contexto
    if st.session_state.contexto_actual == "equipo_caida_encendido":
        # Verificar si el mensaje es una respuesta "Sí" o "No"
        if "no" in mensaje.lower():
            # Respuesta para cuando el equipo no enciende
            respuesta = "Lo siento, no podemos ayudar con eso. ¿Hay algo más con lo que pueda ayudarte?"
            st.session_state.contexto_actual = None  # Cambiar contexto a ninguno, ya que el caso está cerrado
        elif "si" in mensaje.lower():
            st.session_state.contexto_actual = "equipo_caida_bisagra"  # Cambiar contexto a ninguno, ya que el caso está cerrado
            respuesta = random.choice(intent["responses"])
        else:
            # Si la respuesta no es clara, pedir aclaración
            respuesta = "Por favor, responde con 'Sí' o 'No'. ¿El equipo enciende?"
    else:
        # Responder con la respuesta aleatoria si no estamos en el contexto de 'equipo_caida'
        respuesta = random.choice(intent["responses"])
        # Actualizar el contexto basado en el intent
        st.session_state.contexto_actual = intent.get('context', [None])[0]

    # Guardar en el historial de la conversación
    st.session_state.historial.append(('bot', respuesta))
    return respuesta

# Inicializar sesión limpia
if 'past' not in st.session_state:
    st.session_state.past = []
if 'generated' not in st.session_state:
    st.session_state.generated = []

# Manejar entrada del usuario
def on_input_change():
    user_input = st.session_state.user_input.strip()
    if user_input:
        st.session_state.historial.append(('user', user_input))
        respuesta = manejar_mensaje(user_input)
        st.session_state.user_input = ""  # Limpiar input
        
        st.session_state.past.append(user_input)
        st.session_state.generated.append({'type': 'normal', 'data': respuesta})

# Botón para limpiar el chat
def on_btn_click():
    st.session_state.past.clear()
    st.session_state.generated.clear()
    st.session_state.user_input = ""


st.title("Reparaciones Todocom")

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
