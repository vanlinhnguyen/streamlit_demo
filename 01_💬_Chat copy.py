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


def get_prompts():
    # Define your predefined list of prompts and answers
    prompts = [
        {"text": "Hello, what do you want to learn today?", "code": ""},
        {
            "text": "Alright, let's begin with some simple looping. Assuming I have a list",
            "code": """#objects = ["apple", "orange", "banana"]
for ... in objects:
    print(f"I love {fluid}")""",
        },
    ]

    answers = [
        {"text": "Let's learn some Python basics. Please recommend where to start.", "code": ""},
        {
            "text": "Okay, seems like something I know.",
            "code": """#objects = ["apple", "orange", "banana"]
for fruit in objects:
    print(f"I love {fruit}")""",
        },
    ]

    return prompts, answers


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

    prompts, answers = get_prompts()

    # Initialize session state for code_snippet if it doesn't exist
    if "code_snippet" not in st.session_state:
        st.session_state.code_snippet = ""

    # Initialize session state for the current prompt index
    if "current_prompt_index" not in st.session_state:
        st.session_state.current_prompt_index = 0

    # Add a text area for code input
    code_snippet = st.text_area("Playgrounds", value=st.session_state.code_snippet, height=200)

    # Add a submit button
    if st.button("Submit"):
        if code_snippet:
            # Display the submitted code snippet
            st.markdown("### Submitted Code Snippet:")
            st.code(code_snippet, language="python")

            # Display text instructions below the code snippet
            st.markdown("### Instructions:")
            st.markdown(
                """
            Here are some instructions to help you understand the code:
            1. **Understand the syntax**: Make sure you understand the syntax used in the code.
            2. **Test the code**: Run the code to see if it works as expected.
            3. **Debug if necessary**: If there are errors, try to debug and fix them.
            4. **Experiment**: Modify the code to see how it behaves with different inputs.
            """
            )
        else:
            st.warning("Please enter a code snippet before submitting.", icon="⚠️")

    message_container = st.container(height=500, border=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Now you can use message_container in your format_and_append_message function
    if st.session_state.current_prompt_index < len(prompts):
        print("Linh: ", st.session_state.current_prompt_index)
        prompt = prompts[st.session_state.current_prompt_index]
        answer = answers[st.session_state.current_prompt_index]

        format_and_append_message(message_container, prompt["text"], prompt["code"])
        time.sleep(3)
        format_and_append_message(message_container, answer["text"], answer["code"])
        time.sleep(3)

        # Update the code snippet in session state
        st.session_state.code_snippet = answer["code"]
        st.session_state.current_prompt_index += 1

        # Use st.experimental_rerun() to refresh the page and display the next prompt
        st.experimental_rerun()


if __name__ == "__main__":
    main()