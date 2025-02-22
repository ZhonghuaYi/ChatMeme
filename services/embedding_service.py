import requests
from config.settings import Config
from typing import List
import numpy as np
from openai import OpenAI
class EmbeddingService:
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self._client = None
    
    @property
    def client(self):
        """加载OpenAI客户端"""
        if self._client is None:
            if not self.api_key:
                raise ValueError("Embedding API密钥未设置")
            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return self._client
    
    @staticmethod
    def normalize_embedding(embedding: List[float]) -> np.ndarray:
        """归一化嵌入向量"""
        arr = np.array(embedding)
        return arr / np.linalg.norm(arr)
    
    def get_embedding(self, text: str) -> np.ndarray:
        # """获取文本嵌入并归一化"""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding