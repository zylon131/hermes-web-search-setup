---
name: web-search-setup
description: 自动配置 Hermes Agent 联网搜索能力（集成 DuckDuckGo，无需 API Key）。
version: 1.0.0
---

# Web Search Setup Skill

这个 Skill 旨在帮助 Hermes Agent 获取联网搜索能力。它通过在本地安装 `duckduckgo-search` 并补丁 Hermes 的核心库来实现无需 API Key 的搜索。

## 功能
1. **自动安装依赖**：安装 `duckduckgo-search`。
2. **核心库补丁**：
   - 修复 Windows 下的 `SIGKILL` 崩溃问题。
   - 在 `web_tools.py` 中注入 DuckDuckGo 后端驱动。
3. **配置更新**：将 `config.yaml` 中的搜索后端设置为 `ddg`。

## 如何使用
你可以直接让 Hermes 运行以下命令来执行设置：

```bash
python C:\Users\admin\.hermes\skills\web-search-setup\setup.py
```

执行后，Hermes 将具备内置的 `web_search` 能力。

## 注意事项
- 本 Skill 会修改 Hermes 的 site-packages 代码以支持新后端。
- 配置完成后，建议重启 Hermes 终端。
