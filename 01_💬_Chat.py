import ollama
import streamlit as st
from openai import OpenAI
from utilities.icon import page_icon
import time
from code_editor import code_editor

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
    st.title("Learn-it-all: education for all")

    st.subheader("Tutors", divider="red", anchor=False)

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

    # List of code problems
    code_problems = [
        """# Problem 1: Fix the syntax error
    def greet(name):
        return f"Hello, {name}!"

    print(greet("World"))
    """,
        """# Problem 2: Implement a function to add two numbers
    def add(a, b):
        # Your code here
        pass

    print(add(2, 3))  # Expected output: 5
    """,
        """# Problem 3: Find the maximum number in a list
    def find_max(numbers):
        # Your code here
        pass

    print(find_max([1, 5, 3, 9, 2]))  # Expected output: 9
    """,
    ]

    # Initialize session state to track the current problem index
    if "current_problem_index" not in st.session_state:
        st.session_state.current_problem_index = 0

    st.subheader("Playground", divider="red", anchor=False)
    current_problem = code_problems[st.session_state.current_problem_index]
    code_editor(current_problem, height=300, lang="python")


    # Navigation buttons
    col1, col2, col3 = st.columns(3)  # Create three columns for the buttons

    with col1:
        if st.button("Previous"):
            st.session_state.current_problem_index = (st.session_state.current_problem_index - 1) % len(code_problems)
            st.experimental_rerun()  # Refresh the app to show the previous problem

    with col2:
        if st.button("Submit"):
            # Prepare the prompt for the LLM
            prompt = f"Given the original code: ```{current_problem}```, please check if the code is correct and provide suggestions for improvement if needed. Limit your answer to 100 words."

            # Send the prompt to the LLM
            try:
                with st.spinner("Checking your code..."):
                    stream = client.chat.completions.create(
                        model=selected_model,
                        messages=[{"role": "user", "content": prompt}],
                        stream=True,
                    )
                    # Stream the response
                    response = st.write_stream(stream)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(e, icon="⛔️")

    with col3:
        if st.button("Next"):
            st.session_state.current_problem_index = (st.session_state.current_problem_index + 1) % len(code_problems)
            st.experimental_rerun()  # Refresh the app to show the next problem


    st.subheader("Chat with tutor", divider="red", anchor=False)
    message_container = st.container(height=500, border=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "😎"
        with message_container.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter a prompt here..."):
        if prompt.startswith("[tutor]"):
            full_prompt = f"Given the code: ```{code_problems[st.session_state.current_problem_index]}```, {prompt}. Limit your answer in text only and 100 words."
        else:
            full_prompt = prompt
        try:
            st.session_state.messages.append({"role": "user", "content": full_prompt})

            message_container.chat_message("user", avatar="😎").markdown(prompt)

            with message_container.chat_message("assistant", avatar="🤖"):
                with st.spinner("model working..."):
                    stream = client.chat.completions.create(
                        model=selected_model,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                # stream response
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(e, icon="⛔️")

if __name__ == "__main__":
    main()