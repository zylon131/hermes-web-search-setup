# Hermes Web Search Setup

这个项目旨在帮助 **Hermes Agent** 快速启用联网搜索能力，特别是针对 Windows 环境下的 Bug 修复和免 API Key 的 DuckDuckGo 搜索集成。

## 🚀 特性
- **一键配置**：自动完成依赖安装、代码补丁和配置更新。
- **免 API Key**：内置基于 `duckduckgo-search` 的搜索驱动。
- **兼容性修复**：修复了 Windows 下导致的 CLI 崩溃问题。

## 📦 安装方法 (通过 Hermes)

在终端运行：
```bash
hermes skills install https://github.com/YOUR_USERNAME/hermes-web-search-setup
```

或者手动克隆并安装：
1. 克隆本仓库到 `~/.hermes/skills/web-search-setup`。
2. 运行设置脚本：
   ```bash
   python setup.py
   ```

## 🛠️ 内容说明
- `setup.py`: 核心设置脚本，负责打补丁和配置。
- `SKILL.md`: Hermes Skill 定义文件。
- `references/`: 手动修复指南及相关文档。

## ⚠️ 注意
本工具会修改 Hermes 安装目录下的核心文件（补丁方式），建议在执行前备份相关的 Python 库文件。
