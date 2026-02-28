from typing import List, Dict, Any
from src.api.get_api import GetNoteAPI
from src.utils.logger import get_logger

# 初始化日志
logger = get_logger(__name__)

def retrieve_notes(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    检索相关笔记的核心函数
    Args:
        query: 用户查询语句
        top_k: 返回的最大结果数
    Returns:
        包含相关笔记信息的列表
    """
    logger.info(f"开始检索笔记，查询：{query}")
    
    try:
        # 初始化 API 客户端
        api = GetNoteAPI()
        
        # 调用 API 进行搜索
        notes = api.search_notes(query, top_k)
        
        logger.info(f"检索完成，找到 {len(notes)} 个相关笔记/回答")
        
        # ✅ 关键：直接返回所有结果，不做任何过滤
        return notes
        
    except Exception as e:
        logger.error(f"检索笔记时发生异常：{e}")
        # 发生错误时返回空列表，避免程序崩溃
        return []