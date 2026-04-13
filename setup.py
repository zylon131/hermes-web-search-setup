"""
Hermes Web Search Setup Script

自动配置 Hermes Agent 联网搜索能力。
支持 Tavily（推荐）和 DuckDuckGo（备用）后端。

用法:
    python setup.py          # 完整配置（Tavily + 修复 .env 加载）
    python setup.py --check  # 仅检查当前配置状态
"""
import os
import sys
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("hermes-search-setup")

SITE_PACKAGES_TOOLS = Path(sys.prefix) / "Lib" / "site-packages" / "tools"
HERMES_ENV = Path.home() / ".hermes" / ".env"
CONFIG_YAML = Path.home() / ".hermes" / "config.yaml"


def get_hermes_tools_path():
    """Locate the tools directory in site-packages."""
    # Try to import tools directly first
    try:
        import tools
        return Path(tools.__file__).parent
    except ImportError:
        pass

    # Fallback: search in site-packages
    for sp in sys.path:
        tools_dir = Path(sp) / "tools"
        if tools_dir.exists() and (tools_dir / "web_tools.py").exists():
            return tools_dir

    return SITE_PACKAGES_TOOLS


def patch_file(path, search_pattern, replacement, description):
    """Apply a patch to a file if the pattern is found and patch not already applied."""
    if not os.path.exists(path):
        logger.error(f"File not found: {path}")
        return False

    try:
        content = Path(path).read_text(encoding="utf-8")
        if replacement.strip() in content:
            logger.info(f"[OK] {description} already applied.")
            return True

        if search_pattern in content:
            new_content = content.replace(search_pattern, replacement)
            Path(path).write_text(new_content, encoding="utf-8")
            logger.info(f"[PATCHED] {description}")
            return True
        else:
            logger.warning(f"[SKIP] Could not find target pattern for: {description}")
            return False
    except Exception as e:
        logger.error(f"Failed to patch {path}: {e}")
        return False


def check_tavily_config():
    """Check if Tavily is properly configured."""
    import yaml

    # Check .env
    env_key = None
    if HERMES_ENV.exists():
        for line in HERMES_ENV.read_text(encoding="utf-8").splitlines():
            if line.startswith("TAVILY_API_KEY="):
                env_key = line.split("=", 1)[1].strip()
                break

    # Check config.yaml - use yaml parser for accuracy
    backend = None
    if CONFIG_YAML.exists():
        try:
            content = CONFIG_YAML.read_text(encoding="utf-8")
            cfg = yaml.safe_load(content)
            backend = cfg.get("web", {}).get("backend")
        except Exception:
            pass

    return env_key, backend


def check_env_loading_patch(web_tools_py):
    """Check if the .env auto-load patch is applied."""
    if not web_tools_py.exists():
        return False
    content = web_tools_py.read_text(encoding="utf-8")
    return 'load_dotenv(_hermes_env' in content


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hermes Web Search Setup")
    parser.add_argument("--check", action="store_true", help="Only check current config status")
    args = parser.parse_args()

    web_tools_py = get_hermes_tools_path() / "web_tools.py"

    # Check mode
    if args.check:
        logger.info("=== Hermes Web Search Configuration Check ===")
        env_key, backend = check_tavily_config()
        logger.info(f"  TAVILY_API_KEY in ~/.hermes/.env: {'Yes (hidden)' if env_key else 'No'}")
        logger.info(f"  web.backend in config.yaml: {backend or 'Not set'}")
        logger.info(f"  .env auto-load patch: {'Yes' if check_env_loading_patch(web_tools_py) else 'No'}")
        return

    logger.info("=== Hermes Web Search Setup ===")

    # Step 1: Check if Tavily API key is provided via env
    env_key, backend = check_tavily_config()
    use_tavily = bool(env_key)

    if use_tavily:
        logger.info(f"[INFO] Tavily API key found in ~/.hermes/.env")
        logger.info("[INFO] Tavily is the preferred backend")

        # Step 2: Ensure .env auto-load patch is applied
        logger.info(f"[PATCH] Ensuring .env auto-load in {web_tools_py}...")

        dotenv_patch = '''from tools.website_policy import check_website_access

logger = logging.getLogger(__name__)

# Load Hermes .env so API keys are available in subprocess / MCP contexts
try:
    from pathlib import Path
    from dotenv import load_dotenv
    _hermes_env = Path.home() / ".hermes" / ".env"
    if _hermes_env.exists():
        load_dotenv(_hermes_env, override=True, encoding="utf-8")
except Exception:
    pass


# ─── Backend Selection ────────────────────────────────────────────────────────'''

        dotenv_search = '''from tools.website_policy import check_website_access

logger = logging.getLogger(__name__)


# ─── Backend Selection ────────────────────────────────────────────────────────'''

        patch_file(str(web_tools_py), dotenv_search, dotenv_patch, ".env auto-load patch")

        # Step 3: Ensure config.yaml has tavily backend
        if backend != "tavily" and CONFIG_YAML.exists():
            import yaml
            content = CONFIG_YAML.read_text(encoding="utf-8")
            cfg = yaml.safe_load(content)
            cfg.setdefault("web", {})["backend"] = "tavily"
            CONFIG_YAML.write_text(yaml.dump(cfg), encoding="utf-8")
            logger.info("[PATCHED] Set web.backend to 'tavily' in config.yaml")

    else:
        logger.info("[INFO] No Tavily API key found")
        logger.info("[INFO] DuckDuckGo MCP server will be used as fallback")
        logger.info("[INFO] To use Tavily, add TAVILY_API_KEY to ~/.hermes/.env")

    logger.info("\n=== Setup Complete ===")
    logger.info("Run: hermes tools list | grep web")


if __name__ == "__main__":
    main()
