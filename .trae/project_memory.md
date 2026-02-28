# Get笔记RAG问答系统配置流程

## 项目结构

```
Get笔记学习系统/
├── app.py                 # Streamlit前端应用
├── requirements.txt       # 依赖包清单
├── start.bat              # 启动脚本
├── .env.example           # 环境变量示例文件
├── src/                   # 源代码目录
│   ├── api/               # API连接模块
│   ├── retrieval/         # 检索模块
│   ├── generation/        # 生成模块
│   └── utils/             # 工具函数
├── tests/                 # 测试用例
├── TEST_REPORT.md         # 功能测试报告
└── README.md              # 项目说明文档
```

## 环境配置

1. **Python环境**：确保安装了Python 3.8或更高版本

2. **环境变量配置**：
   - 复制`.env.example`文件为`.env`
   - 在`.env`文件中配置以下环境变量：
     ```
     # Get笔记API配置
     API_KEY=your_api_key_here
     KB_ID=your_kb_id_here
     
     # 应用配置
     APP_NAME=Get笔记RAG问答系统
     DEBUG=True
     
     # 检索配置
     TOP_K=3
     SIMILARITY_THRESHOLD=0.7
     
     # 日志配置
     LOG_LEVEL=INFO
     ```
   - 注意：`API_KEY`和`KB_ID`必须从Get笔记平台获取

## 运行方法

### 方法一：使用启动脚本
1. 双击运行`start.bat`脚本
2. 脚本会自动：
   - 检查Python和pip是否安装
   - 安装所需依赖
   - 检查环境变量文件
   - 启动Streamlit应用

### 方法二：手动安装和运行
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 启动应用：
   ```bash
   streamlit run app.py
   ```

## 核心功能

- **检索增强生成**：基于Get笔记内容生成准确的回答
- **引用来源标注**：明确标注回答的引用来源
- **相关性排序**：按相关性对检索结果进行排序
- **错误处理**：完善的错误处理和用户友好的提示
- **日志记录**：详细的系统运行日志

## 技术栈

- **后端开发语言**：Python 3.8+
- **前端框架**：Streamlit 1.20.0+
- **核心逻辑框架**：LangChain 0.0.200+
- **网络请求**：requests库
- **环境变量管理**：python-dotenv
- **测试框架**：unittest

## 注意事项

- 确保`API_KEY`和`KB_ID`配置正确
- 问题描述越具体，回答越准确
- 系统会过滤低于相关性阈值的结果
- 当检索不到相关笔记时，会给出相应提示
- 系统运行日志会保存在`logs/app.log`文件中

## 故障排查

- **API认证失败**：检查API_KEY是否正确
- **知识库不存在**：检查KB_ID是否正确
- **网络连接错误**：检查网络连接是否正常
- **依赖安装失败**：确保pip版本更新，尝试使用`pip install --upgrade pip`
