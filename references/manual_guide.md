# Manual Web Search Setup Guide for Hermes Agent

如果自动化脚本失败，请按照以下步骤手动配置。

## 1. 安装依赖
```bash
pip install duckduckgo-search
```

## 2. 补丁核心库 (Windows 必选)
找到你的 Hermes 安装路径（通常在 `site-packages/tools`）。

### A. 修复 SIGKILL 崩溃
编辑 `mcp_tool.py`，将：
```python
os.kill(pid, _signal.SIGKILL)
```
修改为：
```python
sig = getattr(_signal, 'SIGKILL', _signal.SIGTERM)
os.kill(pid, sig)
```

### B. 增加 DuckDuckGo 支持
编辑 `web_tools.py`：
1. 在 `_get_backend()` 函数中增加 `"ddg"`。
2. 在 `web_search_tool()` 中增加对 `backend == "ddg"` 的处理。
3. 实现 `_ddg_search()` 函数（使用 `duckduckgo_search` 库）。

## 3. 配置 Config
编辑 `~/.hermes/config.yaml`：
```yaml
web:
  backend: ddg
```

## 4. 验证
运行 `hermes doctor` 或 `hermes tools list`。
