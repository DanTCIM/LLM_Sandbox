import streamlit as st
import os
import openai
from openai import OpenAI

st.set_page_config(page_title="Base and Fine-tuned Model Demo")

st.markdown("# Base and Fine-tuned Model Demo")
st.write(
    "The demo shows OpenAI's GPT series models. Babbage-002 is OpenAI's base model open for a user to fine-tune. GPT-3.5-Turbo is OpenAI's fine-tuned model. Babbage-002 is understood to be smaller than GPT-3 models."
)
st.write("The demo limits maximum of 100 tokens for illustration purposes.")
st.divider()
st.sidebar.header("Ask questions")
st.sidebar.caption(
    "Sample questions represent common sense, math, coding, and reasoning skills."
)

## API key setup
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI()


## Define functions to get responses and completions
def get_response(user_input):
    response = client.completions.create(
        model="babbage-002",  # One of OpenAI's Base model: pre-trained model before fine-tuning
        prompt=user_input,
    )
    return response.choices[0].text.strip()


def get_completion(user_input):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        # the flagship model of this family, supports a 16K context window and is optimized for dialog.
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {"role": "user", "content": user_input},
        ],
        max_tokens=100,
    )
    return completion.choices[0].message.content


# Define a function to display responses for a given prompt
def display_responses(user_prompt):
    st.write("**Prompt input:** " + user_prompt)
    with st.spinner("Generating responses ..."):
        col1, col2 = st.columns(2)
        with col1:
            container = st.container(border=True)
            container.write("**Base model: Babbage-002**")
            # Assuming get_response is a function that fetches the response from the base model
            container.write(get_response(user_prompt))
        with col2:
            container = st.container(border=True)
            container.write("**Fine-tuned model: GPT-3.5-Turbo**")
            # Assuming get_completion is a function that fetches the response from the finetuned model
            container.write(get_completion(user_prompt))


# Use a single block for handling different user prompts
questions = [
    "What is capital of Iowa?",
    "What is square root of 4999?",
    "Provide Python code to perform Cholesky decomposition",
    "My cat was 5 years old two years ago when I adopted. My dog was twice the age at the time. How old is my dog now?",
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
