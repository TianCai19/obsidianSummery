# File 1: obsidian_tools.py
import os
from openai import OpenAI, APIError
from frontmatter import Frontmatter

def process_content(raw_content: str) -> str:
    """预处理Markdown内容"""
    try:
        post = Frontmatter.reads(raw_content)
        return post.content
    except:
        return raw_content

def generate_deepseek_summary(client: OpenAI, content: str) -> str:
    """使用DeepSeek生成摘要"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "system",
                "content": "你是一个专业的内容摘要助理，用3句流畅的中文总结以下内容的核心观点，保持专业且易于理解"
            },{
                "role": "user", 
                "content": f"{content[:3500]}"
            }],
            temperature=0.3,
            max_tokens=256
        )
        return response.choices[0].message.content.strip()
    except APIError as e:
        print(f"[API错误] 状态码：{e.status_code} | 错误信息：{e.message}")
        return ""
    except Exception as e:
        print(f"[系统错误] {str(e)}")
        return ""

def process_vault(client: OpenAI, vault_path: str, output_file: str) -> None:
    """处理整个知识库"""
    summaries = []
    
    for root, _, files in os.walk(vault_path):
        # 跳过模板和回收站目录
        if any(x in root for x in ["templates", ".trash"]):
            continue
            
        for file in files:
            if not file.endswith(".md"):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    raw_content = f.read()
                    
                if not raw_content.strip():
                    continue
                    
                # 处理内容
                content = process_content(raw_content)
                summary = generate_deepseek_summary(client, content)
                
                if not summary:
                    continue
                    
                # 创建链接
                rel_path = os.path.relpath(file_path, start=vault_path)
                obsidian_link = f"[[{rel_path.replace('.md', '')}]]"
                summaries.append(f"- {obsidian_link}\n  {summary}\n")
                
            except Exception as e:
                print(f"处理文件失败 {file_path}: {str(e)}")
    
    # 写入汇总文件
    output_path = os.path.join(vault_path, output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Obsidian 文档摘要汇总\n\n")
        f.write("\n".join(summaries))
    print(f"已生成汇总文件：{output_path}")