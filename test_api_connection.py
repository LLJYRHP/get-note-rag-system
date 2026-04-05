import requests
import json

# 测试 Get 笔记 API 连接
def test_get_note_api():
    print("=" * 60)
    print("测试 Get 笔记 API 连接")
    print("=" * 60)
    
    # 从环境变量或直接设置
    api_key = "3c7nhXDzlMvJOFwFMfS9argkXJGeQ8Z/g+m09zmkHZdLCp9KKVhjoaJbPprcJ+ioskPSaikDChh+yuo+Tfcla3c/BxDh44TIbBDu"
    kb_id = "qY2k9W60"
    
    # 官方 API 地址
    url = "https://open-api.biji.com/getnote/openapi/knowledge/search"
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "X-OAuth-Version": "1"
    }
    
    # 请求体
    payload = {
        "question": "健康管理",
        "topic_ids": [kb_id],
        "deep_seek": True,
        "refs": False,
        "history": []
    }
    
    print(f"API URL: {url}")
    print(f"API Key: {api_key[:20]}...")
    print(f"KB ID: {kb_id}")
    print()
    
    try:
        print("发送 POST 请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"响应状态码: {response.status_code}")
        print()
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("响应 JSON:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
                # 检查是否有 AI 回答
                if 'c' in data and 'answers' in data['c']:
                    print("\n✅ 成功获取 AI 回答!")
                else:
                    print("\n❌ 未找到 AI 回答")
            except json.JSONDecodeError:
                print("响应不是有效的 JSON:")
                print(response.text)
        else:
            print("错误响应:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 将输出重定向到文件
    import sys
    original_stdout = sys.stdout
    with open('api_test_output.txt', 'w', encoding='utf-8') as f:
        sys.stdout = f
        test_get_note_api()
    sys.stdout = original_stdout
    print("测试完成，结果已保存到 api_test_output.txt")
