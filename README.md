# Daily Journal App

![DALL·E 2023-10-22 09 46 59 - Vector design of a cyan geometric feather placed centrally on a white backdrop  The word 'JournAI' is displayed above the feather in a clean, minimali](https://github.com/CreeperBeatz/JournAI/assets/9784161/dc782b29-124b-4cd0-ae80-644339c90a03)


## Introduction

The Daily Journal App allows you to maintain a daily journal by answering a set of customizable questions. At the end of each week, the answers are processed by GPT-3 to provide you with a summarized insight into your week.

## Features

- **User Authentication**: Sign-up and login functionality.
- **Customizable Questions**: Add or remove questions that you'd like to answer each day.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Vector Database**: docarray (SQLite)
- **LLM Model**: GPT-3.5 

## Getting Started

### Prerequisites

- Python 3.x
- OpenAI GPT-3 API key

### Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/CreeperBeatz/JournAI.git
    ```

2. **Navigate to the project directory**
    ```bash
    cd JournAI
    ```

3. **Activate a Python Virtual Environment**

    I recommend doing that in a Python Virtual Environment. You can create and
    activate one by typing:
    ```bash
   python -m venv .venv
   ```
   Activate the Venv
    ```bash
   .venv\Scripts\activate.bat
   ```
   
4. **Install requirements**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the config file**

    Rename `config_sample.yaml` to `config.yaml` and update it with your GPT-3 API key.

    ```bash
    openai:
        token: your_gpt3_api_key_here
    ```
   
    For development purposes, a default user (admin:admin) is appended by default.
    If you're setting up the app for production, DELETE the default user from the example.

6. **Run the app**

    Use Streamlit to run the app.
    ```bash
    streamlit run app.py
    ```

    Open the app in your browser at `http://localhost:8501/`.
    The app automatically creates all persistent storage needed.
