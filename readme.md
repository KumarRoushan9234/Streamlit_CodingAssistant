# AI Coding Assistant

An interactive AI-powered coding assistant built using Streamlit and Groq. This tool allows users to ask coding-related questions, select models, and view conversation history.

## Features

- **Model Selection**: Choose from various pre-configured models for AI-driven coding assistance.
- **Conversation History**: View past interactions with the assistant.
- **Clear History**: Clear conversation history while retaining the `conversation.json` file.
- **Flirty Assistant**: The assistant engages in a playful tone while helping with coding questions.

## Requirements

- Python 3.x
- Streamlit
- Groq API Key (Groq service access)
- `dotenv` for managing environment variables

## Setup

### 1. Install Dependencies

First, clone the repository or download the project files.

```bash
git clone https://github.com/yourusername/ai-coding-assistant.git
cd ai-coding-assistant

```

Create a virtual environment and install dependencies:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt

```

### 2. Groq API Key Setup

Create a .env file in the project root and add your Groq API Key:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the Application

To start the application, run the following command:

```bash
streamlit run streamlit_app.py

```

This will start a local Streamlit server, and you can interact with the app in your browser at http://localhost:8501.
