import streamlit as st

st.set_page_config(
    page_title="LLM Sandbox Intro",
)

st.write("# Welcome to LLM Sandbox!")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This is a place to play with Large Language Models (LLMs) for educational purposes only. The demo limited output tokens and is not appropriate for a real-world use.  
    **👈 Select a demo from the sidebar** to see some examples of what LLM can do!
    - LLMs are fine-tuned to be helpful. See how a base model compares to a fine-tuned model that is more helpful.
    - LLM parameters and system prompts can change how LLMs generate responses.
    - Some LLMs are open source and some are fine-tuned for specific purposes (e.g., coding). 
    
    #### See Github for source code and documentation
    - https://github.com/DanTCIM/LLM_Sandbox
"""
)
