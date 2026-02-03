import streamlit as st
from google.cloud import dialogflow_v2 as dialogflow
import os

# ------------------------
# Setup Google credentials
# ------------------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

st.set_page_config(page_title="Google Chatbot", page_icon="🤖")
st.title("🤖 Google Dialogflow Chatbot")

# Load secrets
PROJECT_ID = st.secrets["PROJECT_ID"]
SESSION_ID = st.secrets.get("SESSION_ID", "12345")
LANGUAGE_CODE = "en"

# Create Dialogflow session client
session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID, SESSION_ID)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Dialogflow request
    text_input = dialogflow.TextInput(text=user_input, language_code=LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    # Get bot reply
    bot_reply = response.query_result.fulfillment_text
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
