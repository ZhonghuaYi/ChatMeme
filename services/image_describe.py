import requests
import base64
import os
import time
from config.settings import Config
from typing import List
import numpy as np
from openai import OpenAI

class ImageDescribeService:
    def __init__(self, api_key=None, base_url=None, model=None, request_delay=None):
        self.api_key = api_key or Config.IMAGE_DESCRIBE_API_KEY
        self.base_url = base_url or Config.IMAGE_DESCRIBE_BASE_URL
        self.model = model or Config.IMAGE_DESCRIBE_MODEL
        self.local_image_folder = Config.LOCAL_IMAGE_FOLDER
        self.request_delay = float(request_delay or Config.IMAGE_DESCRIBE_REQUEST_DELAY)
        self.last_request_time = 0
        
        self._client = None
        
    @property
    def client(self):
        """懒加载OpenAI客户端"""
        if self._client is None:
            if not self.api_key:
                raise ValueError("图像描述API密钥未设置")
            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return self._client
    
    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
    
    @staticmethod
    def check_image_url_type(image_url: str) -> str:
        """检查图片URL类型"""
        if image_url.startswith("http"):
            return "image_url"
        else:
            return "image_file"
        
    # @staticmethod
    # def normalize_embedding(embedding: List[float]) -> np.ndarray:
    #     """归一化嵌入向量"""
    #     arr = np.array(embedding)
    #     return arr / np.linalg.norm(arr)
    
    # def get_embedding(self, text: str, key: str) -> np.ndarray:
    #     """获取文本嵌入并归一化"""
    #     headers = {"Authorization": f"Bearer {key if key is not None else self.api_key}"}
    #     payload = {
    #         "input": text,
    #         "model": Config.EMBEDDING_MODEL
    #     }
    #     response = requests.post(self.endpoint, json=payload, headers=headers)
    #     response.raise_for_status()
    #     return self.normalize_embedding(response.json()['data'][0]['embedding']) 
    
    def describe_image(self, image_url: str) -> str:
        """描述图片"""
        # 实现速率限制
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.request_delay:
            sleep_time = self.request_delay - time_since_last_request
            print(f"等待 {sleep_time:.2f} 秒以遵守API速率限制...")
            time.sleep(sleep_time)
        
        image_type = self.check_image_url_type(image_url)
        
        if image_type == "image_url":
            image = image_url
            message_image_url = {
                "type": "image_url",
                "image_url": {
                    "url": image,
                    "detail": "high",  
                },
            }
        else:
            image = self.encode_image(image_url)
            message_image_url = {
                "type": "image_url",
                "image_url": {
                    "url": f'data:image/jpeg;base64,{image}',
                    "detail": "high",
                },
            }
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that describes memes."},
            {
                "role": "user",
                "content": [
                    message_image_url,
                    {
                        "type": "text",
                        "text": "图片是一张表情包，你需要根据你对表情包的理解，正确识别当前这张表情包图像的人物、文字，并描述这张表情包的含义。结果用中文描述，在100字以内。",
                    },
                ],
            },
        ]
        
        description = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
        )
        self.last_request_time = time.time()
        return description.choices[0].message.content
    
    
if __name__ == "__main__":
    image_describe = ImageDescribeService()
    print(image_describe.describe_image("data/images/鼓掌gif.gif"))
