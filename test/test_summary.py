import os
from openai import OpenAI, APIError
from dotenv import load_dotenv
from frontmatter import Frontmatter

load_dotenv()

# 配置信息
OBSIDIAN_VAULT = os.getenv("OBSIDIAN_VAULT", r"C:\Users\jack\iCloudDrive\iCloud~md~obsidian\Cody")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "文档摘要汇总.md")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 初始化客户端（根据DeepSeek最新文档调整）
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1",  # 注意：结尾不要带斜杠
)

def validate_config():
    """增强配置验证"""
    missing_config = []
    
    if not os.path.exists(OBSIDIAN_VAULT):
        missing_config.append(f"Obsidian路径不存在: {OBSIDIAN_VAULT}")
    
    if not DEEPSEEK_API_KEY:
        missing_config.append("未配置DEEPSEEK_API_KEY")
    
    if missing_config:
        raise ValueError("\n".join(missing_config))
    
    # API连通性测试
    try:
        test_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
            timeout=10
        )
        print(f"API连通测试成功（使用模型：{test_response.model}）")
    except APIError as e:
        error_msg = f"API验证失败 [{e.status_code}]: {e.message}"
        if e.status_code == 404:
            error_msg += "\n可能原因：1.API地址错误 2.模型名称不正确"
        raise ConnectionError(error_msg)

def generate_summary(content):
    """增强版摘要生成"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "system",
                "content": "你是一个专业的内容摘要助理，用3句流畅的中文总结以下内容的核心观点，保持专业且易于理解"
            },{
                "role": "user", 
                "content": f"{content[:3500]}"  # 控制上下文长度
            }],
            temperature=0.3,
            max_tokens=256,
            timeout=15
        )
        
        # 处理空响应
        if not response.choices[0].message.content:
            return "（未生成有效摘要）"
            
        return response.choices[0].message.content.strip()
        
    except APIError as e:
        print(f"[API错误] 状态码：{e.status_code} | 错误信息：{e.message}")
    except Exception as e:
        print(f"[系统错误] {str(e)}")
    
    return "摘要生成失败"

# 测试执行（需在正式代码中移除）
if __name__ == "__main__":
    try:
        validate_config()
        test_content = "大型语言模型（LLM）是基于Transformer架构的深度学习模型，通过海量文本训练获得理解生成自然语言的能力。最新研究表明，结合强化学习（RLHF）可以显著提升模型的对齐性能。"
        print("测试摘要结果：", generate_summary(test_content))
    except Exception as e:
        print(f"配置验证失败: {str(e)}")