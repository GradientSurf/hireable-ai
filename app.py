import streamlit as st
import os
from dotenv import load_dotenv, set_key, find_dotenv
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


def update_api_key(api_key):
    # dotenv_file = find_dotenv()
    # set_key(dotenv_file, "GEMINI_API_KEY", api_key)
    st.secrets["GEMINI_API_KEY"] = api_key
    st.write(os.environ["GEMINI_API_KEY"] == st.secrets["GEMINI_API_KEY"])
    # load_dotenv()

file_name = "resume.pdf"
folder_name = "./temp"

input_tab, insights_tab, chat_tab = st.tabs(["Inputs", "Insights", "Chat"])

condition_job_desc = False
condition_file_upload = False


with input_tab:
    if api_key := st.text_input("Enter your GEMINI_API_KEY"):
        update_api_key(api_key=api_key)
    if uploaded_file := st.file_uploader("Choose a file", type="pdf"):
        condition_file_upload = True
    if job_description := st.text_area("Enter the JD of the Job you're applying to."):
        condition_job_desc = True
    

if uploaded_file:
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    path = os.path.join(folder_name, file_name)

    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    with insights_tab:
        insights_tab.subheader("Get Insights from your Resume")
        if condition_job_desc:
            review_api = ReviewAPI(job_description=job_description)
            if st.button("Get Insights"):
                response = review_api.insights()
                st.write(response)
    
    with chat_tab:
        chat_tab.subheader("Ask a Question about your Resume")
        chatbox = st.container(height=400)

        chat_api = ChatAPI(chatbox_container=chatbox)
        chat_api.init_chat()
