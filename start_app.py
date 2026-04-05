import subprocess
import sys

print("启动健医融合·科学健康管理系统...")

# 定义 Streamlit 命令
python_path = r"C:\Users\30314\python-sdk\python3.13.2\python.exe"
command = [python_path, "-m", "streamlit", "run", "app.py"]

print(f"执行命令: {' '.join(command)}")

# 执行命令并捕获输出
try:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=r"d:\销售\.trae\Get笔记学习系统"
    )
    
    # 实时读取输出
    while True:
        stdout_line = process.stdout.readline()
        stderr_line = process.stderr.readline()
        
        if stdout_line:
            print(f"STDOUT: {stdout_line.strip()}")
        if stderr_line:
            print(f"STDERR: {stderr_line.strip()}")
        
        if process.poll() is not None:
            break
    
    # 读取剩余输出
    stdout, stderr = process.communicate()
    if stdout:
        print(f"STDOUT: {stdout}")
    if stderr:
        print(f"STDERR: {stderr}")
    
    print(f"命令执行完成，退出码: {process.returncode}")
    
except Exception as e:
    print(f"执行命令时发生错误: {e}")
