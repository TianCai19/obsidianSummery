# Obsidian Summary

[中文文档](README_zh.md)

This project provides a summary of your Obsidian notes.

## Features

- Summarizes notes
- Easy to use
- Integrates with Obsidian

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

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
