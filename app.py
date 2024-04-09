import streamlit as st
import os
from dotenv import load_dotenv
from api import ReviewAPI
import time


class ChatAPI:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        self.messages = st.session_state.messages

    def chat_history(self):
        self.messages = st.session_state.messages
        # print(self.messages)
        for message in self.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def update_session_state(self, role, content):
        st.session_state.messages.append({"role": role, "content": content})

    def response_generator(self, prompt):
        response = review_api.chat(prompt)
        print(response)
        for sentence in response.split("\n"):
            yield sentence + "\n"
            time.sleep(0.05)

    def chat_input(self):

        if prompt := st.chat_input("What's up BAITCH?"):
            with st.chat_message("user"):
                st.markdown(prompt)
            self.update_session_state("user", prompt)
            response = None
            with st.chat_message("assistant"):
                response = st.write_stream(self.response_generator(prompt))

            self.update_session_state("assistant", response)

    def init_chat(self):
        st.title("Ask a Question about your Resume")
        self.chat_history()
        self.chat_input()


load_dotenv()
uploaded_file = st.file_uploader("Choose a file", type="pdf")
file_name = "resume.pdf"
folder_name = "./temp"

if uploaded_file:
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    path = os.path.join(folder_name, file_name)

    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())

    review_api = ReviewAPI()
    if st.button("Get Insights"):
        response = review_api.insights()
        st.write(response)

    chat_api = ChatAPI()
    chat_api.init_chat()
