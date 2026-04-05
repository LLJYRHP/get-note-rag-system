"""
上下文管理器模块
实现多轮对话的上下文管理、历史记录追踪和上下文引用功能
"""

import json
import os
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import OrderedDict
import re


class ConversationContext:
    """对话上下文类 - 存储单个会话的上下文信息"""
    
    def __init__(self, session_id: str, user_id: str = "default"):
        self.session_id = session_id
        self.user_id = user_id
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        self.messages: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {'topic': None, 'keywords': [], 'sentiment': 'neutral'}
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """添加消息到对话历史"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.messages.append(message)
        self.last_updated = datetime.now()
    
    def get_recent_messages(self, n: int = 5) -> List[Dict]:
        """获取最近 n 条消息"""
        return self.messages[-n:]
    
    def clear_messages(self):
        """清空消息历史"""
        self.messages = []
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat(),
            'messages': self.messages,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationContext':
        """从字典创建"""
        ctx = cls(data['session_id'], data['user_id'])
        ctx.created_at = datetime.fromisoformat(data['created_at'])
        ctx.last_updated = datetime.fromisoformat(data['last_updated'])
        ctx.messages = data['messages']
        ctx.metadata = data.get('metadata', {})
        return ctx


class ContextManager:
    """上下文管理器 - 管理多个会话的上下文"""
    
    def __init__(self, data_dir: str = 'data', max_sessions: int = 100,
                 session_timeout: int = 3600, max_messages: int = 50):
        self.data_dir = data_dir
        self.contexts_file = os.path.join(data_dir, 'conversation_contexts.json')
        self.max_sessions = max_sessions
        self.session_timeout = session_timeout
        self.max_messages = max_messages
        self.contexts_cache: OrderedDict[str, ConversationContext] = OrderedDict()
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self._load_contexts()
    
    def _load_contexts(self):
        """加载上下文"""
        if os.path.exists(self.contexts_file):
            try:
                with open(self.contexts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for sid, ctx_data in data.items():
                        self.contexts_cache[sid] = ConversationContext.from_dict(ctx_data)
            except:
                pass
    
    def _save_contexts(self):
        """保存上下文"""
        data = {sid: ctx.to_dict() for sid, ctx in self.contexts_cache.items()}
        with open(self.contexts_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_session(self, user_id: str = "default") -> str:
        """创建新会话"""
        session_id = hashlib.md5(f"{user_id}_{time.time()}".encode()).hexdigest()
        ctx = ConversationContext(session_id, user_id)
        self.contexts_cache[session_id] = ctx
        
        if len(self.contexts_cache) > self.max_sessions:
            oldest = next(iter(self.contexts_cache))
            del self.contexts_cache[oldest]
        
        self._save_contexts()
        return session_id
    
    def get_context(self, session_id: str):
        """获取会话上下文"""
        return self.contexts_cache.get(session_id)
    
    def add_message(self, session_id: str, role: str, content: str) -> bool:
        """添加消息"""
        ctx = self.get_context(session_id)
        if not ctx:
            return False
        
        # 隐私过滤
        if role == 'user':
            content = self._filter_sensitive(content)
        
        ctx.add_message(role, content)
        
        if len(ctx.messages) > self.max_messages:
            ctx.messages = ctx.messages[-self.max_messages:]
        
        self._save_contexts()
        return True
    
    def get_history(self, session_id: str, n: int = 5) -> List[Dict]:
        """获取对话历史"""
        ctx = self.get_context(session_id)
        if not ctx:
            return []
        return ctx.get_recent_messages(n)
    
    def clear_session(self, session_id: str) -> bool:
        """清空会话"""
        ctx = self.get_context(session_id)
        if not ctx:
            return False
        ctx.clear_messages()
        self._save_contexts()
        return True
    
    def _filter_sensitive(self, content: str) -> str:
        """过滤敏感信息"""
        content = re.sub(r'1[3-9]\d{9}', '[手机号已隐藏]', content)
        content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                        '[邮箱已隐藏]', content)
        return content


# 全局实例
_context_manager = None

def get_context_manager() -> ContextManager:
    """获取全局上下文管理器"""
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager()
    return _context_manager