import streamlit as st
import random
from services.image_search import ImageSearch
from config.settings import Config

# 页面配置
st.set_page_config(
    page_title="ChatMeme",
    page_icon="🌐",
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

# 使用session state中的配置初始化搜索引擎
search_engine = ImageSearch(
    image_describe_api_key=st.session_state.IMAGE_DESCRIBE_API_KEY,
    image_describe_base_url=st.session_state.IMAGE_DESCRIBE_BASE_URL,
    image_describe_model=st.session_state.IMAGE_DESCRIBE_MODEL,
    image_describe_request_delay=st.session_state.IMAGE_DESCRIBE_REQUEST_DELAY,
    search_api_key=st.session_state.SEARCH_API_KEY,
    search_model=st.session_state.SEARCH_MODEL,
    search_base_url=st.session_state.SEARCH_BASE_URL
)

# 搜索框提示语列表
SEARCH_PLACEHOLDERS = [
    "如何看待Deepseek？",
    "如何看待六代机？",
    "如何看待VVQuery？",
    "如何看待张维为？",
    "如何看待...？",
]

st.title("ChatMeme")

# 初始化session state
if 'placeholder' not in st.session_state:
    st.session_state.placeholder = random.choice(SEARCH_PLACEHOLDERS)
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'n_results' not in st.session_state:
    st.session_state.n_results = 5

# 搜索函数
def search():
    if not st.session_state.search_query:
        return
    try:
        with st.spinner('Searching'):
            results, reasons = search_engine.search(
                st.session_state.search_query, 
                st.session_state.n_results,
            )
            return (results, reasons) if results else ([], [])
    except Exception as e:
        st.sidebar.error(f"搜索失败: {e}")
        return [], []

# 回调函数
def on_input_change():
    st.session_state.search_query = st.session_state.user_input
    st.session_state.results = search()

def on_slider_change():
    st.session_state.n_results = st.session_state.n_results_widget
    if st.session_state.search_query:
        st.session_state.results = search()

# def on_api_key_change():
#     st.session_state.api_key = st.session_state.api_key_input

# 侧边栏搜索区域
with st.sidebar:
    st.title("🔍 ChatMeme")
    
    # 配置区域（可折叠）
    with st.expander("⚙️ 配置设置"):
        # 图像描述相关配置
        st.subheader("图像描述配置")
        st.text_input(
            "IMAGE_DESCRIBE_API_KEY",
            value=st.session_state.IMAGE_DESCRIBE_API_KEY,
            type="password",
            key="image_describe_api_key_input",
            on_change=lambda: setattr(st.session_state, 'IMAGE_DESCRIBE_API_KEY', st.session_state.image_describe_api_key_input)
        )
        st.text_input(
            "IMAGE_DESCRIBE_BASE_URL",
            value=st.session_state.IMAGE_DESCRIBE_BASE_URL,
            key="image_describe_base_url_input",
            on_change=lambda: setattr(st.session_state, 'IMAGE_DESCRIBE_BASE_URL', st.session_state.image_describe_base_url_input)
        )
        st.text_input(
            "IMAGE_DESCRIBE_MODEL",
            value=st.session_state.IMAGE_DESCRIBE_MODEL,
            key="image_describe_model_input",
            on_change=lambda: setattr(st.session_state, 'IMAGE_DESCRIBE_MODEL', st.session_state.image_describe_model_input)
        )
        st.number_input(
            "IMAGE_DESCRIBE_REQUEST_DELAY",
            value=float(st.session_state.IMAGE_DESCRIBE_REQUEST_DELAY),
            key="image_describe_request_delay_input",
            on_change=lambda: setattr(st.session_state, 'IMAGE_DESCRIBE_REQUEST_DELAY', st.session_state.image_describe_request_delay_input)
        )
        
        # 搜索相关配置
        st.subheader("搜索配置")
        st.text_input(
            "SEARCH_API_KEY",
            value=st.session_state.SEARCH_API_KEY,
            type="password",
            key="search_api_key_input",
            on_change=lambda: setattr(st.session_state, 'SEARCH_API_KEY', st.session_state.search_api_key_input)
        )
        st.text_input(
            "SEARCH_MODEL",
            value=st.session_state.SEARCH_MODEL,
            key="search_model_input",
            on_change=lambda: setattr(st.session_state, 'SEARCH_MODEL', st.session_state.search_model_input)
        )
        st.text_input(
            "SEARCH_BASE_URL",
            value=st.session_state.SEARCH_BASE_URL,
            key="search_base_url_input",
            on_change=lambda: setattr(st.session_state, 'SEARCH_BASE_URL', st.session_state.search_base_url_input)
        )
        
        # 应用配置按钮
        if st.button("应用配置", use_container_width=True):
            # 重新初始化搜索引擎
            search_engine = ImageSearch(
                image_describe_api_key=st.session_state.IMAGE_DESCRIBE_API_KEY,
                image_describe_base_url=st.session_state.IMAGE_DESCRIBE_BASE_URL,
                image_describe_model=st.session_state.IMAGE_DESCRIBE_MODEL,
                image_describe_request_delay=st.session_state.IMAGE_DESCRIBE_REQUEST_DELAY,
                search_api_key=st.session_state.SEARCH_API_KEY,
                search_model=st.session_state.SEARCH_MODEL,
                search_base_url=st.session_state.SEARCH_BASE_URL
            )
            st.success("配置已更新！")
    
    # 原有的搜索输入框和其他控件
    user_input = st.text_input(
        "请输入搜索关键词", 
        value=st.session_state.search_query,
        placeholder=st.session_state.placeholder,
        key="user_input",
        on_change=on_input_change
    )
    
    n_results = st.slider(
        "选择展示的结果数量", 
        1, 30, 
        value=st.session_state.n_results,
        key="n_results_widget",
        on_change=on_slider_change
    )
    
    search_button = st.button("搜索", use_container_width=True, on_click=on_input_change)

# 主区域显示
if not st.session_state.get("results"):
    # 初始页面显示欢迎信息
    st.title("👋 Welcome！")
    st.markdown("""
                在左侧的侧边栏输入或者点击左上角的箭头以开始。
                """)
else:
    # 显示搜索结果
    results, reasons = st.session_state.results
    if results:
        # 使用列布局显示图片
        cols = st.columns(3)  # 在一行中显示3张图片
        for i, (image_path, reason) in enumerate(zip(results, reasons)):
            with cols[i % 3]:
                st.image(image_path, use_container_width=True)
                st.markdown(f"*{reason}*")
    else:
        st.sidebar.warning("未找到匹配的表情包") 

# 添加页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    
    🌟 关注我 | Follow Me 🌟
    
    👨‍💻 [GitHub](https://github.com/DanielZhangyc) · 
    📺 [哔哩哔哩](https://space.bilibili.com/165404794) · 
    📝 [博客](https://www.xy0v0.top/)
    </div>
    """, 
    unsafe_allow_html=True
) 