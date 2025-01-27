# Obsidian 笔记汇总工具

[English Documentation](README.md)

一个高效的 Obsidian 笔记汇总工具，使用 Deepseek 经济实惠的 AI 模型自动生成你的知识库摘要报告。通过集中式的摘要和直接链接，帮助你快速回顾和导航所有笔记内容。

## 功能特点

- **智能摘要**：使用 AI 自动为每个笔记生成简洁的三句话摘要
- **知识导航**：创建直接链接到原始笔记，方便快速参考
- **进度追踪**：实时显示处理进度和详细统计信息
- **中断保护**：支持通过 Ctrl+C 优雅中断并保存进度
- **并行处理**：使用多线程加速处理过程
- **灵活配置**：通过环境变量自定义摘要生成行为


## 成本估算

使用 Deepseek AI 模型的成本非常低：
- 每篇笔记平均成本：约 ¥0.0007-0.0015（基于 token 使用量）
- 处理 1000 篇笔记：约 ¥0.7-1.5
- 显著低于其他商业 AI 模型的价格

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

## 输出格式

生成的摘要文件包含：
- 生成时间戳
- 所有已处理笔记的摘要
- 使用 Obsidian 的 `[[链接]]` 格式直接链接到原始笔记

示例：
```markdown
# Obsidian 文档摘要汇总

> 自动生成于 2024-01-20 15:30

- [[projects/web-dev/react-hooks]]
  React Hooks 是 React 16.8 引入的特性，允许在函数组件中使用状态和其他 React 特性。主要包括 useState 和 useEffect 两个基础 Hook。通过 Hooks 可以实现更清晰的代码组织和状态管理。

- [[learning/python/async-await]]
  Python 的异步编程模型基于协程实现，通过 async/await 语法提供了简洁的异步编程接口。异步编程适合 I/O 密集型任务，可以显著提高程序性能。

// ... 更多摘要 ...
```

## 配置选项

目前支持通过环境变量进行基础配置：
- `DEEPSEEK_API_KEY`：你的 Deepseek API 密钥
- `OBSIDIAN_VAULT`：Obsidian 知识库路径
- `OUTPUT_FILE`：输出摘要文件名（默认：文档摘要汇总.md）

以下配置选项将在未来版本中支持，现在需要自己手动修改代码：
- 处理内容的最大长度
- 摘要生成的 Token 限制
- AI 生成的温度参数
- 最小文件大小过滤
- 自定义系统提示词
- 更多功能...

敬请期待后续更新！如果你想帮助实现这些功能，欢迎参与贡献。

## 参与贡献

欢迎提交 Issue 或 Pull Request 来帮助改进项目。

## 开源协议

本项目采用 MIT 协议开源。
