import ollama
import streamlit as st
from openai import OpenAI
from utilities.icon import page_icon
import time

st.set_page_config(
    page_title="Learn-it-all: education for all",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def extract_model_names(models_info: list) -> tuple:
    """
    Extracts the model names from the models information.

    :param models_info: A dictionary containing the models' information.

    Return:
        A tuple containing the model names.
    """
    print(models_info)
    return tuple(model["model"] for model in models_info["models"])

def format_and_append_message(message_container, prompt_text, prompt_code):
    """
    Formats the given text and code snippets with appropriate Markdown syntax and appends them to the session state messages.

    Args:
        prompt_text (str): The text of the prompt.
        prompt_code (str): The Python code snippet from the prompt.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Append formatted text
    message_text = f"""{prompt_text}"""
    avatar = "🤖"  # Default to assistant role
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            avatar = "😎"  # Change to user role if there's a preceding user message
            break

    st.session_state.messages.append({"role": "user", "content": message_text})
    with message_container.chat_message("user", avatar=avatar):
        st.markdown(message_text)

    # Append formatted code snippet if it exists
    if prompt_code:
        message_code = f"```python\n{prompt_code}\n```"
        with message_container.chat_message("assistant", avatar="🤖"):
            st.markdown(message_code)

def main():
    """
    The main function that runs the application.
    """

    page_icon("💬")
    st.subheader("Learn-it-all: education for all", divider="red", anchor=False)

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    )

    models_info = ollama.list()
    available_models = extract_model_names(models_info)

    if available_models:
        selected_model = st.selectbox(
            "Pick a model available locally on your system ↓", available_models
        )

    else:
        st.warning("You have not pulled any model from Ollama yet!", icon="⚠️")
        if st.button("Go to settings to download a model"):
            st.page_switch("pages/03_⚙️_Settings.py")

    message_container = st.container(height=500, border=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # for message in st.session_state.messages:
    #     avatar = "🤖" if message["role"] == "assistant" else "😎"
    #     with message_container.chat_message(message["role"], avatar=avatar):
    #         st.markdown(message["content"])

    # if prompt := st.chat_input("Enter a prompt here..."):
    #     try:
    #         st.session_state.messages.append(
    #             {"role": "user", "content": prompt})

    #         message_container.chat_message("user", avatar="😎").markdown(prompt)

    #         with message_container.chat_message("assistant", avatar="🤖"):
    #             with st.spinner("model working..."):
    #                 stream = client.chat.completions.create(
    #                     model=selected_model,
    #                     messages=[
    #                         {"role": m["role"], "content": m["content"]}
    #                         for m in st.session_state.messages
    #                     ],
    #                     stream=True,
    #                 )
    #             # stream response
    #             response = st.write_stream(stream)
    #         st.session_state.messages.append(
    #             {"role": "assistant", "content": response})

    #     except Exception as e:
    #         st.error(e, icon="⛔️")

    # Define your predefined list of prompts and answers
    prompts = [
        {"text": "Hello, what do you want to learn today?", "code": ''''''},
        {"text": "Alright, let begin with some  simple looping. Assuming I have a list", "code": ''''#objects = ["apple",  "orange", "banana"]
        for ... in objects:
            print(f"I love {fluid}")'''},
    ]

    answers = [
        {"text": "Let learn some Python basis. Please recommend where to start.", "code": ''''''},
        {"text": "Okay, seem something I know.", "code": '''#objects = ["apple",  "orange", "banana"]
        for fruid in objects:
            print(f"I love {fruid}")'''},
    ]

    # Now you can use message_container in your format_and_append_message function
    for i, prompt in enumerate(prompts):
        format_and_append_message(message_container, prompt["text"], prompt["code"])
        time.sleep(3)
        format_and_append_message(message_container, answers[i]["text"], answers[i]["code"])
        time.sleep(3)


if __name__ == "__main__":
    main()
