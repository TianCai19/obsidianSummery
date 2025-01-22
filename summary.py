# File 2: summary.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from obsidian_tools import process_vault

load_dotenv()

def validate_config():
    """验证环境配置"""
    required_vars = {
        "OBSIDIAN_VAULT": os.getenv("OBSIDIAN_VAULT"),
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY")
    }
    
    missing = [k for k, v in required_vars.items() if not v]
    if missing:
        raise ValueError(f"缺少环境变量: {', '.join(missing)}")
    
    if not os.path.exists(required_vars["OBSIDIAN_VAULT"]):
        raise ValueError("Obsidian知识库路径不存在")

def get_client() -> OpenAI:
    """创建DeepSeek客户端"""
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1"
    )

if __name__ == "__main__":
    try:
        validate_config()
        client = get_client()
        process_vault(
            client=client,
            vault_path=os.getenv("OBSIDIAN_VAULT"),
            output_file=os.getenv("OUTPUT_FILE", "文档摘要汇总.md")
        )
    except Exception as e:
        print(f"程序执行失败: {str(e)}")