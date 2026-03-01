
import streamlit as st
from src.retrieval.retrieval import retrieve_notes
from src.generation.generator import AnswerGenerator
from src.utils.logger import get_logger
import time

# 初始化日志
logger = get_logger(__name__)

# 页面配置
st.set_page_config(
    page_title="Get笔记RAG问答系统",
    page_icon="📝",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
<style>
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        margin-bottom: 1rem;
    }
    .answer-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    .note-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        margin-bottom: 0.5rem;
    }
    .note-title {
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .note-snippet {
        color: #555;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.header("系统信息")st.标题(“系统信息”)
    st.info("这是一个基于Get笔记API的检索增强生成(RAG)问答系统"这是一个基于Get笔记API的检索增强生成(RAG)问答系统)st.信息(“这是一个基于Get笔记API的检索增强生成这是一个基于Get笔记API的检索增强生成(RAG)问答系统”)
    
    st.markdown("### 使用说明：")
    st.markdown("1. 在下方输入框中输入您的问题")
    st.markdown("2. 点击'提交问题'按钮")st.markdown("2. 点击'提交问题'按钮'")
    st.markdown("3. 系统会从Get笔记中检索相关内容并生成回答")st.markdown(“3. 系统会从Get笔记中检索相关内容并生成回答”)
    st.markdown("4. 回答会包含引用来源和相关笔记片段")st.markdown(“4. 回答会包含引用来源和相关笔记片段”)
    
    st.markdown("### 注意事项：")st.markdown(“### 注意事项：”)
    st.markdown("- 请确保已配置好 API_KEY 和 KB_ID 环境变量")
    st.markdown("- 问题描述越具体，回答越准确")

# 主界面
st.title("🧠 健医融合・科学健康管理系统")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:与col1:
    st.subheader("📋 问题输入")
    question = st.text_area(问题 = st.文本区域(
        "请输入您的问题：",
        placeholder="例如：如何使用LangChain构建RAG系统？",placeholder=“例如：如何使用LangChain构建RAG系统？”,
        height=150
    )
    
    submit_button = st.button("🚀 提交问题", type="primary", use_container_width=True)submit_button = st.button(“提交问题”, type=“primary”, use_container_width=True)

with col2:
    st.subheader("📚 相关笔记")
    notes_placeholder = st.empty()
    notes_placeholder.info("提交问题后，相关笔记会显示在这里")

# 处理逻辑
if submit_button and question:
    if not question.strip():
        st.warning("请输入问题内容！")
    else:
        try:
            # 显示加载动画
            with st.spinner('正在检索笔记并生成回答，请稍候...'):
                start_time = time.time()
                
                # 1. 检索笔记
                logger.info(f"用户提交查询：{question}")
                notes = retrieve_notes(question, top_k=3)
                
                # 2. 判断结果类型并展示
                has_ai_answer = False
                ai_answer_content = ""
                regular_notes = []
                
                for note in notes:
                    # 检查是否是 AI 生成的回答 (我们之前设定的标记)
                    if note.get("source") == "Get 笔记 AI 生成" or note.get("title") == "AI 综合回答":
                        has_ai_answer = True
                        ai_answer_content = note.get("content", "")
                    else:
                        regular_notes.append(note)
                
                end_time = time.time()
                duration = end_time - start_time
                
                # 显示耗时
                st.success(f"处理完成，用时 {duration:.2f} 秒")
                
                # 3. 展示结果
                st.subheader("💡 回答结果")
                
                if has_ai_answer:
                    # 展示 AI 回答
                    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                    st.markdown("### 回答")
                    # 处理换行符，让文本更易读
                    formatted_answer = ai_answer_content.replace('\\n', '\n').replace('\n\n', '\n\n')
                    st.write(formatted_answer)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 如果有普通笔记片段，也显示在右侧
                    if regular_notes:
                        notes_placeholder.subheader("参考笔记片段")
                        for i, note in enumerate(regular_notes):
                            title = note.get("title", f"笔记片段 {i+1}")
                            snippet = note.get("content", note.get("snippet", "无内容"))
                            # 截断过长的片段
                            if len(snippet) > 200:
                                snippet = snippet[:200] + "..."
                            
                            notes_placeholder.markdown(f"""
                            <div class="note-card">
                                <div class="note-title">{title}</div>
                                <div class="note-snippet">{snippet}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        notes_placeholder.success("AI 已基于知识库生成综合回答")
                        
                elif regular_notes:
                    # 没有 AI 回答，但有普通笔记
                    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                    st.markdown("### 找到以下相关笔记：")
                    for i, note in enumerate(regular_notes):
                        title = note.get("title", f"笔记片段 {i+1}")
                        snippet = note.get("content", note.get("snippet", "无内容"))
                        st.markdown(f"**{title}**:")
                        st.write(snippet)
                        st.markdown("---")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    notes_placeholder.subheader("相关笔记列表")
                    for i, note in enumerate(regular_notes):
                        title = note.get("title", f"笔记片段 {i+1}")
                        notes_placeholder.markdown(f"- {title}")
                        
                else:
                    # 完全没有结果
                    st.warning("抱歉，未检索到与您的问题相关的笔记内容。请尝试调整问题表述或提供更多关键词。")
                    notes_placeholder.warning("无相关笔记")
                    
        except Exception as e:
            logger.error(f"处理过程中发生错误：{e}")
            st.error(f"处理过程中发生错误：{str(e)}")
            notes_placeholder.error("检索失败")

# 页脚
st.markdown("---")
st.caption("© 2026 Get笔记RAG问答系统 - 基于LangChain和Streamlit构建")
