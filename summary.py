# File 2: summary.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from obsidian_tools import SummaryProcessor

load_dotenv()

def validate_config() -> dict:
    """验证并返回配置"""
    config = {
        "vault_path": os.path.expanduser(os.getenv("OBSIDIAN_VAULT")),
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "output_file": os.getenv("OUTPUT_FILE", "文档摘要汇总.md")
    }
    
    if not config["api_key"]:
        raise ValueError("DEEPSEEK_API_KEY 未配置")
    
    if not config["vault_path"] or not os.path.exists(config["vault_path"]):
        raise ValueError("Obsidian知识库路径配置错误或不存在")
        
    return config

def main():
    try:
        config = validate_config()
        
        client = OpenAI(
            api_key=config["api_key"],
            base_url="https://api.deepseek.com/v1"
        )
        
        processor = SummaryProcessor(client)
        print("🦉 开始处理知识库... (按 Ctrl+C 可中断并保存进度)")
        processor.process_vault(
            vault_path=config["vault_path"],
            output_file=config["output_file"]
        )
        
    except Exception as e:
        print(f"\n❌ 程序运行失败: {str(e)}")

if __name__ == "__main__":
    main()