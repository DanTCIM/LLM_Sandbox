import streamlit as st
import os
import openai
from openai import OpenAI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

token_limits = 2000

st.set_page_config(page_title="Model Test")

st.markdown("# Model Test")
st.write("The demo is in a test mode.")
st.write(
    """
Llama-2 chat (7B and 70B) and Code Llama are fine tuned from Meta's Llama 2 base model. Code Llama is optimized for coding.  
Mixtral-8x7b is an open-source mixture-of-experts (MOE) model by Mistral.
"""
)

MODEL_NAME = st.selectbox(
    "Select open-source model",
    [
        "Llama-2-7b-chat",
        "Llama-2-70b-chat",
        "CodeLlama-34b-Instruct",
        "Mixtral-8x7b",
    ],
)

st.write(
    f"The demo limits maximum of {token_limits/10} tokens for illustration purposes."
)
st.divider()
st.sidebar.header("Ask questions")

## API key setup
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client1 = OpenAI()
client2 = OpenAI(
    api_key=st.secrets["DEEPINFRA_API_KEY"],
    base_url="https://api.deepinfra.com/v1/openai",
)
client3 = MistralClient(api_key=st.secrets["MISTRAL_API_KEY"])

MODEL_ID1 = "gpt-3.5-turbo-0125"

# Define a dictionary to map the MODEL_NAME to MODEL_ID
model_name_to_id = {
    "Llama-2-70b-chat": "meta-llama/Llama-2-70b-chat-hf",
    "Llama-2-7b-chat": "meta-llama/Llama-2-7b-chat-hf",
    "CodeLlama-34b-Instruct": "codellama/CodeLlama-34b-Instruct-hf",
    "Mixtral-8x7b": "open-mixtral-8x7b",
}
# Use the MODEL_NAME to get the corresponding MODEL_ID from the dictionary
MODEL_ID2 = model_name_to_id[MODEL_NAME]


# Define a function to get completion based on user input
def get_completion(client, model_name, user_input):
    if model_name == "open-mixtral-8x7b":
        chat_response = client3.chat(
            model="mistral-large-latest",
            messages=[
                ChatMessage(role="system", content="You are a helpful assistant."),
                ChatMessage(role="user", content=user_input),
            ],
            max_tokens=token_limits,
        )
        return chat_response.choices[0].message.content

    else:
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
