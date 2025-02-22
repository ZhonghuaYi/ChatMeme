import os
import numpy as np
import pickle
from typing import Optional, List, Dict
from openai import OpenAI
from rich import print
from config.settings import Config
from services.embedding_service import EmbeddingService
from services.image_description_database import ImageDescriptionDatabase


class ImageSearch:
    def __init__(self, 
                 image_describe_api_key=None,
                 image_describe_base_url=None,
                 image_describe_model=None,
                 image_describe_request_delay=None,
                 search_api_key=None,
                 search_model=None,
                 search_base_url=None,
                 use_embedding_search=False,
                 use_query_understanding=None,
                 embedding_api_key=None,
                 embedding_base_url=None,
                 embedding_model=None):
        self.local_image_folder = Config.LOCAL_IMAGE_FOLDER
        self.web_url_file = Config.WEB_URL_FILE
        self.database_file = Config.DATABASE_FILE
        self.index_file = Config.INDEX_FILE
        
        # 使用传入的配置或默认配置
        self.image_describe_api_key = image_describe_api_key or Config.IMAGE_DESCRIBE_API_KEY
        self.image_describe_base_url = image_describe_base_url or Config.IMAGE_DESCRIBE_BASE_URL
        self.image_describe_model = image_describe_model or Config.IMAGE_DESCRIBE_MODEL
        self.image_describe_request_delay = image_describe_request_delay or Config.IMAGE_DESCRIBE_REQUEST_DELAY
        self.search_api_key = search_api_key or Config.SEARCH_API_KEY
        self.search_model = search_model or Config.SEARCH_MODEL
        self.search_base_url = search_base_url or Config.SEARCH_BASE_URL
        self.use_embedding_search = use_embedding_search
        self.use_query_understanding = use_query_understanding if use_query_understanding is not None else Config.USE_QUERY_UNDERSTANDING
        
        self.image_description_database = ImageDescriptionDatabase(
            local_image_folder=self.local_image_folder,
            web_url_file=self.web_url_file,
            database_file=self.database_file,
            index_file=self.index_file,
            image_describe_api_key=self.image_describe_api_key,
            image_describe_base_url=self.image_describe_base_url,
            image_describe_model=self.image_describe_model,
            image_describe_request_delay=self.image_describe_request_delay
        )
        self.image_description_database.construct_image_description_database()
        
        self._client = None
        
        if self.use_embedding_search:
            self.embedding_service = EmbeddingService(
                api_key=embedding_api_key or Config.EMBEDDING_API_KEY,
                base_url=embedding_base_url or Config.EMBEDDING_BASE_URL,
                model=embedding_model or Config.EMBEDDING_MODEL
            )
            self.embeddings_cache = self._load_or_create_embeddings()

    @property
    def client(self):
        """懒加载OpenAI客户端"""
        if self._client is None:
            if not self.search_api_key:
                raise ValueError("搜索API密钥未设置")
            self._client = OpenAI(api_key=self.search_api_key, base_url=self.search_base_url)
        return self._client

    def _get_embedding_dir(self) -> str:
        """获取当前embedding模型的缓存目录"""
        model_name = Config.EMBEDDING_MODEL.replace('/', '_')
        embedding_dir = os.path.join(Config.EMBEDDING_DATABASE_DIR, model_name)
        os.makedirs(embedding_dir, exist_ok=True)
        return embedding_dir

    def _get_embedding_path(self, image_id: str) -> str:
        """获取特定图片的embedding缓存文件路径"""
        return os.path.join(self._get_embedding_dir(), f"{image_id}.pkl")

    def _load_or_create_embeddings(self) -> Dict[str, np.ndarray]:
        """加载或创建embeddings缓存"""
        embeddings = {}
        embedding_dir = self._get_embedding_dir()
        
        for desc, idx in zip(self.image_description_database.database_list, 
                           self.image_description_database.index_list):
            embedding_path = self._get_embedding_path(idx)
            
            # 尝试加载现有的embedding
            if os.path.exists(embedding_path):
                try:
                    with open(embedding_path, 'rb') as f:
                        embeddings[idx] = pickle.load(f)
                    continue
                except Exception as e:
                    print(f"加载embedding缓存失败 [{idx}]: {e}")
            
            # 如果加载失败或文件不存在，创建新的embedding
            try:
                embedding = self.embedding_service.get_embedding(desc)
                embeddings[idx] = embedding
                # 保存新生成的embedding
                with open(embedding_path, 'wb') as f:
                    pickle.dump(embedding, f)
            except Exception as e:
                print(f"生成embedding失败 [{idx}]: {e}")
        
        return embeddings

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """计算余弦相似度"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def _embedding_search(self, query: str, top_k: int = 5) -> tuple[List[str], List[str]]:
        """使用embedding进行搜索"""
        if self.use_query_understanding:
            # 使用chat模型理解查询
            messages = [
                {"role": "system", "content": "你是一个了解各种表情包（meme）的专家。请帮助用户理解他们的查询意图，描述他们可能感兴趣的smeme的含义。"},
                {"role": "user", "content": query}
            ]
            
            response = self.client.chat.completions.create(
                model=self.search_model,
                messages=messages,
                temperature=0.3
            )
            
            query = response.choices[0].message.content
            print(f"Query understanding: {query}")
        
        # 获取query的embedding
        query_embedding = self.embedding_service.get_embedding(query)
        
        # 计算相似度
        similarities = []
        for idx, embedding in self.embeddings_cache.items():
            sim = self._cosine_similarity(query_embedding, embedding)
            similarities.append((idx, sim))
        
        # 排序获取top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_k_results = similarities[:top_k]
        
        # 准备返回结果
        result_images = [os.path.join(self.local_image_folder, idx) for idx, _ in top_k_results]
        result_reasons = [f"相似度: {sim:.2f}" for _, sim in top_k_results]
        
        return result_images, result_reasons
        
    def search(self, query: str, top_k: int = 5) -> tuple[List[str], List[str]]:
        """搜索接口，支持两种搜索模式"""
        if self.use_embedding_search:
            return self._embedding_search(query, top_k)
        
        else:
            # 原有的基于LLM的搜索逻辑
            database_list = self.image_description_database.database_list
            database_str = ""
            for i, description in enumerate(database_list):
                database_str += f"{i+1}. {description}\n"

            messages = [
                {"role": "system", "content": "You are a helpful assistant that can find the most relevant meme from the database to match the query."},
                {"role": "user", "content": f"问题: {query}\n数据库: {database_str}\n请返回{top_k}个最相关表情包的索引。注意输出格式需要格式化为如下的格式：\n1-索引-推荐原因\n..."}
            ]
            
            response = self.client.chat.completions.create(
                model=self.search_model,
                messages=messages,
                temperature=0.5
            )
            
            response_content = response.choices[0].message.content
            response_list = response_content.split("\n")
            result_index_list = []
            result_reason_list = []
            for i in response_list:
                print(i)
                index = int(i.split("-")[1])
                reason = i.split("-")[2]
                result_index_list.append(index)
                result_reason_list.append(reason)
            
            index_list = self.image_description_database.index_list
            result_image_list = [os.path.join(self.local_image_folder, index_list[i-1]) for i in result_index_list]
            
            return result_image_list, result_reason_list
        