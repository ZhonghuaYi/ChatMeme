import os
from dotenv import load_dotenv
from pathlib import Path

# 打印当前工作目录和.env文件位置
print(f"Current working directory: {os.getcwd()}")
env_path = Path('.env')
print(f".env file exists: {env_path.exists()}")
print(f".env file path: {env_path.absolute()}")

# 显式指定.env文件路径，并强制覆盖已存在的环境变量
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    # SILICON_API_KEY = os.getenv("SILICON_API_KEY")
    IMAGE_DESCRIBE_API_KEY = os.getenv("IMAGE_DESCRIBE_API_KEY", None)
    IMAGE_DESCRIBE_BASE_URL = os.getenv("IMAGE_DESCRIBE_BASE_URL", "https://api.siliconapi.com/v1")
    IMAGE_DESCRIBE_MODEL = os.getenv("IMAGE_DESCRIBE_MODEL", "deepseek-ai/deepseek-vl2")
    IMAGE_DESCRIBE_REQUEST_DELAY = os.getenv("IMAGE_DESCRIBE_REQUEST_DELAY", 0.1)
    
    SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", None)
    SEARCH_MODEL = os.getenv("SEARCH_MODEL", "gemini-2.0-flash")
    SEARCH_BASE_URL = os.getenv("SEARCH_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    
    # 基础路径
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # 项目根目录
    print(f"\nBASE_DIR: {BASE_DIR}")
    
    # 从环境变量获取相对路径，如果没有设置则使用默认值
    _LOCAL_IMAGE_FOLDER = os.getenv("LOCAL_IMAGE_FOLDER", "data/images")
    _WEB_URL_FILE = os.getenv("WEB_URL_FILE", "data/web_urls.txt")
    _DATABASE_FILE = os.getenv("DATABASE_FILE", "data/database/text_description/database.txt")
    _INDEX_FILE = os.getenv("INDEX_FILE", "data/database/text_description/index.txt")
    
    print("\n环境变量读取结果:")
    print(f"  _LOCAL_IMAGE_FOLDER: {_LOCAL_IMAGE_FOLDER}")
    print(f"  _WEB_URL_FILE: {_WEB_URL_FILE}")
    print(f"  _DATABASE_FILE: {_DATABASE_FILE}")
    print(f"  _INDEX_FILE: {_INDEX_FILE}")
    
    # 将相对路径转换为绝对路径
    LOCAL_IMAGE_FOLDER = os.path.join(BASE_DIR, _LOCAL_IMAGE_FOLDER)
    WEB_URL_FILE = os.path.join(BASE_DIR, _WEB_URL_FILE)
    DATABASE_FILE = os.path.join(BASE_DIR, _DATABASE_FILE)
    INDEX_FILE = os.path.join(BASE_DIR, _INDEX_FILE)
    
    # 打印路径信息用于调试
    print("\n最终路径配置:")
    print(f"  LOCAL_IMAGE_FOLDER: {LOCAL_IMAGE_FOLDER}")
    print(f"  WEB_URL_FILE: {WEB_URL_FILE}")
    print(f"  DATABASE_FILE: {DATABASE_FILE}")
    print(f"  INDEX_FILE: {INDEX_FILE}")
    
    # Embedding相关配置
    EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", None)
    EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "https://api.siliconapi.com/v1")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    EMBEDDING_DATABASE_DIR = os.path.join(BASE_DIR, "data/database/embedding")
    USE_EMBEDDING_SEARCH = os.getenv("USE_EMBEDDING_SEARCH", "false").lower() == "true"
    USE_QUERY_UNDERSTANDING = os.getenv("USE_QUERY_UNDERSTANDING", "false").lower() == "true"
    
    # EMBEDDING_MODEL = "BAAI/bge-m3"
    # IMAGE_DIR = os.path.join(os.path.dirname(__file__), os.getenv("IMAGE_DIR"))
    # CACHE_FILE = os.path.join(os.path.dirname(__file__), '../data/embeddings.pkl') 