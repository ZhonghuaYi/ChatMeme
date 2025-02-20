import requests
from config.settings import Config
from typing import List
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.api_key = Config.SILICON_API_KEY
        self.endpoint = "https://api.siliconflow.cn/v1/embeddings"
        
    @staticmethod
    def normalize_embedding(embedding: List[float]) -> np.ndarray:
        """归一化嵌入向量"""
        arr = np.array(embedding)
        return arr / np.linalg.norm(arr)
    
    def get_embedding(self, text: str, key: str) -> np.ndarray:
        """获取文本嵌入并归一化"""
        headers = {"Authorization": f"Bearer {key if key is not None else self.api_key}"}
        payload = {
            "input": text,
            "model": Config.EMBEDDING_MODEL
        }
        response = requests.post(self.endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return self.normalize_embedding(response.json()['data'][0]['embedding']) 