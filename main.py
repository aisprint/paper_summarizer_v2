from dotenv import load_dotenv
import os

import streamlit as st

from PyPDF2 import PdfReader

from anthropic import Anthropic
from openai import OpenAI

import numpy as np

import random
import time
from datetime import datetime

st.set_page_config("Paper Summarizer", page_icon=":memo:")

# Custom styles for the author name and updated date
st.markdown("""
<style>
.title-style {
    font-size: 50px;
    font-weight: bold;
    color: #5D00FF;
    text-align: center;
    margin-top: 30px;
}
.author-style {
    font-size: 20px;
    font-weight: bold;
    color: #D4BCFF;
    text-align: center;
    margin-bottom: 5px;
}
.update-date-style {
    font-size: 16px;
    color: #555;
    text-align: center;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# Display the stylish title
st.markdown('<div class="title-style">🧑‍🎓Paper Summarizer📜</div>', unsafe_allow_html=True)

# Display author and the updated date
current_date = datetime.now().strftime("%m/%d/%Y")
st.markdown('<div class="author-style">By Mamoru</div>', unsafe_allow_html=True)
st.markdown(f'<div class="update-date-style">Last Updated: {current_date}</div>', unsafe_allow_html=True)



# Initialize or update the session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar for API keys
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
st.sidebar.markdown(
    "[How to get OpenAI API key?](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)", 
    unsafe_allow_html=True
)

anthropic_api_key = st.sidebar.text_input('Anthropic API Key', type='password')
st.sidebar.markdown(
    "[How to get Anthropic API key?](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)", 
    unsafe_allow_html=True
)

# Function to add conversation to history with formatted title
def add_to_history(user_input, response, file_name):
    now = datetime.now()
    formatted_date = now.strftime("%m/%d/%Y %H:%M:%S")
    title = f"{formatted_date} & {file_name}"
    st.session_state.history.append({"title": title, "user_input": user_input, "response": response})

client_openai = OpenAI(api_key=openai_api_key)
client = Anthropic(api_key=anthropic_api_key)

# File uploader
# File uploader and PDF reading
uploaded_file = st.file_uploader("Pleaes upload a PDF", type="pdf")
text = ""
file_name = ""
if uploaded_file is not None:
    with st.spinner('Extracting contents.....🤖💤'):
        pdf_reader = PdfReader(uploaded_file)
        file_name = uploaded_file.name  # Get the file name
        for page in pdf_reader.pages:
            text += page.extract_text()

# Display extracted text
if text:
    st.subheader("Extract PDF contents")
    st.text_area("", value=text, height=300)


#Define system prompt
with open("./system_prompt.txt","r") as f:
    system_prompt = f.read()

main_prompt = "Here is a academic paper: <paper>{}</paper>"


# Generate response
# OpenAI
def generate_response_openai(prompt, selected_model, temperature, max_tokens):
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        return
    full_prompt = f"{system_prompt}\n{prompt}"
    completion = client_openai.chat.completions.create(
    model=selected_model,
    temperature = temperature,
    max_tokens=max_tokens,
    messages=[{"role": "user", "content": full_prompt}],
    stream=False,
    )
    response = completion.choices[0].message.content
    return response

# Anthropic
def generate_response_anthropic(prompt, selected_model, temperature, max_tokens):
    if not anthropic_api_key.startswith('sk-'):
        st.warning('Please enter your Anthropic API key!', icon='⚠')
    if submitted and anthropic_api_key.startswith('sk-'):
        response = client.messages.create(
        system = system_prompt,
        max_tokens=max_tokens,
        model=selected_model,
        temperature=temperature,
        messages=[
            {"role":"user", "content": prompt}
        ]
    ) 
    return response.content[0].text

# CSS to inject custom styles in the Streamlit app
css_style = """
<style>
    .stCodeBlock {
        white-space: pre-wrap !important;
    }
</style>
"""

st.markdown(css_style, unsafe_allow_html=True)

# Select model and submit button
models = [
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "gpt-3.5-turbo",
    "gpt-4-turbo",
    "claude-3-opus-20240229",
]

with st.form('my_form'):
    text_input = st.text_area('Enter prompt:(You can leave it as is)', 'Here is an academic paper.')
    paper_placeholder = ': <paper>{}</paper>'
    Paper_contents = paper_placeholder.format(text)
    submitted = st.form_submit_button('Submit')
    if submitted:
        input_text = f"{text_input}\n{Paper_contents}"
        selected_model = st.selectbox('Choose a model:', models)
        temperature = st.slider("Set Temperature (0-1.0):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        max_tokens = st.number_input("Set Max Tokens(1-4000):", min_value=1, max_value=4000, value=2000)
        with st.spinner('Summarizing.....🤖💤'):
            if selected_model.startswith('gpt'):
                response_text = generate_response_openai(input_text, selected_model, temperature, max_tokens)
            else:
                response_text = generate_response_anthropic(input_text, selected_model, temperature, max_tokens)
            if response_text:
                    st.code(response_text, language="text")
                    add_to_history(input_text, response_text, file_name)

# Display conversation history in the main window
st.subheader("Conversation History")
for i, conversation in enumerate(reversed(st.session_state.history)):
    with st.expander(f"{conversation['title']}"):
        st.write("Response:")
        st.code(conversation['response'], language="text")
