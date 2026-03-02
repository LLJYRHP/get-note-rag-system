
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
    st.header("系统信息")
    st.info("这是一个基于Get笔记API的检索增强生成(RAG)问答系统")

    # 产品介绍
    st.markdown("### 健医融合 · 科学健康管理系统")
    st.markdown("以医疗专业为基础，融合健康管理理念，打造全周期、智能化的科学健康服务体系。")

    # 核心价值
    st.markdown("### ✨ 核心价值")
    st.markdown("- **健医融合**：打通医疗与健康边界，实现连续照护")
    st.markdown("- **科学为本**：标准化流程 + 数据化支撑，提升决策质量")

    # 联系方式
    st.write("**开发**：梁亮")
    st.write("**电话/微信**：18578974141（微信同号）")
# 主界面
# 初始化会话状态（存储聊天历史）
if "messages" not in st.session_state:
    st.session_state.messages = []
st.title("健医融合・科学健康管理系统")
st.markdown("-----")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 智能咨询")
    question = st.text_area(
        label="请输入您的问题...",
        placeholder="例如:如何通过饮食改善高血压？",
        height=150
    )
    submit_button = st.button("📝 提交问题", type="primary", use_container_width=True)

with col2:
    st.subheader("📑 参考依据")
    notes_placeholder = st.empty()
    notes_placeholder.info("提交问题后，系统将展示回答所依据的权威内容")
    # 处理逻辑
    if submit_button and question:
        if not question.strip():
            st.warning("请输入问题内容！")
        else:
            try:
                # 1. 将用户当前问题加入历史记录
                st.session_state.messages.append({"role": "user", "content": question})
                
                # 显示用户刚发的问题
                with st.chat_message("user"):
                    st.write(question)

                # 2. 准备发送给 AI 的完整上下文（最近 5 轮对话）
                history_text = ""
                for msg in st.session_state.messages[-5:]: # 只取最近 5 轮，防止太长
                    role = "用户" if msg["role"] == "user" else "助手"
                    history_text += f"{role}: {msg['content']}\n"

                # 显示加载动画
                with st.spinner("正在结合历史记忆生成回答..."):
                    generator = AnswerGenerator()
                    # 先检索笔记 (保持原有逻辑)
                    notes = retrieve_notes(question, top_k=3)
                    
                    # 调用后端，传入 history_text
                    result = generator.generate(query=question, notes=notes, history=history_text) 
                
                answer = result.get("answer", "")
                references = result.get("references", [])

                # 3. 将 AI 回答加入历史记录
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # 4. 显示 AI 回答
                with st.chat_message("assistant"):
                    st.write(answer)
                    if references:
                        with st.expander("📖 查看相关笔记"):
                            st.write(references)
                    
                # 更新右侧参考依据
                notes_placeholder.info("已基于知识库及历史对话生成综合回答")

            except Exception as e:
                st.error(f"❌ 系统出错：{str(e)}")
                # 如果出错，移除刚才添加的用户消息，避免脏数据
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop() 
                
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
