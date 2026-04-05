# 检查依赖项
print("检查依赖项...")

try:
    import streamlit
    print("✅ streamlit 已安装")
except ImportError:
    print("❌ streamlit 未安装")

try:
    import requests
    print("✅ requests 已安装")
except ImportError:
    print("❌ requests 未安装")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv 已安装")
except ImportError:
    print("❌ python-dotenv 未安装")

print("依赖项检查完成!")
