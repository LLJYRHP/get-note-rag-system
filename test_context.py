"""
上下文管理器测试演示
"""

from context_manager import get_context_manager

def test_context_manager():
    """测试上下文管理器功能"""
    
    print("="*60)
    print("上下文管理器功能测试")
    print("="*60)
    
    # 获取管理器
    cm = get_context_manager()
    
    # 1. 创建会话
    print("\n1️⃣ 创建会话")
    session_id = cm.create_session("test_user")
    print(f"   ✓ 会话 ID: {session_id[:16]}...")
    
    # 2. 添加对话
    print("\n2️⃣ 添加多轮对话")
    cm.add_message(session_id, 'user', '如何通过饮食改善高血压？')
    cm.add_message(session_id, 'assistant', '建议您低盐饮食，多吃蔬菜水果...')
    cm.add_message(session_id, 'user', '那运动方面呢？')
    cm.add_message(session_id, 'assistant', '建议每周至少 150 分钟中等强度运动...')
    cm.add_message(session_id, 'user', '谢谢，我记住了')
    print("   ✓ 已添加 5 条消息")
    
    # 3. 查看历史
    print("\n3️⃣ 查看对话历史")
    history = cm.get_history(session_id, n=5)
    for i, msg in enumerate(history, 1):
        role = "👤 用户" if msg['role'] == 'user' else "🤖 助手"
        print(f"   {i}. {role}: {msg['content'][:30]}...")
    
    # 4. 上下文摘要
    print("\n4️⃣ 上下文摘要")
    summary = cm.get_context_summary(session_id) if hasattr(cm, 'get_context_summary') else {}
    if summary:
        print(f"   消息数：{summary.get('message_count', 0)}")
        print(f"   创建时间：{summary.get('created_at', '')}")
    else:
        ctx = cm.get_context(session_id)
        print(f"   消息数：{len(ctx.messages)}")
        print(f"   用户：{ctx.user_id}")
    
    # 5. 隐私过滤测试
    print("\n5️⃣ 隐私过滤测试")
    cm.add_message(session_id, 'user', '我的电话是 13812345678')
    history = cm.get_history(session_id, n=1)
    print(f"   原始：我的电话是 13812345678")
    print(f"   过滤后：{history[0]['content']}")
    
    print("\n" + "="*60)
    print("✅ 所有测试完成！")
    print("="*60)
    print(f"\n数据已保存到：data/conversation_contexts.json")

if __name__ == "__main__":
    test_context_manager()