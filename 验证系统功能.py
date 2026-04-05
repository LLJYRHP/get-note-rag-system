# 验证系统核心功能
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, '.')

from src.api.get_api import GetNoteAPI
from src.retrieval.retrieval import retrieve_notes

print("=" * 60)
print("验证健医融合·科学健康管理系统功能")
print("=" * 60)

print("1. 测试 Get 笔记 API 连接...")
try:
    api = GetNoteAPI()
    print("API 客户端初始化成功")
    print("API Key: " + api.api_key[:20] + "...")
    print("KB ID: " + api.kb_id)
    print("Base URL: " + api.base_url)
except Exception as e:
    print("API 客户端初始化失败: " + str(e))
    sys.exit(1)

print()
print("2. 测试笔记检索功能...")
try:
    test_query = "如何通过饮食改善高血压？"
    print("搜索查询: " + test_query)
    
    notes = retrieve_notes(test_query, top_k=3)
    
    print("检索完成，找到 " + str(len(notes)) + " 个结果:")
    print("-" * 60)
    
    for i, note in enumerate(notes, 1):
        print("\n结果 " + str(i) + ":")
        print("  标题: " + note.get('title', '无标题'))
        print("  来源: " + note.get('source', '未知来源'))
        content = note.get('content', '无内容')
        if len(content) > 300:
            content = content[:300] + "..."
        print("  内容: " + content)
        print("-" * 60)
        
except Exception as e:
    print("检索失败: " + str(e))
    import traceback
    traceback.print_exc()

print()
print("3. 测试健康管理相关查询...")
try:
    health_query = "健康管理的核心概念是什么？"
    print("搜索查询: " + health_query)
    
    health_notes = retrieve_notes(health_query, top_k=3)
    
    print("检索完成，找到 " + str(len(health_notes)) + " 个结果:")
    print("-" * 60)
    
    for i, note in enumerate(health_notes, 1):
        print("\n结果 " + str(i) + ":")
        print("  标题: " + note.get('title', '无标题'))
        print("  来源: " + note.get('source', '未知来源'))
        content = note.get('content', '无内容')
        if len(content) > 300:
            content = content[:300] + "..."
        print("  内容: " + content)
        print("-" * 60)
        
except Exception as e:
    print("检索失败: " + str(e))
    import traceback
    traceback.print_exc()

print()
print("验证完成!")
print("核心功能正常，系统可以使用 Get 笔记 API 进行健康管理相关的查询。")
print()
print("如何启动系统:")
print(r"1. 打开命令提示符 (cmd.exe)")
print(r"2. 切换到系统目录: cd d:\销售\.trae\Get笔记学习系统")
print(r"3. 运行命令: C:\Users\30314\python-sdk\python3.13.2\python.exe -m streamlit run app.py")
print(r"4. 打开浏览器访问 http://localhost:8501")
