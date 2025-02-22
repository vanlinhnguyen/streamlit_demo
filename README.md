# 🚀 Ollama x Streamlit Playground

This project demonstrates how to run and manage models locally using [Ollama](https://ollama.com/) by creating an interactive UI with [Streamlit](https://streamlit.io).

The app has a page for running chat-based models and also one for nultimodal models (_llava and bakllava_) for vision.

## App in Action

![GIF](assets/ollama_streamlit.gif)


## Features

- **Interactive UI**: Utilize Streamlit to create a user-friendly interface.
- **Local Model Execution**: Run your Ollama models locally without the need for external APIs.
- **Real-time Responses**: Get real-time responses from your models directly in the UI.

## Installation

Before running the app, ensure you have Python installed on your machine. Then, clone this repository and install the required packages using pip:

```bash
git clone https://github.com/tonykipkemboi/ollama_streamlit_demos.git
```

```bash
cd ollama_streamlit_demos
```

```bash
pip install -r requirements.txt
```

## Usage

To start the app, run the following command in your terminal:

```bash
streamlit run 01_💬_Chat_Demo.py
```

Navigate to the URL provided by Streamlit in your browser to interact with the app.

**NB: Make sure you have downloaded [Ollama](https://ollama.com/) to your system.**