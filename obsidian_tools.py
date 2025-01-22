# File 1: obsidian_tools.py
import os
import re
import signal
import time
from typing import Set
from openai import OpenAI, APIError
from frontmatter import Frontmatter

class SummaryProcessor:
    def __init__(self, client: OpenAI):
        self.client = client
        self.interrupted = False
        self.stats = {
            "total_files": 0,
            "processed_files": 0,
            "skipped_files": 0,
            "total_tokens": 0,
            "start_time": time.time()
        }
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def handle_interrupt(self, signum, frame):
        """处理中断信号"""
        self.interrupted = True
        print("\n检测到中断，正在保存当前进度...")

    def get_processed_links(self, output_path: str) -> Set[str]:
        """获取已处理的文档链接"""
        processed = set()
        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
                matches = re.findall(r"\[\[(.*?)\]\]", content)
                processed = set(matches)
        return processed

    def process_content(self, raw_content: str) -> str:
        """预处理Markdown内容"""
        try:
            post = Frontmatter.reads(raw_content)
            return post.content
        except:
            return raw_content

    def generate_summary(self, content: str) -> (str, int):
        """生成摘要并返回token使用量"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的内容摘要助理，用3句流畅的中文总结以下内容的核心观点，保持专业且易于理解"
                    },
                    {
                        "role": "user", 
                        "content": f"{content[:3500]}"
                    }
                ],
                temperature=0.3,
                max_tokens=256
            )
            
            usage = response.usage.total_tokens
            return response.choices[0].message.content.strip(), usage
            
        except APIError as e:
            print(f"\n[API错误] 状态码：{e.status_code} | 错误信息：{e.message}")
        except Exception as e:
            print(f"\n[系统错误] {str(e)}")
        
        return "", 0

    def print_progress(self):
        """显示实时进度"""
        elapsed = time.time() - self.stats["start_time"]
        processed = self.stats["processed_files"]
        total = self.stats["total_files"]
        
        progress = processed / total if total > 0 else 0
        eta = (total - processed) * elapsed / processed if processed > 0 else 0
        
        print(f"\r🚀 进度: {processed}/{total} ({progress:.1%}) | "
              f"⏳ 用时: {elapsed:.1f}s | "
              f"📊 Token: {self.stats['total_tokens']} | "
              f"🕒 剩余: {eta:.1f}s", end="")

    def init_output_file(self, output_path: str):
        """初始化输出文件"""
        if not os.path.exists(output_path):
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("# Obsidian 文档摘要汇总\n\n")
                f.write("> 自动生成于 {}\n\n".format(time.strftime("%Y-%m-%d %H:%M")))
        else:
            # 检查文件头是否完整
            with open(output_path, "r+", encoding="utf-8") as f:
                content = f.read()
                if not content.startswith("# Obsidian 文档摘要汇总"):
                    f.seek(0, 0)
                    f.write("# Obsidian 文档摘要汇总\n\n> 自动生成于 {}\n\n".format(time.strftime("%Y-%m-%d %H:%M")) + content)

    def _walk_vault(self, vault_path: str):
        """生成器：预遍历知识库文件"""
        for root, _, files in os.walk(vault_path):
            if self.interrupted:
                return
            if any(x in root for x in ["templates", ".trash"]):
                continue
            for file in files:
                if file.endswith(".md"):
                    yield os.path.join(root, file)

    def _should_process(self, file_path: str, processed_links: set) -> bool:
        """判断文件是否需要处理"""
        rel_path = os.path.relpath(file_path, start=self.vault_path)
        obsidian_link = rel_path.replace(".md", "").replace("\\", "/")
        return (
            os.path.getsize(file_path) > 1024 and  # 过滤小文件
            obsidian_link not in processed_links and
            not any(p in rel_path for p in ["_templates", "Daily Notes"])  # 额外过滤条件
        )

    def process_single_file(self, file_path: str, output_path: str, lock):
        """处理单个文件（线程安全版本）"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
                
            if not raw_content.strip():
                return 0

            content = self.process_content(raw_content)
            summary, tokens = self.generate_summary(content)
            
            if summary:
                rel_path = os.path.relpath(file_path, start=self.vault_path)
                obsidian_link = rel_path.replace(".md", "").replace("\\", "/")
                entry = f"- [[{obsidian_link}]]\n  {summary}\n\n"
                
                # 使用线程锁保证写入安全
                with lock:
                    with open(output_path, "a", encoding="utf-8") as f:
                        f.write(entry)

            return tokens
            
        except Exception as e:
            print(f"\n处理文件失败 {file_path}: {str(e)}")
            return 0

    def process_vault(self, vault_path: str, output_file: str) -> None:
        """处理整个知识库（多线程优化版）"""
        self.vault_path = vault_path
        output_path = os.path.join(vault_path, output_file)
        processed_links = self.get_processed_links(output_path)
        self.init_output_file(output_path)

        # 预扫描并过滤文件
        file_list = []
        for file_path in self._walk_vault(vault_path):
            if self._should_process(file_path, processed_links):
                file_list.append(file_path)
        self.stats["total_files"] = len(file_list)
        self.stats["skipped_files"] = sum(1 for _ in self._walk_vault(vault_path)) - len(file_list)

        try:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            import threading
            
            # 初始化线程锁
            write_lock = threading.Lock()
            # 动态调整线程数（4-8个）
            max_workers = min(8, max(4, (os.cpu_count() or 4)))
            completed = 0
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(self.process_single_file, f, output_path, write_lock): f for f in file_list}
                
                for future in as_completed(futures):
                    if self.interrupted:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                        
                    tokens = future.result()
                    self.stats["processed_files"] += 1
                    self.stats["total_tokens"] += tokens
                    completed += 1
                    
                    # 降低进度刷新频率（每处理1%或至少1秒）
                    if completed % max(1, len(file_list)//100) == 0 or time.time() - self.stats["start_time"] > 1:
                        self.print_progress()
            
            print(f"\n\n✅ 处理完成！结果已保存至：{output_path}")
            
        finally:
            total_time = time.time() - self.stats["start_time"]
            print(f"\n📊 最终统计：")
            print(f"- 总文件数: {self.stats['total_files'] + self.stats['skipped_files']}")
            print(f"- 待处理文件: {self.stats['total_files']}")
            print(f"- 成功处理: {self.stats['processed_files']}")
            print(f"- 跳过文件: {self.stats['skipped_files']}")
            print(f"- 总Token用量: {self.stats['total_tokens']}")
            print(f"- 总耗时: {total_time:.1f}秒")
            if total_time > 0:
                print(f"- 处理速度: {self.stats['processed_files']/total_time:.1f} 文件/秒")
                print(f"- Token速率: {self.stats['total_tokens']/total_time:.1f} token/秒")
