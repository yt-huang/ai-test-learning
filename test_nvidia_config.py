#!/usr/bin/env python3
"""
使用配置文件运行的 browser-use 测试
支持多配置文件，按优先级自动选择
"""

import asyncio
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI
from config_loader import get_nvidia_config


async def main():
    # 加载配置（自动尝试 .env.local -> .env -> config.json -> config.yaml -> 环境变量）
    config = get_nvidia_config()

    print(f"🤖 使用模型: {config['model']}")
    print(f"🌐 API 地址: {config['base_url']}")

    # 创建浏览器实例
    browser = Browser()

    # 使用加载的配置创建 LLM
    llm = ChatOpenAI(
        model=config['model'],
        api_key=config['api_key'],
        base_url=config['base_url'],
        temperature=config['temperature'],
    )

    # 创建 Agent
    agent = Agent(
        task="访问 https://github.com/browser-use/browser-use 并告诉我这个仓库有多少星标",
        llm=llm,
        browser=browser,
    )

    # 运行任务
    result = await agent.run()
    print(f"\n✅ 任务完成！")
    print(f"📊 结果: {result}")


if __name__ == "__main__":
    asyncio.run(main())
