#!/usr/bin/env python3
"""
用户管理测试用例
功能：
1. 使用 admin 账号登录系统
2. 进入 users 模块
3. 创建新用户 test002
4. 退出登录
5. 使用 test002 登录验证

配置来源（按优先级）：.env.local -> .env -> config.json -> 环境变量
LLM 自动降级：按 .env 中配置顺序依次尝试，主 LLM 失败时自动 fallback
"""

import asyncio
import os
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI
from browser_use.llm.deepseek.chat import ChatDeepSeek

# ── LLM 提供商注册表 ──
# 新增提供商只需在此追加一项，无需改动其他代码
PROVIDERS = [
    {
        "name": "DeepSeek",
        "env_prefix": "DEEPSEEK",
        "llm_class": ChatDeepSeek,
        "defaults": {
            "BASE_URL": "https://api.deepseek.com/v1",
            "MODEL": "deepseek-chat",
        },
        "use_vision": False,
    },
    {
        "name": "Kimi (Moonshot)",
        "env_prefix": "KIMI",
        "llm_class": ChatOpenAI,
        "defaults": {
            "BASE_URL": "https://api.moonshot.cn/v1",
            "MODEL": "kimi-k2.5",
        },
        "extra_params": {
            "temperature": 1,
            "frequency_penalty": None,
            "remove_min_items_from_schema": True,
            "remove_defaults_from_schema": True,
        },
        "use_vision": True,
    },
    {
        "name": "NVIDIA",
        "env_prefix": "NVIDIA",
        "llm_class": ChatOpenAI,
        "defaults": {
            "BASE_URL": "https://integrate.api.nvidia.com/v1",
            "MODEL": "moonshotai/kimi-k2.5",
        },
        "use_vision": True,
    },
]


def _load_raw_env():
    """从 .env.local / .env / config.json / 环境变量 汇总所有原始配置"""
    from pathlib import Path
    import json

    raw = {}

    for env_file in [".env.local", ".env"]:
        if Path(env_file).exists():
            print(f"📄 加载配置: {env_file}")
            with open(env_file, "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#") and "=" in line:
                        k, v = line.strip().split("=", 1)
                        raw.setdefault(k, v.strip().strip("\"'"))

    if Path("config.json").exists():
        print("📄 加载配置: config.json")
        with open("config.json", "r") as f:
            data = json.load(f)
            for section_name, section_data in data.items():
                if isinstance(section_data, dict):
                    prefix = section_name.upper()
                    for field in ["api_key", "base_url", "model"]:
                        if field in section_data:
                            raw.setdefault(f"{prefix}_{field.upper()}", section_data[field])

    for provider in PROVIDERS:
        prefix = provider["env_prefix"]
        for suffix in ["API_KEY", "BASE_URL", "MODEL"]:
            key = f"{prefix}_{suffix}"
            if key not in raw and os.getenv(key):
                raw[key] = os.getenv(key)

    return raw


def _create_llm(provider_cfg, raw):
    """根据提供商配置和原始环境变量，创建 LLM 实例。无 API Key 则返回 None。"""
    prefix = provider_cfg["env_prefix"]
    api_key = raw.get(f"{prefix}_API_KEY")
    if not api_key:
        return None

    defaults = provider_cfg.get("defaults", {})
    base_url = raw.get(f"{prefix}_BASE_URL", defaults.get("BASE_URL"))
    model = raw.get(f"{prefix}_MODEL", defaults.get("MODEL"))

    params = {"model": model, "api_key": api_key, "base_url": base_url}
    params.update(provider_cfg.get("extra_params", {}))

    return provider_cfg["llm_class"](**params)


def build_llms():
    """按优先级构建可用 LLM 列表，返回 [(name, llm_instance, use_vision), ...]"""
    raw = _load_raw_env()
    available = []
    for provider in PROVIDERS:
        llm = _create_llm(provider, raw)
        if llm:
            available.append((provider["name"], llm, provider.get("use_vision", True)))
    return available


