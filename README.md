# ChatMeme
一个基于人工智能的表情包工具，可以根据给定的上下文环境推荐合适的表情包。

本项目受到 [VVQuest](https://github.com/DanielZhangyc/VVQuest) 的启发并部分基于其实现。

## 功能特点
### AI描述的表情包数据库
通过使用视觉-语言模型，我们可以用自然语言描述每个表情包。

### 表情包推荐
通过使用表情包数据库，我们可以根据给定的上下文环境推荐合适的表情包，并给出推荐理由。

## 使用方法

1. 克隆项目

```bash
git clone https://github.com/ZhonghuaYi/ChatMeme.git
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置环境变量

```bash
cp .env_template .env
```
编辑 `.env` 文件，配置环境变量，包含：
- `LOCAL_IMAGE_FOLDER`：本地表情包图片文件夹路径
- `WEB_URL_FILE`：表情包图片的web url文件路径
- `DATABASE_FILE`：表情包描述数据库文件路径
- `INDEX_FILE`：表情包描述索引文件路径
- `IMAGE_DESCRIBE_API_KEY`：表情包描述API密钥
- `IMAGE_DESCRIBE_BASE_URL`：表情包描述API基础URL
- `IMAGE_DESCRIBE_MODEL`：表情包描述模型
- `IMAGE_DESCRIBE_REQUEST_DELAY`：表情包描述API请求延迟
- `SEARCH_API_KEY`：搜索API密钥
- `SEARCH_MODEL`：搜索模型
- `SEARCH_BASE_URL`：搜索API基础URL
- `EMBEDDING_API_KEY`：Embedding API密钥
- `EMBEDDING_BASE_URL`：Embedding API基础URL
- `EMBEDDING_MODEL`：Embedding模型

本项目提供一些默认的配置，可以参考 `.env_template` 文件。

4. 运行项目

```bash
streamlit run streamlit_app.py
```

## 项目特点

- 使用VLM直接描述表情包
- 可选择使用LLM直接进行推荐，并具有推荐理由
- 可选择使用Embedding进行语义搜索，同时可选择使用LLM对提问进行理解
- 灵活添加新的表情包描述模型和搜索模型
