import streamlit as st
import json
import os
from dotenv import load_dotenv
from groq import Groq

# Initialize Streamlit page configuration
st.set_page_config(page_title="AI Coding Assistant", layout="wide")

# Load environment variables
load_dotenv()

# Initialize Groq
api_key = os.getenv("GROQ_API_KEY")
groq = Groq(api_key=api_key)

# File paths
MODEL_FILE = "data.json"
CONVERSATION_FILE = "conversation.json"

# Global variable to store selected model
selected_model = None

# Function to load the selected model
def load_selected_model():
    global selected_model
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):  # Ensure data is a dictionary
                    selected_model = data.get("id", None)
                else:
                    selected_model = None  # If it's a list or other structure
            except json.JSONDecodeError:
                selected_model = None

# Load model at startup
load_selected_model()

# Function to update chat history
def update_chat_history(user_message, system_response):
    history = []
    
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append({"user": user_message, "assistant": system_response})

    with open(CONVERSATION_FILE, "w") as f:
        json.dump(history, f, indent=4)

# Load the last 5 messages from history
def get_recent_conversation():
    chat_history = []
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, "r") as f:
            try:
                chat_history = json.load(f)
            except json.JSONDecodeError:
                chat_history = []
    
    # Limit the history to the last 5 messages
    return chat_history[-5:]  # Only take the last 5 entries

# Streamlit User Interface

# Fixed Header with Select Model and Delete Conversation Button
st.title("AI Coding Assistant")
col1, col2, col3 = st.columns([2, 7, 1])  # Adjust width ratio
with col1:
    model_option = st.selectbox(
        "Select Model", 
        options=["Select a model", "mixtral-8x7b-32768", "llama-3.3-70b-specdec", "llama-3.3-70b-versatile", 
                 "llama3-8b-8192", "llama-guard-3-8b", "llama3-70b-8192", "llama-3.2-1b-preview", 
                 "whisper-large-v3-turbo", "llama-3.2-3b-preview", 
                 "llama-guard-3-8b", "gemma2-9b-it", "distil-whisper-large-v3-en"]
    )

    if model_option != "Select a model" and model_option != selected_model:
        selected_model = model_option
        with open(MODEL_FILE, "w") as f:
            json.dump({"id": selected_model}, f, indent=4)
        st.success(f"Model '{selected_model}' selected successfully")
        st.rerun()  # Refresh page after model change

with col2:
    if selected_model:
        st.write(f"Selected Model: {selected_model}")  # Show selected model name

with col3:
    if st.button("Delete History"):
        if os.path.exists(CONVERSATION_FILE):
            os.remove(CONVERSATION_FILE)
            st.success("Conversation history cleared.")
            st.rerun()  
        else:
            st.warning("No conversation history to clear.")
            st.rerun()  

# Layout for chat and user input (using columns for positioning)
st.subheader("Chat")

# Form for user input (to add new message)
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Enter your prompt:")
    submit_button = st.form_submit_button(label="Send")

    if submit_button or user_input:  # Check for form submission or user input
        if not selected_model:
            st.error("No model selected. Please choose a model first.")
        elif not user_input:
            st.error("Please provide a prompt.")
        else:
            # Get the recent conversation history (limit to the last 5 messages)
            chat_history = get_recent_conversation()

            messages = [{"role": "system", "content": "You are a coding assistant.Only answer coding question; for anyother question apart from coding reply => 'Kindly ask a Question related to coding.'"}]
            for chat in chat_history:
                messages.append({"role": "user", "content": chat["user"]})
                messages.append({"role": "assistant", "content": chat["assistant"]})

            messages.append({"role": "user", "content": user_input})

            try:
                chat_completion = groq.chat.completions.create(
                    messages=messages,
                    model=selected_model,
                    temperature=0.5,
                    top_p=1,
                    stream=False,
                )

                response_text = chat_completion.choices[0].message.content
                update_chat_history(user_input, response_text)

                # Display the new messages above the input
                with st.container():
                    st.markdown(f'<div class="chat-box"><div class="user-message">User: {user_input}</div><div class="assistant-message">Assistant: {response_text}</div></div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

                
# Container for current and previous chats
chat_container = st.container()

# Show current chat and responses
with chat_container:
    # Border for chat box styling
    st.markdown(""" 
    <style>
     .chat-box {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        background-color: #f2f2f2;  /* Light Gray background for the entire chat box */
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #738bd9;  /* Light blue background for user messages */
        color: #121c36;  /* Dark blue text color */
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .assistant-message {
        background-color: #67c781;  /* Light green background for assistant messages */
        color: #242b23;  /* Dark green text color */
        padding: 5px;
        border-radius: 5px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Show previous conversation if checkbox is selected
    conversation_expanded = st.checkbox("Expand/Collapse conversation history", value=True)
    
    if conversation_expanded:
        if os.path.exists(CONVERSATION_FILE):
            with open(CONVERSATION_FILE, "r") as f:
                try:
                    history = json.load(f)
                    for entry in history:
                        # Display system (assistant) messages on the right and user input on the left
                        with st.container():
                            st.markdown(f'<div class="chat-box"><div class="user-message">User: {entry["user"]}</div><div class="assistant-message">Assistant: {entry["assistant"]}</div></div>', unsafe_allow_html=True)
                except json.JSONDecodeError:
                    st.write("No conversation history.")
    else:
        st.write("Conversation history is collapsed.")
