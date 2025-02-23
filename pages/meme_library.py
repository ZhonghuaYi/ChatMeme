import streamlit as st
from services.image_description_database import ImageDescriptionDatabase
from config.settings import Config
import os

# 页面配置
st.set_page_config(
    page_title="ChatMeme - 表情包库",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state用于存储当前页码
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# 初始化数据库
image_db = ImageDescriptionDatabase(
    local_image_folder=Config.LOCAL_IMAGE_FOLDER,
    web_url_file=Config.WEB_URL_FILE,
    database_file=Config.DATABASE_FILE,
    index_file=Config.INDEX_FILE,
    image_describe_api_key=st.session_state.get('IMAGE_DESCRIBE_API_KEY'),
    image_describe_base_url=st.session_state.get('IMAGE_DESCRIBE_BASE_URL'),
    image_describe_model=st.session_state.get('IMAGE_DESCRIBE_MODEL'),
    image_describe_request_delay=st.session_state.get('IMAGE_DESCRIBE_REQUEST_DELAY')
)

# 构建数据库（如果需要）
image_db.construct_image_description_database()

st.title("📚 表情包库")
st.markdown("这里展示了所有可用的表情包及其描述")

# 分页设置
images_per_page = 30
total_images = len(image_db.index_list)
num_pages = (total_images + images_per_page - 1) // images_per_page

# 创建分页导航
with st.container():  # 使用容器来居中
    cols = st.columns([1, 6, 1])  # 分成三列，中间列放页码按钮
    
    # 上一页按钮
    with cols[0]:
        if st.button("上一页", key="prev_page", disabled=st.session_state.current_page == 1):
            if st.session_state.current_page > 1:
                st.session_state.current_page -= 1
                st.rerun()  # 确保页面更新
    
    # 页码按钮
    with cols[1]:
        page_cols = st.columns(9)  # 用于显示所有页码的列
        
        # 确定要显示哪些页码
        current_page = st.session_state.current_page
        pages_to_show = set()
        pages_to_show.add(1)  # 第一页
        pages_to_show.add(num_pages)  # 最后一页
        pages_to_show.add(current_page)  # 当前页
        
        # 当前页左右的页码
        for i in range(max(2, current_page - 1), min(current_page + 2, num_pages)):
            pages_to_show.add(i)
        
        # 将页码排序
        pages_to_show = sorted(list(pages_to_show))
        
        # 显示页码按钮
        button_idx = 0
        for i, page in enumerate(pages_to_show):
            # 如果页码不连续，显示省略号
            if i > 0 and page > pages_to_show[i-1] + 1:
                with page_cols[button_idx]:
                    st.markdown("...")
                button_idx += 1
            
            # 显示页码按钮
            with page_cols[button_idx]:
                if st.button(str(page), key=f"page_{page}", type="primary" if page == current_page else "secondary"):
                    st.session_state.current_page = page
                    st.rerun()  # 使用新的API
            button_idx += 1
            
            # 每个按钮都在同一行显示
            if button_idx >= 9:
                break
    
    # 下一页按钮
    with cols[2]:
        if st.button("下一页", key="next_page", disabled=st.session_state.current_page == num_pages):
            if st.session_state.current_page < num_pages:
                st.session_state.current_page += 1
                st.rerun()  # 确保页面更新

# 计算当前页的图片索引
start_idx = (st.session_state.current_page - 1) * images_per_page
end_idx = min(start_idx + images_per_page, total_images)

# 显示当前页的图片和描述
cols_per_row = 3
for idx in range(start_idx, end_idx):
    if idx % cols_per_row == 0:
        cols = st.columns(cols_per_row)  # 创建新的列
    col_idx = idx % cols_per_row
    with cols[col_idx]:
        image_path = image_db.index_list[idx]
        description = image_db.database_list[idx]
        
        # 如果是本地图片，需要构建完整路径
        if not image_path.startswith('http'):
            full_image_path = os.path.join(Config.LOCAL_IMAGE_FOLDER, image_path)
        else:
            full_image_path = image_path
        
        # 显示图片和描述
        st.image(full_image_path, use_container_width=True)
        st.markdown(f"""
            <div style='padding: 10px; border-radius: 5px; margin-bottom: 20px'>
                <p style='margin: 0; font-size: 0.9em'>{description}</p>
            </div>
        """, unsafe_allow_html=True)

# 在底部也显示分页导航
with st.container():  # 使用容器来居中
    cols = st.columns([1, 6, 1])  # 分成三列，中间列放页码按钮
    
    # 上一页按钮
    with cols[0]:
        if st.button("上一页", key="prev_page_bottom", disabled=st.session_state.current_page == 1):
            if st.session_state.current_page > 1:
                st.session_state.current_page -= 1
                st.rerun()  # 确保页面更新
    
    # 页码按钮
    with cols[1]:
        page_cols = st.columns(9)  # 用于显示所有页码的列
        
        # 确定要显示哪些页码
        current_page = st.session_state.current_page
        pages_to_show = set()
        pages_to_show.add(1)  # 第一页
        pages_to_show.add(num_pages)  # 最后一页
        pages_to_show.add(current_page)  # 当前页
        
        # 当前页左右的页码
        for i in range(max(2, current_page - 1), min(current_page + 2, num_pages)):
            pages_to_show.add(i)
        
        # 将页码排序
        pages_to_show = sorted(list(pages_to_show))
        
        # 显示页码按钮
        button_idx = 0
        for i, page in enumerate(pages_to_show):
            # 如果页码不连续，显示省略号
            if i > 0 and page > pages_to_show[i-1] + 1:
                with page_cols[button_idx]:
                    st.markdown("...")
                button_idx += 1
            
            # 显示页码按钮
            with page_cols[button_idx]:
                if st.button(str(page), key=f"page_{page}_bottom", type="primary" if page == current_page else "secondary"):
                    st.session_state.current_page = page
                    st.rerun()  # 使用新的API
            button_idx += 1
            
            # 每个按钮都在同一行显示
            if button_idx >= 9:
                break
    
    # 下一页按钮
    with cols[2]:
        if st.button("下一页", key="next_page_bottom", disabled=st.session_state.current_page == num_pages):
            if st.session_state.current_page < num_pages:
                st.session_state.current_page += 1
                st.rerun()  # 确保页面更新

# 添加页脚
st.markdown("---")
st.markdown(
    """
    
    <div style='text-align: center'>
    👨‍💻 [GitHub](https://github.com/ZhonghuaYi)
    </div>
    """, 
    unsafe_allow_html=True
)
