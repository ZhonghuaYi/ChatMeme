import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SILICON_API_KEY = os.getenv("SILICON_API_KEY")
    IMAGE_DESCRIBE_API_KEY = os.getenv("IMAGE_DESCRIBE_API_KEY")
    IMAGE_DESCRIBE_BASE_URL = os.getenv("IMAGE_DESCRIBE_BASE_URL")
    IMAGE_DESCRIBE_MODEL = os.getenv("IMAGE_DESCRIBE_MODEL")
    IMAGE_DESCRIBE_REQUEST_DELAY = os.getenv("IMAGE_DESCRIBE_REQUEST_DELAY")
    
    SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
    SEARCH_MODEL = os.getenv("SEARCH_MODEL")
    SEARCH_BASE_URL = os.getenv("SEARCH_BASE_URL")
    
    LOCAL_IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), os.getenv("LOCAL_IMAGE_FOLDER"))
    WEB_URL_FILE = os.path.join(os.path.dirname(__file__), os.getenv("WEB_URL_FILE"))
    DATABASE_FILE = os.path.join(os.path.dirname(__file__), os.getenv("DATABASE_FILE"))
    INDEX_FILE = os.path.join(os.path.dirname(__file__), os.getenv("INDEX_FILE"))
    
    # EMBEDDING_MODEL = "BAAI/bge-m3"
    # IMAGE_DIR = os.path.join(os.path.dirname(__file__), os.getenv("IMAGE_DIR"))
    # CACHE_FILE = os.path.join(os.path.dirname(__file__), '../data/embeddings.pkl') 