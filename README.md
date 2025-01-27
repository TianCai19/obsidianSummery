# Obsidian Summary

[中文文档](README_zh.md)

An efficient tool to create a comprehensive summary of your Obsidian notes using Deepseek's cost-effective AI model. It helps you quickly review and navigate through your knowledge base by generating a centralized summary with direct links to original notes.

## Features

- **Smart Summarization**: Automatically generates concise 3-sentence summaries for each note using AI
- **Knowledge Navigation**: Creates direct links to original notes for easy reference
- **Progress Tracking**: Shows real-time progress with detailed statistics
- **Interrupt-Safe**: Supports graceful interruption and progress saving with Ctrl+C
- **Parallel Processing**: Utilizes multi-threading for faster processing
- **Configurable**: Customize summary generation through environment variables



## Cost Estimation

Using Deepseek's AI model is very cost-effective:
- Average cost per note: ~$0.0001-0.0002 (based on token usage)
- Process 1000 notes: ~$0.1-0.2
- Significantly cheaper than other commercial AI models

## Installation

1. Install `uv`:
    ```sh
    pip install uv
    ```

2. Sync dependencies:
    ```sh
    uv sync
    ```

## Usage

1. Configure the .env file with your settings. You can use the provided `env.example` file as a template:
    ```sh
    cp env.example .env
    ```

2. Set up your configuration:
   - Get your Deepseek API key:
     1. Sign up at https://platform.deepseek.com/
     2. Go to "API Keys" section
     3. Create a new API key
     4. Copy the key to your .env file

   - Find your Obsidian vault path:
     1. Open Obsidian
     2. Go to Settings → About
     3. Look for "Vault path"
     4. Copy the path to your .env file
     - On macOS/Linux: e.g., `/Users/username/Documents/ObsidianVault`
     - On Windows: e.g., `C:\Users\username\Documents\ObsidianVault`

3. Run the project:
    ```sh
    uv run summary.py
    ```

    Example output:
    ```
    🦉 Starting to process vault... (Press Ctrl+C to interrupt and save progress)
    🚀 Progress: 24/24 (100.0%) | ⏳ Time: 18.3s | 📊 Token: 25788 | 🕒 ETA: 0.0s

    ✅ Processing complete! Results saved to: /path/to/vault/summary.md

    📊 Final Statistics:
    - Total files: 43
    - Files to process: 24
    - Successfully processed: 24
    - Skipped files: 19
    - Total tokens used: 25788
    - Total time: 18.3s
    - Processing speed: 1.3 files/sec
    - Token rate: 1405.4 tokens/sec
    ```

## Output Format

The generated summary file contains:
- A timestamp of generation
- Summaries of all processed notes
- Direct links to original notes using Obsidian's `[[link]]` format

Example:
```markdown
# Obsidian 文档摘要汇总

> 自动生成于 2024-01-20 15:30

- [[projects/web-dev/react-hooks]]
  React Hooks 是 React 16.8 引入的特性，允许在函数组件中使用状态和其他 React 特性。主要包括 useState 和 useEffect 两个基础 Hook。通过 Hooks 可以实现更清晰的代码组织和状态管理。

- [[learning/python/async-await]]
  Python 的异步编程模型基于协程实现，通过 async/await 语法提供了简洁的异步编程接口。异步编程适合 I/O 密集型任务，可以显著提高程序性能。

// ... more summaries ...
```

## Configuration Options

Currently, basic configuration is supported through environment variables:
- `DEEPSEEK_API_KEY`: Your Deepseek API key
- `OBSIDIAN_VAULT`: Path to your Obsidian vault
- `OUTPUT_FILE`: Name of the output summary file (default: 文档摘要汇总.md)

Advanced configuration options will be supported in future releases:
- Maximum content length for processing
- Summary token limit
- AI generation temperature
- Minimum file size filter
- Custom system prompt
- And more...

Stay tuned for updates! Feel free to contribute if you'd like to help implement these features.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
