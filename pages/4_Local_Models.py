import streamlit as st
import os
import openai
from openai import OpenAI

# import ollama

token_limits = 200

st.set_page_config(page_title="Model Types")

st.markdown("# Local Models: NOT INTENDED TO WORK ON WEB")
st.write(
    "The demo compares OpenAI's closed model GPT-3.5-Turbo and other open-source local models that do not need a web connection."
)
st.write(
    """
- Gemma 7B (Google's open-source model) 
- Mistral 7B (Mistral's open-source model)
- Code Llama 7B Python (Fine-tuned from Llama 2, excels at coding)
- Solar 10.7 B instruct  
"""
)

MODEL_NAME = st.selectbox(
    "Select local open-source model",
    [
        "Gemma 7b",
        "Mistral 7b",
        "Code Llama 7b Python",
        "Solar 10.7b",
    ],
)
st.write(f"The demo limits maximum of {token_limits} tokens for illustration purposes.")
st.divider()
st.sidebar.header("Customize model")

## API key setup
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client1 = OpenAI()
client2 = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required, but unused
)
MODEL_ID1 = "gpt-3.5-turbo-0125"

# Define a dictionary to map the MODEL_NAME to MODEL_ID
model_name_to_id = {
    "Gemma 7b": "gemma:latest",
    "Mistral 7b": "mistral:instruct",
    "Code Llama 7b Python": "codellama:7b-python",
    "Solar 10.7b": "solar:10.7b-instruct-v1-q5_K_M",
}
# Use the MODEL_NAME to get the corresponding MODEL_ID from the dictionary
MODEL_ID2 = model_name_to_id[MODEL_NAME]


# Define a function to get completion based on user input
def get_completion(client, model_name, user_input):
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
        max_tokens=token_limits,
    )
    return completion.choices[0].message.content


# Define a function to display responses for a given prompt
def display_responses(user_prompt):
    st.write("**Prompt input:** " + user_prompt)
    with st.spinner("Generating responses ..."):
        col1, col2 = st.columns(2)
        with col1:
            container = st.container(border=True)
            container.write("**OpenAI GPT-3.5-Turbo**")
            container.write(get_completion(client1, MODEL_ID1, user_prompt))
        with col2:
            container = st.container(border=True)
            container.write(f"**{MODEL_NAME}**")
            container.write(get_completion(client2, MODEL_ID2, user_prompt))


# Use a single block for handling different user prompts
questions = [
    "My cat was 5 years old two years ago when I adopted. My dog was twice the age at the time. How old is my dog now?",
    "Explain Principal Component Analysis with simple numerical examples",
    "Write a Python code to perform Principal Component Analysis",
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
