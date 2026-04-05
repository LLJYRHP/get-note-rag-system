import sys
sys.path.insert(0, '.')

from src.api.get_api import GetNoteAPI

print("=" * 60)
print("测试 Get 笔记 API 搜索功能")
print("=" * 60)

print("正在初始化 API 客户端...")
try:
    api = GetNoteAPI()
    print("✅ API 客户端初始化成功")
    print(f"API Key: {api.api_key[:20]}...")
    print(f"KB ID: {api.kb_id}")
    print(f"Base URL: {api.base_url}")
except Exception as e:
    print(f"❌ API 客户端初始化失败: {e}")
    sys.exit(1)

print()
print("测试搜索功能...")
try:
    test_query = "健康管理"
    print(f"搜索查询: {test_query}")
    
    results = api.search_notes(test_query, top_k=3)
    
    print(f"\n✅ 搜索完成，找到 {len(results)} 个结果:")
    print("-" * 60)
    
    for i, result in enumerate(results, 1):
        print(f"\n结果 {i}:")
        print(f"  标题: {result.get('title', '无标题')}")
        print(f"  来源: {result.get('source', '未知来源')}")
        content = result.get('content', '无内容')
        if len(content) > 200:
            content = content[:200] + "..."
        print(f"  内容: {content}")
        print("-" * 60)
        
except Exception as e:
    print(f"❌ 搜索失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成!")