async def test_user_management():
    """完整的用户管理测试流程"""

    llms = build_llms()
    if not llms:
        print("❌ 未找到任何可用的 API Key")
        print("请在 .env.local 中配置至少一个提供商的 API Key")
        return

    primary_name, primary_llm, primary_vision = llms[0]
    fallback_llm = llms[1][1] if len(llms) > 1 else None

    print(f"\n🤖 主 LLM: {primary_name} ({primary_llm.name}), vision={primary_vision}")
    if fallback_llm:
        print(f"🔄 备用 LLM: {llms[1][0]} ({fallback_llm.name})")
    else:
        print("⚠️  无备用 LLM，建议配置多个提供商")

    # keep_alive=True 防止 Agent 结束时销毁浏览器会话，保证多步骤共享同一浏览器
    browser = Browser(disable_security=True, keep_alive=True)

    # 测试步骤定义
    steps = [
        (
            "步骤1: 使用 admin 账号登录系统",
            """
访问 https://192.168.137.193/ 登录页面，执行以下操作：
1. 等待页面加载完成
2. 在邮箱/用户名输入框中输入: admin@cpaas.io
3. 在密码输入框中输入: 07Apples@
4. 点击登录按钮
5. 等待登录成功，验证是否进入了系统主页面
""",
        ),
        (
            "步骤2: 进入 Users 用户管理模块",
            """
需要找到左上角菜单栏点击进入Administrator模块，然后点击Users/用户管理 模块：
在系统主页面中找到并点击 Users/用户管理 模块：
1. 查找左侧导航栏或顶部菜单中的 "Users" 或 "用户" 选项
2. 点击该选项进入用户管理页面
3. 等待用户列表页面加载完成
4. 确认页面显示了用户列表或用户管理相关界面
""",
        ),
        (
            "步骤3: 创建新用户 test002",
            """
在用户管理页面创建新用户：
1. 查找并点击 "Create User"/"Add User"/"新建用户"/"+" 按钮
2. 在用户名/邮箱输入框中输入: test002
3. 如果要求输入邮箱，输入: test002@example.com
4. 在密码输入框中输入: 07Apples@
5. 在确认密码输入框中输入: 07Apples@
6. 根据页面要求填写其他必填字段（如姓名、角色等）
7. 点击 "Create"/"Save"/"创建" 按钮提交
8. 等待创建成功的提示信息
9. 确认新用户 test002 出现在用户列表中
""",
        ),
        (
            "步骤4: 退出当前账号",
            """
退出当前登录账号：
1. 查找用户头像、用户名或右上角的用户菜单
2. 点击打开用户下拉菜单
3. 查找并点击 "Logout"/"Sign Out"/"退出登录" 选项
4. 等待页面跳转到登录页面
5. 确认已成功退出，看到登录表单
""",
        ),
        (
            "步骤5: 使用 test002 登录验证",
            """
使用新创建的 test002 账号登录系统：
1. 确认当前在登录页面 https://192.168.137.193/
2. 在邮箱/用户名输入框中输入: test002
3. 在密码输入框中输入: 07Apples@
4. 点击登录按钮
5. 等待登录完成
6. 验证是否成功登录进入系统主页面
7. 确认页面显示了 test002 用户信息或相关仪表板
""",
        ),
    ]

    try:
        for title, task in steps:
            print(f"\n{'=' * 50}")
            print(title)
            print("=" * 50)

            agent = Agent(
                task=task,
                llm=primary_llm,
                fallback_llm=fallback_llm,
                browser=browser,
                use_vision=primary_vision,
            )
            result = await agent.run()
            print(f"✅ {title} 完成")

        print(f"\n{'=' * 50}")
        print("🎉 所有测试步骤执行完成！")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 测试执行出错: {e}")
        raise
    finally:
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_user_management())
