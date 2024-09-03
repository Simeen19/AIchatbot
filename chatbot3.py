import streamlit as st
from openai import OpenAI  # Replace with actual import if needed
import time

# Access the API key from Streamlit secrets
api_key = st.secrets["OPENAI_KEY"]

# Initialize OpenAI with the API key
client = OpenAI(api_key=api_key)


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

 # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

def make_request_with_retries(prompt, retries=3):
    for _ in range(retries):
        try:
            response = OpenAI.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100
            )
            return response.choices[0].text.strip()
        except OpenAI.error.RateLimitError:
            print("Rate limit exceeded. Retrying in 10 seconds...")
            time.sleep(10)  # Wait for 10 seconds before retrying
    raise Exception("Max retries exceeded")