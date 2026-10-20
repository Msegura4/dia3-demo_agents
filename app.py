import streamlit as st
from llm_agent import Chatagent 

st.set_page_config(page_title="Jarvis")
st.title("La Barbe de Merlin")

# créer l'agent et l'historique si pas encore fait
if "agent" not in st.session_state:
    st.session_state.agent = Chatagent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# création de la barre de chat et ses paramètres
user_input = st.chat_input(
    "Que veux-tu mousaillon ?",
    accept_file=False,
    accept_audio=False
    )

if user_input:
    # afficher les messages utilisateur
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Appel au modèle
    response = st.session_state.agent.ask_llm(user_input)

    # afficher la réponse (sauvegarde dans la liste)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
