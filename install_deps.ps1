$pythonPath = "C:\Users\30314\python-sdk\python3.13.2\python.exe"
Write-Host "使用清华镜像安装依赖..."
& $pythonPath -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple streamlit requests python-dotenv
Write-Host "依赖安装完成!"
Write-Host "启动应用..."
& $pythonPath -m streamlit run app.py
