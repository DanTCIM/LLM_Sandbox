import streamlit as st
import os
import openai
from openai import OpenAI

token_limits = 150

st.set_page_config(page_title="Model Parameters and Prompting")

st.markdown("# Model Parameters and Prompting")
st.write(
    "The demo is based on GPT-3.5-Turbo, OpenAI's fine-tuned model. The base setup uses temperature of 0.75 and a system instruction *you are a helpful assistant*."
)
st.write(f"The demo limits maximum of {token_limits} tokens for illustration purposes.")
st.divider()
st.sidebar.header("Customize model")

## API key setup
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI()

# Define variables for inputs
default_system_message = "You are a helpful assistant."

user_system_message = st.sidebar.text_input(
    "System Instruction", "You are a helpful assistant."
)
user_temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 1.0, 0.25)


# Define a function to get completion based on user input
def get_completion(user_input, system_message=default_system_message, temperature=0.75):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        # the flagship model of this family, supports a 16K context window and is optimized for dialog.
        messages=[
            {
                "role": "system",
                "content": system_message,
            },
            {"role": "user", "content": user_input},
        ],
        max_tokens=token_limits,
        temperature=temperature,
    )
    return completion.choices[0].message.content


# Define a function to display responses for a given prompt
def display_responses(user_prompt):
    st.write("**Prompt input:** " + user_prompt)
    with st.spinner("Generating responses ..."):
        col1, col2 = st.columns(2)
        with col1:
            container = st.container(border=True)
            container.write("**Base Setup**")
            container.write(get_completion(user_prompt))
        with col2:
            container = st.container(border=True)
            container.write("**Custom Setup**")
            container.write(
                get_completion(
                    user_prompt,
                    system_message=user_system_message,
                    temperature=user_temperature,
                )
            )


# Use a single block for handling different user prompts
questions = [
    "What is capital of Iowa?",
    "Explain CLO asset class",
    "Brainstorm how LLMs can help actuarial students get more efficient at work",
    "Explain bootstrapping with simple numerical examples",
]

# Generate buttons for each question
for question in questions:
    if st.sidebar.button(question):
        display_responses(question)

# Handling custom user input
if user_prompt := st.sidebar.chat_input(
    "Enter your question:"
):  ## text_input vs. chat_input
    # if user_prompt:
    display_responses(user_prompt)
