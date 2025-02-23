import streamlit as st
from config.settings import Config

# 页面配置
st.set_page_config(
    page_title="ChatMeme - 配置",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化配置相关的session state
if 'IMAGE_DESCRIBE_API_KEY' not in st.session_state:
    st.session_state.IMAGE_DESCRIBE_API_KEY = Config.IMAGE_DESCRIBE_API_KEY
if 'IMAGE_DESCRIBE_BASE_URL' not in st.session_state:
    st.session_state.IMAGE_DESCRIBE_BASE_URL = Config.IMAGE_DESCRIBE_BASE_URL
if 'IMAGE_DESCRIBE_MODEL' not in st.session_state:
    st.session_state.IMAGE_DESCRIBE_MODEL = Config.IMAGE_DESCRIBE_MODEL
if 'IMAGE_DESCRIBE_REQUEST_DELAY' not in st.session_state:
    st.session_state.IMAGE_DESCRIBE_REQUEST_DELAY = Config.IMAGE_DESCRIBE_REQUEST_DELAY
if 'SEARCH_API_KEY' not in st.session_state:
    st.session_state.SEARCH_API_KEY = Config.SEARCH_API_KEY
if 'SEARCH_MODEL' not in st.session_state:
    st.session_state.SEARCH_MODEL = Config.SEARCH_MODEL
if 'SEARCH_BASE_URL' not in st.session_state:
    st.session_state.SEARCH_BASE_URL = Config.SEARCH_BASE_URL
if 'USE_EMBEDDING_SEARCH' not in st.session_state:
    st.session_state.USE_EMBEDDING_SEARCH = Config.USE_EMBEDDING_SEARCH
if 'USE_QUERY_UNDERSTANDING' not in st.session_state:
    st.session_state.USE_QUERY_UNDERSTANDING = Config.USE_QUERY_UNDERSTANDING
if 'EMBEDDING_API_KEY' not in st.session_state:
    st.session_state.EMBEDDING_API_KEY = Config.EMBEDDING_API_KEY
if 'EMBEDDING_BASE_URL' not in st.session_state:
    st.session_state.EMBEDDING_BASE_URL = Config.EMBEDDING_BASE_URL
if 'EMBEDDING_MODEL' not in st.session_state:
    st.session_state.EMBEDDING_MODEL = Config.EMBEDDING_MODEL

st.title("⚙️ ChatMeme - 配置")
st.markdown("在这里您可以配置搜索和图像描述的相关设置。")

# 创建两列布局
col1, col2 = st.columns(2)

# 左列：图像描述配置和搜索配置
with col1:
    # 图像描述相关配置
    st.subheader("📷 图像描述配置")
    st.text_input(
        "图像描述API密钥",
        value=st.session_state.IMAGE_DESCRIBE_API_KEY,
        key="image_describe_api_key_input",
        on_change=lambda: setattr(st.session_state, 'IMAGE_DESCRIBE_API_KEY', st.session_state.image_describe_api_key_input)
    )
    st.text_input(
        "图像描述基础URL（例如：https://api.openai.com/v1）",
        value=st.session_state.IMAGE_DESCRIBE_BASE_URL,
        key="image_describe_base_url_input",
        on_change=lambda: setattr(st.session_state, 'IMAGE_DESCRIBE_BASE_URL', st.session_state.image_describe_base_url_input)
    )
    st.text_input(
        "图像描述模型",
        value=st.session_state.IMAGE_DESCRIBE_MODEL,
        key="image_describe_model_input",
        on_change=lambda: setattr(st.session_state, 'IMAGE_DESCRIBE_MODEL', st.session_state.image_describe_model_input)
    )
    st.number_input(
        "图像描述请求延迟",
        value=float(st.session_state.IMAGE_DESCRIBE_REQUEST_DELAY),
        key="image_describe_request_delay_input",
        on_change=lambda: setattr(st.session_state, 'IMAGE_DESCRIBE_REQUEST_DELAY', st.session_state.image_describe_request_delay_input)
    )
    
    # 搜索相关配置
    st.subheader("🔍 搜索配置")
    st.text_input(
        "搜索API密钥",
        value=st.session_state.SEARCH_API_KEY,
        key="search_api_key_input",
        on_change=lambda: setattr(st.session_state, 'SEARCH_API_KEY', st.session_state.search_api_key_input)
    )
    st.text_input(
        "搜索模型",
        value=st.session_state.SEARCH_MODEL,
        key="search_model_input",
        on_change=lambda: setattr(st.session_state, 'SEARCH_MODEL', st.session_state.search_model_input)
    )
    st.text_input(
        "搜索基础URL",
        value=st.session_state.SEARCH_BASE_URL,
        key="search_base_url_input",
        on_change=lambda: setattr(st.session_state, 'SEARCH_BASE_URL', st.session_state.search_base_url_input)
    )

# 右列：搜索模式和Embedding配置
with col2:
    # 搜索模式选择
    st.subheader("🎯 搜索模式")
    st.checkbox(
        "使用Embedding搜索",
        value=st.session_state.USE_EMBEDDING_SEARCH,
        key="use_embedding_search_input",
        help="启用后将使用基于Embedding的语义搜索",
        on_change=lambda: setattr(st.session_state, 'USE_EMBEDDING_SEARCH', st.session_state.use_embedding_search_input)
    )
    
    # 只有在启用Embedding搜索时才显示相关配置
    if st.session_state.USE_EMBEDDING_SEARCH:
        st.subheader("🧬 Embedding配置")
        st.text_input(
            "Embedding API密钥",
            value=st.session_state.EMBEDDING_API_KEY,
            key="embedding_api_key_input",
            on_change=lambda: setattr(st.session_state, 'EMBEDDING_API_KEY', st.session_state.embedding_api_key_input)
        )
        st.text_input(
            "Embedding 基础URL（例如：https://api.openai.com/v1）",
            value=st.session_state.EMBEDDING_BASE_URL,
            key="embedding_base_url_input",
            on_change=lambda: setattr(st.session_state, 'EMBEDDING_BASE_URL', st.session_state.embedding_base_url_input)
        )
        st.text_input(
            "Embedding 模型",
            value=st.session_state.EMBEDDING_MODEL,
            key="embedding_model_input",
            on_change=lambda: setattr(st.session_state, 'EMBEDDING_MODEL', st.session_state.embedding_model_input)
        )
        st.checkbox(
            "启用查询理解",
            value=st.session_state.USE_QUERY_UNDERSTANDING,
            key="use_query_understanding_input",
            help="启用后会先使用LLM理解查询意图，再进行语义搜索",
            on_change=lambda: setattr(st.session_state, 'USE_QUERY_UNDERSTANDING', st.session_state.use_query_understanding_input)
        )

# 应用配置按钮（在两列下方居中显示）
st.markdown("---")
if st.button("应用配置", use_container_width=True):
    st.success("配置已更新！") 