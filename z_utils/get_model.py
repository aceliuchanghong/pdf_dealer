import os
import threading
from openai import OpenAI
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from minio import Minio
from z_test.test_emb import emb_chunks
from z_test.test_llm import get_result
from pymilvus import MilvusClient

load_dotenv()


class TALK_LLM:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = OpenAI(api_key=os.getenv('API_KEY'), base_url=os.getenv('BASE_URL'))
        return cls._instance


class EMB_LLM:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = OllamaEmbeddings(
                    model=os.getenv('EMB_MODEL'),
                    base_url=os.getenv('EMB_BASE_URL'),
                )
        return cls._instance


class Milvus_Client:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = MilvusClient(uri=os.getenv('milvus_url'))
        return cls._instance


class Minio_Client:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = Minio(
                    os.getenv('minio_endpoint'),
                    access_key=os.getenv('minio_access_key'),
                    secret_key=os.getenv('minio_secret_key'),
                    secure=False
                )
        return cls._instance


if __name__ == '__main__':
    emb_client = EMB_LLM()
    llm_client = TALK_LLM()
    client, user_prompt, Basic_info = llm_client, '我的名字什么?', '我的名字是lawrence'
    print(get_result(client, user_prompt, Basic_info))
    print(emb_chunks(emb_client, [Basic_info]))
