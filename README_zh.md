# Obsidian 笔记汇总工具

[English Documentation](README.md)

这个项目可以帮助你总结 Obsidian 笔记的内容。

## 功能特点

- 自动总结笔记内容
- 使用简单方便
- 完美集成 Obsidian

## 安装方法

1. 安装 `uv`:
    ```sh
    pip install uv
    ```

2. 同步依赖:
    ```sh
    uv sync
    ```

## 使用说明

1. 配置 .env 文件。你可以使用提供的模板文件 `env.example`:
    ```sh
    cp env.example .env
    ```

2. 设置你的配置:
   - 获取 Deepseek API 密钥:
     1. 注册 https://platform.deepseek.com/
     2. 进入 "API Keys" 页面
     3. 创建新的 API 密钥
     4. 将密钥复制到 .env 文件中

   - 找到你的 Obsidian 仓库路径:
     1. 打开 Obsidian
     2. 进入 设置 → 关于
     3. 找到 "仓库路径"
     4. 将路径复制到 .env 文件中
     - macOS/Linux 示例: `/Users/用户名/Documents/ObsidianVault`
     - Windows 示例: `C:\Users\用户名\Documents\ObsidianVault`

3. 运行项目:
    ```sh
    uv run summary.py
    ```

    运行示例:
    ```
    🦉 开始处理知识库... (按 Ctrl+C 可中断并保存进度)
    🚀 进度: 24/24 (100.0%) | ⏳ 用时: 18.3s | 📊 Token: 25788 | 🕒 剩余: 0.0s

    ✅ 处理完成！结果已保存至：/path/to/vault/summary.md

    📊 最终统计：
    - 总文件数: 43
    - 待处理文件: 24
    - 成功处理: 24
    - 跳过文件: 19
    - 总Token用量: 25788
    - 总耗时: 18.3秒
    - 处理速度: 1.3 文件/秒
    - Token速率: 1405.4 token/秒
    ```

## 参与贡献

欢迎提交 Issue 或 Pull Request 来帮助改进项目。

## 开源协议

本项目采用 MIT 协议开源。
