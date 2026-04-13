---
name: web-search-setup
description: 自动配置 Hermes Agent 联网搜索能力（支持 Tavily、DuckDuckGo 等后端）。
version: 1.2.0
---

# Web Search Setup Skill

这个 Skill 旨在帮助 Hermes Agent 获取联网搜索能力。支持多种后端：
- **Tavily** (推荐，需 API Key，https://app.tavily.com)
- **DuckDuckGo** (无需 API Key，免费)

## 功能
1. **自动加载 .env**：确保 API Key 在所有上下文中可用
2. **配置验证**：检查 config.yaml 和 .env 配置
3. **多后端支持**：Tavily（推荐）或 DuckDuckGo（备用）

## 如何使用
你可以直接让 Hermes 运行以下命令来执行设置：

```bash
python C:\Users\admin\.hermes\skills\web-search-setup\setup.py
```

执行后，Hermes 将具备内置的 `web_search` 能力。

## 搜索后端配置

### 方式一：Tavily（推荐）
```bash
# 1. 添加 API Key 到 ~/.hermes/.env
echo "TAVILY_API_KEY=你的key" >> ~/.hermes/.env

# 2. 修改 config.yaml 中的 backend
# 编辑 ~/.hermes/config.yaml，将 web.backend 改为 tavily
```

### 方式二：DuckDuckGo（无需 API Key）
```bash
# 直接修改 config.yaml
web:
  backend: ddg
```

## 配置文件位置
- 配置: `~/.hermes/config.yaml` (控制 `web.backend`)
- 环境变量: `~/.hermes/.env` (存储 API Keys)

## 验证
```bash
hermes tools list | grep web
```

## 已知问题
- 如果 Tavily 搜索失败（返回空结果或错误），检查 `TAVILY_API_KEY` 是否在 `~/.hermes/.env` 中正确配置
- 备用方案：DuckDuckGo MCP server 已默认启用，可在 Tavily 不可用时自动回退
