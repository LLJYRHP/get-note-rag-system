import streamlit as st
from src.retrieval.retrieval import retrieve_notes
from src.api.get_api import GetNoteAPI
from src.utils.logger import get_logger
import time
import json
import os
import hashlib
import re
from datetime import datetime
from typing import List, Dict, Any

# 初始化日志
logger = get_logger(__name__)


class ContextManager:
    """
    上下文管理器 - 负责管理多轮对话的会话和历史记录
    功能：创建会话、保存对话历史、加载历史记录、隐私过滤
    """
    
    def __init__(self, data_dir: str = 'data'):
        """初始化上下文管理器"""
        self.data_dir = data_dir
        self.file = os.path.join(data_dir, 'contexts.json')
        self.contexts: Dict[str, List[Dict]] = {}
        self._ensure_dir()
        self._load()
    
    def _ensure_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load(self):
        """从文件加载上下文数据"""
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    self.contexts = json.load(f)
            except Exception as e:
                logger.error(f"加载上下文失败：{e}")
                self.contexts = {}
        else:
            self.contexts = {}
    
    def _save(self):
        """保存上下文数据到文件"""
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(self.contexts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存上下文失败：{e}")
    
    def create_session(self) -> str:
        """创建新会话，返回会话 ID"""
        sid = hashlib.md5(f"{time.time()}_{os.urandom(8).hex()}".encode()).hexdigest()[:16]
        self.contexts[sid] = []
        self._save()
        logger.info(f"创建新会话：{sid}")
        return sid
    
    def get_session(self, sid: str) -> List[Dict]:
        """获取指定会话的历史记录"""
        return self.contexts.get(sid, [])
    
    def add_message(self, sid: str, role: str, content: str):
        """
        添加消息到会话历史
        role: 'user' 或 'assistant'
        content: 消息内容
        """
        if sid not in self.contexts:
            return
        
        filtered_content = self._filter_sensitive_info(content)
        
        self.contexts[sid].append({
            'role': role,
            'content': filtered_content,
            'time': datetime.now().strftime('%H:%M:%S')
        })
        
        if len(self.contexts[sid]) > 20:
            self.contexts[sid] = self.contexts[sid][-20:]
        
        self._save()
    
    def _filter_sensitive_info(self, text: str) -> str:
        """过滤敏感信息"""
        text = re.sub(r'1[3-9]\d{9}', '[手机号已隐藏]', text)
        text = re.sub(r'\d{17}[\dXx]', '[身份证号已隐藏]', text)
        text = re.sub(r'\d{16,19}', '[银行卡号已隐藏]', text)
        return text
    
    def clear_session(self, sid: str):
        """清空指定会话"""
        if sid in self.contexts:
            self.contexts[sid] = []
            self._save()
    
    def delete_session(self, sid: str):
        """删除会话"""
        if sid in self.contexts:
            del self.contexts[sid]
            self._save()
    
    def get_all_sessions(self) -> Dict[str, List[Dict]]:
        """获取所有会话"""
        return self.contexts
    
    def get_context_text(self, sid: str, last_n: int = 5) -> str:
        """
        获取格式化的上下文文本，用于增强检索
        last_n: 使用最近多少轮对话
        """
        if sid not in self.contexts or not self.contexts[sid]:
            return ""
        
        messages = self.contexts[sid][-last_n*2:]
        context_parts = []
        
        for msg in messages:
            prefix = "用户" if msg['role'] == 'user' else "助手"
            context_parts.append(f"{prefix}: {msg['content']}")
        
        return "\n".join(context_parts)


# 页面配置
st.set_page_config(
    page_title="健医融合·科学健康管理系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式 - 全面 UI 优化版
st.markdown("""
<style>
    /* ==================== 全局样式 ==================== */
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    
    /* 全局字体和配色 */
    .stApp {
        font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    }
    
    /* ==================== 移动端优化 - 响应式布局 ==================== */
    @media (max-width: 768px) {
        .css-1d39wkg {
            padding: 1rem !important;
        }
        .stTextInput > div > div > input {
            font-size: 16px !important;
        }
        .stTextArea > div > div > textarea {
            font-size: 16px !important;
        }
        .stButton > button {
            width: 100%;
        }
    }
    
    /* ==================== 输入框优化 ==================== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 15px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        background-color: #ffffff;
        border-color: #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
        outline: none;
    }
    
    /* ==================== 按钮优化 ==================== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* 次要按钮样式 */
    .stButton[data-baseweb="button"] button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* ==================== 对话消息气泡优化 ==================== */
    .chat-message {
        padding: 1.2rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-user {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 5px solid #2196f3;
        margin-right: 20%;
    }
    
    .chat-assistant {
        background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
        border-left: 5px solid #4caf50;
        margin-left: 20%;
    }
    
    .chat-time {
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    /* ==================== 回答卡片优化 ==================== */
    .answer-box {
        padding: 2rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e0e0e0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    
    /* ==================== 成功提示优化 ==================== */
    .success-box {
        padding: 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        border: 2px solid #c3e6cb;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    /* ==================== 笔记卡片优化 ==================== */
    .note-card {
        padding: 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #e9ecef;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .note-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: #4facfe;
    }
    
    .note-title {
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .note-snippet {
        color: #555;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* ==================== 侧边栏会话样式优化 ==================== */
    .session-item {
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .session-item:hover {
        background-color: #e3f2fd;
        transform: translateX(5px);
    }
    
    .session-active {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        font-weight: 600;
    }
    
    /* ==================== 标题样式优化 ==================== */
    .stTitle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* ==================== 分割线优化 ==================== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 2rem 0;
    }
    
    /* ==================== 警告框优化 ==================== */
    .stAlert {
        border-radius: 12px;
        border: 2px solid;
    }
    
    /* ==================== 加载动画优化 ==================== */
    .stSpinner > div {
        border-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# ========================
# 初始化上下文管理器
# ========================
if 'context_manager' not in st.session_state:
    st.session_state.context_manager = ContextManager()

# ========================
# 初始化会话状态
# ========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "result" not in st.session_state:
    st.session_state.result = None

if "current_session_id" not in st.session_state:
    # 优先使用现有的会话，而不是创建新会话
    all_sessions = st.session_state.context_manager.get_all_sessions()
    if all_sessions:
        # 使用最新的会话（按最后修改时间排序）
        latest_session = max(all_sessions.items(), key=lambda x: len(x[1]))[0]
        st.session_state.current_session_id = latest_session
        # 加载会话的消息历史
        st.session_state.messages = st.session_state.context_manager.get_session(latest_session)
    else:
        # 如果没有现有会话，才创建新会话
        st.session_state.current_session_id = st.session_state.context_manager.create_session()
        st.session_state.messages = []

# ========================
# 侧边栏
# ========================
with st.sidebar:
    st.markdown("## ⚙️ 系统设置")
    
    # 模式切换
    learning_mode = st.radio(
        "📚 选择学习模式",
        ["知识库问答", "系统课程学习"],
        index=0,
        help="【知识库问答】基于你的 Get 笔记进行全局检索。\n【系统课程学习】基于本地的录音和逐字稿进行系统学习。"
    )
    st.session_state.learning_mode = learning_mode
    
    st.markdown("---")
    
    if st.button("➕ 新建会话", use_container_width=True):
        st.session_state.current_session_id = st.session_state.context_manager.create_session()
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 💬 历史会话")
    all_sessions = st.session_state.context_manager.get_all_sessions()
    
    for sid, msgs in sorted(all_sessions.items(), key=lambda x: len(x[1]), reverse=True):
        title = "新会话"
        for msg in msgs:
            if msg['role'] == 'user':
                title = msg['content'][:20] + "..." if len(msg['content']) > 20 else msg['content']
                break
        
        is_active = sid == st.session_state.current_session_id
        col1, col2 = st.columns([4, 1])
        
        with col1:
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"💬 {title}", key=f"session_{sid}", use_container_width=True, type=btn_type):
                st.session_state.current_session_id = sid
                st.session_state.messages = st.session_state.context_manager.get_session(sid)
                st.rerun()
        
        with col2:
            if st.button("🗑️", key=f"delete_{sid}"):
                st.session_state.context_manager.delete_session(sid)
                if sid == st.session_state.current_session_id:
                    st.session_state.current_session_id = st.session_state.context_manager.create_session()
                    st.session_state.messages = []
                st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 🏥 健医融合 · 专属 AI 导师")
    st.markdown("不仅是知识库，更是陪伴你学习的严师！")

    st.markdown("#### 🌟 核心价值")
    st.markdown("- **苏格拉底提问**：每次回答附带3个启发式追问")
    st.markdown("- **学练测评闭环**：即将推出随机抽考与错题本！")

    st.markdown("---")
    st.markdown("#### 👨‍💻 开发者信息")
    st.markdown("**开发**：梁亮")
    st.markdown("**电话/微信**：18578974141（微信同号）")

# ========================
# 主界面 (微信聊天式 UI)
# ========================
st.markdown("<h1 class='stTitle'>🏥 健医融合 · 专属 AI 导师</h1>", unsafe_allow_html=True)
st.caption("基于 Get 笔记生态的主动学习系统 V1.0")
st.markdown("---")

# ========================
# 课程学习模式 (音文同步)
# ========================
current_course_text = ""
if st.session_state.learning_mode == "系统课程学习":
    st.markdown("### 🎧 系统课程点读机")
    
    courses_dir = "courses"
    if not os.path.exists(courses_dir):
        st.warning("未检测到 `courses` 文件夹。请在项目根目录下创建 `courses` 文件夹，并放入课程。")
    else:
        # 获取所有课程文件夹
        course_folders = [f for f in os.listdir(courses_dir) if os.path.isdir(os.path.join(courses_dir, f))]
        
        if not course_folders:
            st.info("当前 `courses` 文件夹中没有课程。请放入例如 `lesson_01` 文件夹。")
        else:
            # 选课下拉框
            selected_course = st.selectbox("选择要学习的课程", course_folders)
            course_path = os.path.join(courses_dir, selected_course)
            
            audio_path = os.path.join(course_path, "audio.mp3")
            text_path = os.path.join(course_path, "text.md")
            if not os.path.exists(text_path):
                text_path = os.path.join(course_path, "text.txt") # 兼容 txt 格式
            
            # 播放器
            if os.path.exists(audio_path):
                st.audio(audio_path, format="audio/mp3")
            else:
                st.warning(f"未找到音频文件：{audio_path} (必须命名为 audio.mp3)")
                
            # 讲义展示
            if os.path.exists(text_path):
                with open(text_path, 'r', encoding='utf-8') as f:
                    current_course_text = f.read()
                
                with st.expander("📄 查看本节讲义/逐字稿 (展开)"):
                    st.markdown(current_course_text)
            else:
                st.warning(f"未找到讲义文件：{text_path} (必须命名为 text.md 或 text.txt)")
    
    st.markdown("---")
    st.markdown("#### 👩‍⚕️ 本课专属助教答疑")

# ========================
# 课后测验考场逻辑
# ========================
if st.session_state.learning_mode == "系统课程学习" and current_course_text:
    st.markdown("---")
    st.markdown("### 🔥 课后专属考场")
    
    if "quiz_question" not in st.session_state:
        st.session_state.quiz_question = None
    if "quiz_feedback" not in st.session_state:
        st.session_state.quiz_feedback = None
        
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("🎯 生成本课测验", type="primary", use_container_width=True):
            with st.spinner("AI 考官正在为您出题..."):
                prompt = f"【出题指令】请根据以下讲义出一道简答题，考查我的核心理解。要求：只要题目，不要输出答案！\n\n讲义：{current_course_text[:2000]}"
                notes = retrieve_notes(prompt, top_k=1)
                ai_answer = ""
                for note in notes:
                    if note.get("title") == "AI 综合回答":
                        ai_answer = note.get("content", "")
                        break
                if ai_answer:
                    st.session_state.quiz_question = ai_answer
                    st.session_state.quiz_feedback = None
                else:
                    st.error("出题失败，请重试。")
                st.rerun()

    if st.session_state.quiz_question:
        st.info(f"**考官提问**：\n\n{st.session_state.quiz_question}")
        
        user_answer = st.text_area("✍️ 请输入你的答案：", height=100, key="quiz_answer")
        
        if st.button("✅ 提交试卷"):
            if not user_answer.strip():
                st.warning("答案不能为空！")
            else:
                with st.spinner("AI 考官正在阅卷，请稍候..."):
                    eval_prompt = f"""【阅卷指令】
原题：{st.session_state.quiz_question}
我的答案：{user_answer}
讲义参考：{current_course_text[:2000]}

请你作为严格的考官，根据讲义给我的答案打分（0-100分）。
请务必在回答的第一行写上“分数：XX”，然后给出详细的点评和正确解析。"""
                    
                    notes = retrieve_notes(eval_prompt, top_k=1)
                    ai_feedback = ""
                    for note in notes:
                        if note.get("title") == "AI 综合回答":
                            ai_feedback = note.get("content", "")
                            break
                    
                    if ai_feedback:
                        st.session_state.quiz_feedback = ai_feedback
                        
                        # 解析分数
                        score_match = re.search(r'分数[：:\s]*(\d+)', ai_feedback)
                        score = int(score_match.group(1)) if score_match else 100
                        
                        if score < 80:
                            st.warning(f"您的得分是 {score} 分，未达标！正在将错题同步至 Get 笔记错题本...")
                            # 尝试保存到 Get 笔记
                            try:
                                api = GetNoteAPI()
                                title = f"健医融合错题集 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                                content = f"**【错题题目】**\n{st.session_state.quiz_question}\n\n**【我的答案】**\n{user_answer}\n\n**【AI 考官解析】**\n{ai_feedback}"
                                success = api.save_note(title, content)
                                if success:
                                    st.success("✅ 错题已成功同步到 Get 笔记！")
                                else:
                                    st.error("❌ 同步错题到 Get 笔记失败，可能是 API 权限问题。")
                            except Exception as e:
                                st.error(f"同步错题时发生错误：{e}")
                        else:
                            st.success(f"🎉 恭喜！您的得分是 {score} 分，顺利过关！")
                            
                    else:
                        st.error("阅卷失败，请重试。")

    if st.session_state.quiz_feedback:
        st.markdown("#### 📝 考官点评")
        st.markdown(f"<div class='answer-box'>{st.session_state.quiz_feedback}</div>", unsafe_allow_html=True)


# ========================
# 对话历史显示区域
# ========================
# 遍历 session_state 中的历史消息，使用 st.chat_message 渲染
for msg in st.session_state.messages:
    # 根据角色选择头像
    avatar = "👨‍🎓" if msg['role'] == 'user' else "👩‍⚕️"
    with st.chat_message(msg['role'], avatar=avatar):
        st.markdown(msg['content'])

# ========================
# 聊天输入区域
# ========================
if prompt := st.chat_input("请输入您想学习的知识点或疑惑，例如：如何理解四步换脑？"):
    # 1. 立即在界面上显示用户的输入
    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)
    
    # 2. 准备处理逻辑
    current_sid = st.session_state.current_session_id
    
    # 构造带有“苏格拉底追问”指令的 Prompt
    # 考虑到 Get 笔记接口的特殊性，我们把指令直接拼在用户问题的末尾
    system_instruction = "\n\n【重要指令：作为《健医融合》专属AI助教，请在回答完上述问题后，根据你的回答内容，自动生成3个相关的、启发式的追问推荐（用无序列表列出，每个问题前加'👉'），引导我进一步深入思考和学习。】"
    
    # 针对不同模式，采用不同的提示词策略
    if st.session_state.learning_mode == "系统课程学习" and current_course_text:
        # 如果是课程学习模式，强制 AI 基于当前的讲义回答
        course_instruction = f"""
【本课专属定向辅导指令】
以下是本节课的核心逐字稿/讲义内容：
---
{current_course_text[:3000]}  # 截取前3000字，防止 API 长度限制超载
---
请你**完全基于上面这节课的内容**，来回答我的问题。
如果讲义中没有提到，请明确告诉我“这节课暂未涉及该内容”，不要自己发散。

我的问题是：{prompt}
"""
        enhanced_prompt = course_instruction + system_instruction
    else:
        # 如果是默认的知识库问答模式
        enhanced_prompt = prompt + system_instruction
    
    # 3. 显示 AI 正在思考的动画
    with st.chat_message("assistant", avatar="👩‍⚕️"):
        with st.spinner("正在您的 Get 笔记中翻阅资料，请稍候..."):
            try:
                start_time = time.time()
                logger.info(f"用户提交查询：{prompt}")
                
                # 获取上下文（历史对话增强）
                context_text = st.session_state.context_manager.get_context_text(current_sid, last_n=3)
                if context_text:
                    final_query = f"历史对话上下文:\n{context_text}\n\n当前问题：{enhanced_prompt}"
                else:
                    final_query = enhanced_prompt
                
                # 调用检索 API
                notes = retrieve_notes(final_query, top_k=3)
                
                has_ai_answer = False
                ai_answer_content = ""
                
                for note in notes:
                    if note.get("source") == "Get 笔记 AI 生成" or note.get("title") == "AI 综合回答":
                        has_ai_answer = True
                        ai_answer_content = note.get("content", "")
                        break
                
                # 记录时间
                end_time = time.time()
                duration = end_time - start_time
                
                # 展示回答
                if has_ai_answer:
                    formatted_answer = ai_answer_content.replace('\\n', '\n').replace('\n\n', '\n\n')
                    st.markdown(formatted_answer)
                    st.caption(f"✅ 检索并生成完成，用时 {duration:.2f} 秒")
                    
                    # 4. 将消息保存到历史记录中
                    st.session_state.context_manager.add_message(current_sid, 'user', prompt)
                    st.session_state.context_manager.add_message(current_sid, 'assistant', formatted_answer)
                    
                    # 5. 同步更新当前会话的 messages，防止引用丢失
                    st.session_state.messages = st.session_state.context_manager.get_session(current_sid)
                    
                else:
                    no_result_msg = "抱歉，您的知识库中未检索到相关内容。请尝试调整问题表述，或补充相关笔记后重试。"
                    st.warning(no_result_msg)
                    st.session_state.context_manager.add_message(current_sid, 'user', prompt)
                    st.session_state.context_manager.add_message(current_sid, 'assistant', no_result_msg)
                    st.session_state.messages = st.session_state.context_manager.get_session(current_sid)
                    
            except Exception as e:
                logger.error(f"处理过程中发生错误：{e}")
                st.error(f"系统开小差了，请稍后再试或检查日志。错误详情：{str(e)}")

# ========================
# 页脚
# ========================
st.markdown("---")
st.caption("© 2026 健医融合·科学健康管理系统 - 基于 LangChain 和 Streamlit 构建 | 支持上下文对话")