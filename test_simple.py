# 简单测试脚本
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, '.')

from src.api.get_api import GetNoteAPI

print("测试 Get 笔记 API 连接...")
try:
    api = GetNoteAPI()
    print("API 客户端初始化成功")
    print("API Key: " + api.api_key[:20] + "...")
    print("KB ID: " + api.kb_id)
    print("Base URL: " + api.base_url)
    print("测试完成!")
except Exception as e:
    print("API 客户端初始化失败: " + str(e))
    sys.exit(1)
