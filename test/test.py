import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# 配置信息
OBSIDIAN_VAULT = os.getenv("OBSIDIAN_VAULT", r"C:\Users\jack\iCloudDrive\iCloud~md~obsidian\Cody")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "文档摘要汇总.md")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")



# 初始化DeepSeek客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def validate_config():
    """验证配置是否有效"""
    if not os.path.exists(OBSIDIAN_VAULT):
        raise ValueError(f"Obsidian库路径不存在: {OBSIDIAN_VAULT}")
    
    if not DEEPSEEK_API_KEY:
        raise ValueError("缺少DeepSeek API密钥")
    
    print("配置验证通过，开始处理...")

def generate_summary(content):
    """使用DeepSeek生成摘要"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "user",
                "content": f"请为以下内容生成简洁的摘要，保留关键信息，使用中文：\n{content}"
            }],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"生成摘要时出错: {e}")
        return None

def test_deepseek_access():
    """测试DeepSeek API访问"""
    try:
        # 测试接口可用性
        client.models.list()
        print("DeepSeek API访问成功")
        return True
    except Exception as e:
        print(f"DeepSeek API访问失败: {e}")
        return False

if __name__ == "__main__":
    validate_config()
    # test_deepseek_access()
    print(generate_summary("这是一段测试文本"))