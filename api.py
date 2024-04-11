from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
import os
import json


class ReviewAPI:
    def __init__(self, job_description):
        self.config = Utils().load_config()
        Settings.embed_model = GeminiEmbedding(
            model_name=self.config["embedding_model"],
            api_key=os.getenv("GEMINI_API_KEY"),
        )
        Settings.llm = Gemini(api_key=os.getenv("GEMINI_API_KEY"), temperature=0.1)

        documents = SimpleDirectoryReader(self.config["temp_dir_path"]).load_data()
        index = VectorStoreIndex.from_documents(documents)

        self.query_engine = index.as_query_engine()
        self.chat_engine = index.as_chat_engine(chat_mode="context")

        self._insights_prompt = self.config["insights_prompt"]
        self._chat_prompt_template = self.config["chat_prompt_template"]

        self.jd = job_description

    def insights(self):
        response = self.query_engine.query(self._insights_prompt.format(job_description=self.jd))
        return response.response

    def chat(self, user_query):
        response = self.chat_engine.chat(
            self._chat_prompt_template.format(job_description=self.jd, user_query=user_query)
        )
        return response.response


class Utils:
    def __init__(self) -> None:
        pass

    def load_config(self):
        f = open("config.json")
        config = json.load(f)
        f.close()
        return config
