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
        # 关键修改：deep_seek=True (开启深度思考), refs=True (获取引用来源)
        payload = {
            "question": query,              # 参数名必须是 question
            "topic_ids": [self.kb_id],      # 必须是列表格式 ["kb_id"]
            "deep_seek": True,              # 开启深度思考，进行更深入的分析
            "refs": True,                   # 开启引用来源，返回具体的笔记片段
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
            # 正常格式可能是 {'data': [...]}
            # 但 Get 笔记 AI 回答通常在 {'c': {'answers': '...'}} 中
            
            # 1. 优先尝试提取 AI 生成的答案 (c.answers)
            if isinstance(result, dict):
                if 'c' in result and isinstance(result['c'], dict):
                    answers = result['c'].get('answers', '')
                    refs = result['c'].get('refs', [])
                    
                    combined_result = []
                    
                    # 如果有 AI 回答，加入结果列表
                    if answers:
                        logger.info("成功从 'c.answers' 提取到 AI 回答！")
                        combined_result.append({
                            "content": answers, 
                            "source": "Get 笔记 AI 生成",
                            "title": "AI 综合回答"
                        })
                    
                    # 如果有引用片段，也加入结果列表
                    if refs:
                        logger.info(f"成功从 'c.refs' 提取到 {len(refs)} 条引用笔记")
                        for ref in refs:
                            combined_result.append({
                                "title": ref.get("title", "未知标题"),
                                "content": ref.get("content", ""),
                                "source": "原始笔记片段"
                            })
                    
                    if combined_result:
                        return combined_result
                
                # 2. 如果没找到 c.answers/c.refs，尝试提取原始笔记片段 (data/items)
                data = result.get("data", [])
                if isinstance(data, dict):
                    data = data.get("items", []) or data.get("list", []) or data.get("notes", []) or [data]
                elif not data and result:
                    data = result.get("items", []) or result.get("list", []) or [result]
                
                if data:
                    logger.info(f"成功从 'data' 提取到 {len(data)} 条笔记片段")
                    return data

            # 3. 如果都没找到，返回空列表
            logger.warning("未在 API 响应中找到有效数据字段")
            return []
            
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求错误：{e}")
            error_detail = ""
            if hasattr(e, 'response') and e.response is not None:
                error_detail = f"服务器响应：{e.response.text}"
                logger.error(error_detail)
            raise RuntimeError(f"检索笔记时发生错误：{str(e)} {error_detail}")
        except Exception as e:
            logger.error(f"未知错误：{e}")
            raise RuntimeError(f"检索笔记时发生错误：{str(e)}")