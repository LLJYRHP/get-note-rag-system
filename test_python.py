import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

try:
    import streamlit
    print(f"Streamlit version: {streamlit.__version__}")
except ImportError:
    print("Streamlit is not installed")

print("Test completed")