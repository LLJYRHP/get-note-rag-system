import os
import requests
from typing import Dict, List, Any
from src.utils.logger import get_logger
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化日志
logger = get_logger(__name__)

class GetNoteAPI:
    """
    Get 笔记 API 连接模块
    用于与 Get 笔记 API 进行交互，包括检索笔记内容等操作
    """

    def __init__(self):
        """
        初始化 Get 笔记 API 连接
        从环境变量加载 API_KEY 和 KB_ID
        """
        self.api_key = os.getenv('API_KEY')
        self.kb_id = os.getenv('KB_ID')
        
        # 使用正确的官方基础 URL
        self.base_url = "https://open-api.biji.com/getnote/openapi"
        
        # 添加完整的 Headers (包含 X-OAuth-Version)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "X-OAuth-Version": "1"
        }

        # 验证必要的环境变量
        if not self.api_key:
            raise ValueError("API_KEY 环境变量未设置")
        if not self.kb_id:
            raise ValueError("KB_ID 环境变量未设置")
            
        logger.info("GetNoteAPI 初始化成功")

    def search_notes(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        根据查询语句搜索相关笔记
        Args:
            query: 用户查询语句
            top_k: 返回的最大结果数
        Returns:
            包含相关笔记信息的列表
        """
        logger.info(f"开始搜索笔记，查询：{query}")
        
        # 使用正确的接口路径
        url = f"{self.base_url}/knowledge/search"
        
        # 构造符合官方文档的请求体 (JSON Payload)
        payload = {
            "question": query,              # 参数名必须是 question
            "topic_ids": [self.kb_id],      # 使用 topic_ids 数组
            "deep_seek": True,              # 开启深度思考，进行更深入的分析
            "refs": False,                  # 引用在 stream 模式生效
            "history": []                   # 暂不传递历史记录
        }
        
        try:
            logger.info(f"发送 POST 请求到：{url}")
            logger.debug(f"请求参数：{payload}")
            
            # 发送 POST 请求，并设置较长的超时时间以应对深度思考
            response = requests.post(url, headers=self.headers, json=payload, timeout=120)
            
            # 检查 HTTP 状态码
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"API 返回原始结果：{result}")
            
            # ==========================================
            # ✅ 核心修复：专门处理 Get 笔记 API 的特殊返回格式
            # ==========================================
            # 正常格式：{"h": {...}, "c": {"answers": "...", "deep_seek": "..."}}
            
            # 1. 优先尝试提取 AI 生成的答案 (c.answers)
            if isinstance(result, dict):
                if 'c' in result and isinstance(result['c'], dict):
                    answers = result['c'].get('answers', '')
                    
                    combined_result = []
                    
                    # 如果有 AI 回答，加入结果列表
                    if answers:
                        logger.info("成功从 'c.answers' 提取到 AI 回答！")
                        combined_result.append({
                            "content": answers, 
                            "source": "Get 笔记 AI 生成",
                            "title": "AI 综合回答"
                        })
                    
                    if combined_result:
                        return combined_result

            logger.warning("未在 API 响应中找到有效数据字段")
            return []
            
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求错误：{e}")
            return []
        except Exception as e:
            logger.error(f"未知错误：{e}")
            return []

    def save_note(self, title: str, content: str) -> bool:
        """
        将错题保存回 Get 笔记知识库
        Args:
            title: 错题笔记标题
            content: 错题内容及 AI 解析
        Returns:
            是否保存成功
        """
        logger.info(f"准备同步错题到 Get 笔记，标题：{title}")
        
        # 尝试使用基于 openapi.biji.com 的保存接口（需要 note.content.write 权限）
        url = f"{self.base_url}/note/create"
        
        payload = {
            "title": title,
            "content": content,
            "topic_ids": [self.kb_id]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"✅ 错题同步成功！API 返回: {response.json()}")
                return True
            else:
                logger.warning(f"同步失败，状态码：{response.status_code}，如果报错 404 或无权限，请检查 API 端点和 Key 的 write 权限。")
                return False
        except Exception as e:
            logger.error(f"同步错题时发生异常：{e}")
            return False