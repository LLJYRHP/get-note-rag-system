import logging
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
log_level = os.getenv('LOG_LEVEL', 'INFO')
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 创建日志目录
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置文件日志 (使用 utf-8 编码，防止中文和 Emoji 乱码)
file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'), encoding='utf-8')
file_handler.setLevel(log_level)
file_handler.setFormatter(logging.Formatter(log_format))

# 配置控制台日志
# 小白科普：Windows 的 cmd/PowerShell 默认可能是 GBK 编码。
# 如果 API 返回了包含 Emoji (如 💡) 的文本，直接打印会导致 UnicodeEncodeError 崩溃。
# 这里我们强制让控制台输出使用 utf-8，解决潜在的隐形炸弹！
console_handler = logging.StreamHandler(sys.stdout)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
console_handler.setLevel(log_level)
console_handler.setFormatter(logging.Formatter(log_format))

# 创建日志记录器
def get_logger(name):
    """
    获取日志记录器 (Logger)
    
    小白科普：
    这个函数就像是给每个文件发一个专属的“记录本”。
    你在哪个文件调用它，它就会把那个文件的名字印在日志上，
    这样程序报错时，你一眼就能看出是哪个文件在捣鬼。
    
    Args:
        name: 日志记录器名称 (通常传入 __name__)
        
    Returns:
        日志记录器对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # 避免重复添加处理器 (防止日志重复打印两遍)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
