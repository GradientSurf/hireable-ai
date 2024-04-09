import streamlit as st
import os
from dotenv import load_dotenv
from api import ReviewAPI
import time


class ChatAPI:
    def __init__(self, chatbox_container):
        self.chatbox_container = chatbox_container
        if "messages" not in st.session_state:
            st.session_state.messages = []
        self.messages = st.session_state.messages

    def chat_history(self):
        self.messages = st.session_state.messages
        for message in self.messages:
            with self.chatbox_container.chat_message(message["role"]):
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
        if prompt := st.chat_input("Ask a question"):
            self.update_session_state("user", prompt)
            with self.chatbox_container.chat_message("user"):
                st.markdown(prompt)
            response = None
            with self.chatbox_container.chat_message("assistant"):
                response = st.write_stream(self.response_generator(prompt))

            self.update_session_state("assistant", response)

    def init_chat(self):
        self.chat_history()
        self.chat_input()


load_dotenv()
uploaded_file = st.file_uploader("Choose a file", type="pdf")
file_name = "resume.pdf"
folder_name = "./temp"

insights_tab, chat_tab = st.tabs(["Insights", "Chat"])

if uploaded_file:
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    path = os.path.join(folder_name, file_name)

    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    with insights_tab:
        insights_tab.subheader("Get Insights from your Resume")
        review_api = ReviewAPI()
        if st.button("Get Insights"):
            response = review_api.insights()
            st.write(response)
    
    with chat_tab:
        chat_tab.subheader("Ask a Question about your Resume")
        chatbox = st.container(height=400)

        chat_api = ChatAPI(chatbox_container=chatbox)
        chat_api.init_chat()
