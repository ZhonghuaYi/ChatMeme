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
    
    @staticmethod
    def normalize_embedding(embedding: List[float]) -> np.ndarray:
        """归一化嵌入向量"""
        arr = np.array(embedding)
        return arr / np.linalg.norm(arr)
    
    def get_embedding(self, text: str) -> np.ndarray:
        # """获取文本嵌入并归一化"""
        
        if self.api_key is None:
            raise ValueError("Embedding API密钥未设置")
        
        if self.base_url is None:
            raise ValueError("Embedding API基础URL未设置")
        
        if self.model is None:
            raise ValueError("Embedding API模型未设置")
        
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding