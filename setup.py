import os
import sys
import re
import subprocess
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("hermes-search-setup")

def patch_file(path, search_pattern, replacement, description):
    if not os.path.exists(path):
        logger.error(f"File not found: {path}")
        return False
    
    try:
        content = Path(path).read_text(encoding="utf-8")
        if replacement.strip() in content:
            logger.info(f"✅ {description} already applied.")
            return True
        
        if search_pattern in content:
            new_content = content.replace(search_pattern, replacement)
            Path(path).write_text(new_content, encoding="utf-8")
            logger.info(f"🔧 {description} applied successfully.")
            return True
        else:
            logger.warning(f"⚠️ Could not find target pattern for: {description}")
            return False
    except Exception as e:
        logger.error(f"Failed to patch {path}: {e}")
        return False

def main():
    logger.info("🚀 Starting Hermes Web Search Setup...")

    # 1. 安装必要的 Python 库
    logger.info("📦 Step 1: Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "duckduckgo-search", "yaml"], check=False)
    except Exception as e:
        logger.error(f"Failed to install dependencies: {e}")

    # 2. 定位 Hermes 库路径
    try:
        import tools
        lib_path = Path(tools.__file__).parent
        web_tools_py = lib_path / "web_tools.py"
        mcp_tool_py = lib_path / "mcp_tool.py"
    except ImportError:
        logger.error("Could not find Hermes 'tools' module. Are you running this via Hermes?")
        return

    # 3. 应用代码补丁
    logger.info(f"🛠️ Step 2: Patching Hermes core files at {lib_path}...")

    # 补丁 1: 修复 Windows SIGKILL 崩溃
    patch_file(
        mcp_tool_py,
        "os.kill(pid, _signal.SIGKILL)",
        "sig = getattr(_signal, 'SIGKILL', _signal.SIGTERM)\n            os.kill(pid, sig)",
        "Windows SIGKILL Fix"
    )

    # 补丁 2: 在 web_tools.py 中增加 DDG 支持 (部分关键补丁)
    if not patch_file(
        web_tools_py,
        'if configured in ("parallel", "firecrawl", "tavily", "exa"):',
        'if configured in ("parallel", "firecrawl", "tavily", "exa", "ddg"):',
        "Enable 'ddg' as valid backend"
    ):
        # 兼容性检查：如果已经是最新版或已被修改
        pass
    
    # 补丁 3: 注入 _ddg_search 函数
    ddg_search_func = """
def _ddg_search(query: str, limit: int = 5) -> dict:
    \"\"\"Search using DuckDuckGo (no key required) and return results as a dict.\"\"\"
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(keywords=query, max_results=limit)]
            web_results = []
            for i, r in enumerate(results):
                web_results.append({
                    "url": r.get("href", ""),
                    "title": r.get("title", ""),
                    "description": r.get("body", ""),
                    "position": i + 1,
                })
            return {"success": True, "data": {"web": web_results}}
    except Exception as e:
        return {"success": False, "error": str(e)}

"""
    if "_ddg_search" not in web_tools_py.read_text(encoding="utf-8"):
        with open(web_tools_py, "a", encoding="utf-8") as f:
            f.write(ddg_search_func)
        logger.info("🔧 Injected _ddg_search implementation.")

    # 4. 更新 config.yaml
    logger.info("📝 Step 3: Updating config.yaml...")
    hermes_home = Path(os.path.expanduser("~/.hermes"))
    config_path = hermes_home / "config.yaml"
    if config_path.exists():
        try:
            content = config_path.read_text(encoding="utf-8")
            if "backend: ddg" not in content:
                # 简单替换或正则替换
                new_content = re.sub(r"backend:.*", "backend: ddg", content)
                config_path.write_text(new_content, encoding="utf-8")
                logger.info("✅ Set web.backend to 'ddg' in config.yaml.")
        except Exception as e:
            logger.error(f"Failed to update config: {e}")

    logger.info("\n✨ Setup complete! Hermes Agent is now search-ready.")
    logger.info("建议运行 'hermes tools list' 确认 web 工具已启用。")

if __name__ == "__main__":
    main()
