import os
import numpy as np
import pickle
from typing import Optional, List, Dict
from openai import OpenAI
from rich import print
from config.settings import Config
from services.embedding_service import EmbeddingService
from services.image_description_database import ImageDescriptionDatabase
# class ImageSearch:
#     def __init__(self):
#         self.embedding_service = EmbeddingService()
#         self.image_data = self._load_image_embeddings()
    
#     def _load_image_embeddings(self) -> List[Dict]:
#         """加载或生成图片嵌入缓存"""
#         # 尝试加载缓存
#         if os.path.exists(Config.CACHE_FILE):
#             try:
#                 with open(Config.CACHE_FILE, 'rb') as f:
#                     return pickle.load(f)
#             except (pickle.UnpicklingError, EOFError):
#                 print("缓存文件损坏，重新生成...")
        
#         # 生成新缓存
#         image_files = self._get_image_files()
#         embeddings = self._generate_embeddings(image_files)
        
#         # 保存缓存
#         with open(Config.CACHE_FILE, 'wb') as f:
#             pickle.dump(embeddings, f)
            
#         return embeddings
        
#     def _get_image_files(self) -> List[str]:
#         """获取图片文件名列表（不含扩展名）"""
#         if not os.path.exists(Config.IMAGE_DIR):
#             os.makedirs(Config.IMAGE_DIR, exist_ok=True)
            
#         return [
#             os.path.splitext(f)[0]
#             for f in os.listdir(Config.IMAGE_DIR)
#             if f.lower().endswith('.png')
#         ]
    
#     def _generate_embeddings(self, filenames: List[str]) -> List[Dict]:
#         """批量生成文件名嵌入"""
#         embeddings = []
#         for filename in filenames:
#             try:
#                 embedding = self.embedding_service.get_embedding(filename, api_key = Config.SILICON_API_KEY)
#                 embeddings.append({
#                     "filename": f"{filename}.png",
#                     "embedding": embedding
#                 })
#             except Exception as e:
#                 print(f"生成嵌入失败 [{filename}]: {str(e)}")
#         return embeddings
    
#     def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
#         """余弦相似度计算"""
#         return np.dot(a, b)
    
#     def search(self, query: str, top_k: int = 5, api_key: str = None) -> List[str]:
#         """语义搜索最匹配的图片"""
#         try:
#             query_embedding = self.embedding_service.get_embedding(query, api_key)
#         except Exception as e:
#             print(f"查询嵌入生成失败: {str(e)}")
#             return []
        
#         similarities = [
#             (img["filename"], self._cosine_similarity(query_embedding, img["embedding"]))
#             for img in self.image_data
#         ]
        
#         if not similarities:
#             return []
            
#         # 按相似度降序排序并返回前top_k个结果
#         sorted_items = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
#         return [os.path.join(Config.IMAGE_DIR, item[0]) for item in sorted_items] 


class ImageSearch:
    def __init__(self, 
                 image_describe_api_key=None,
                 image_describe_base_url=None,
                 image_describe_model=None,
                 image_describe_request_delay=None,
                 search_api_key=None,
                 search_model=None,
                 search_base_url=None):
        self.local_image_folder = os.path.join(os.path.dirname(__file__), Config.LOCAL_IMAGE_FOLDER)
        self.web_url_file = os.path.join(os.path.dirname(__file__), Config.WEB_URL_FILE)
        self.database_file = os.path.join(os.path.dirname(__file__), Config.DATABASE_FILE)
        self.index_file = os.path.join(os.path.dirname(__file__), Config.INDEX_FILE)
        
        # 使用传入的配置或默认配置
        self.image_describe_api_key = image_describe_api_key or Config.IMAGE_DESCRIBE_API_KEY
        self.image_describe_base_url = image_describe_base_url or Config.IMAGE_DESCRIBE_BASE_URL
        self.image_describe_model = image_describe_model or Config.IMAGE_DESCRIBE_MODEL
        self.image_describe_request_delay = image_describe_request_delay or Config.IMAGE_DESCRIBE_REQUEST_DELAY
        self.search_api_key = search_api_key or Config.SEARCH_API_KEY
        self.search_model = search_model or Config.SEARCH_MODEL
        self.search_base_url = search_base_url or Config.SEARCH_BASE_URL
        
        self.image_description_database = ImageDescriptionDatabase(
            self.local_image_folder, 
            self.web_url_file, 
            self.database_file, 
            self.index_file,
            image_describe_api_key=self.image_describe_api_key,
            image_describe_base_url=self.image_describe_base_url,
            image_describe_model=self.image_describe_model,
            image_describe_request_delay=self.image_describe_request_delay
        )
        self.image_description_database.construct_image_description_database()
        
        self.client = OpenAI(api_key=self.search_api_key, base_url=self.search_base_url)
        
    def search(self, query: str, top_k: int = 5) -> List[str]:
        # 数据库列表
        database_list = self.image_description_database.database_list
        # 列表转化为带有标号的字符串
        database_str = ""
        for i, description in enumerate(database_list):
            database_str += f"{i+1}. {description}\n"

        # 使用LLM根据query和database_str生成一个prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant that can find the most relevant meme from the database to match the query."},
            {"role": "user", "content": f"问题: {query}\n数据库: {database_str}\n请返回{top_k}个最相关表情包的索引。注意输出格式需要格式化为如下的格式：\n1-索引-推荐原因\n..."}
        ]
        
        response = self.client.chat.completions.create(
            model=self.search_model,
            messages=messages,
            temperature=0.5
        )
        
        # 解析response
        response_content = response.choices[0].message.content
        # 将response_content转化为列表
        response_list = response_content.split("\n")
        # 将response_list中的1-索引-推荐原因格式转化为索引列表和推荐原因列表
        result_index_list = []
        result_reason_list = []
        for i in response_list:
            index = int(i.split("-")[1])
            reason = i.split("-")[2]
            result_index_list.append(index)
            result_reason_list.append(reason)
        
        # 根据response_list从index_list中获取对应的图片路径
        index_list = self.image_description_database.index_list
        result_image_list = [os.path.join(self.local_image_folder, index_list[i-1]) for i in result_index_list]
        
        return result_image_list, result_reason_list
        