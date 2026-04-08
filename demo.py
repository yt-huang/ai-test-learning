#!/usr/bin/env python3
"""
browser-use demo 脚本
功能：自动搜索 browser-use GitHub 仓库并获取星标数量

需要先设置 API key:
export OPENAI_API_KEY="your-openai-key"
或者使用 browser-use 提供的 ChatBrowserUse()
"""

import asyncio
import os
from browser_use import Agent, Browser
from browser_use.sdk import ChatBrowserUse

async def main():
    # 创建浏览器实例，配置SSL证书错误处理
    browser = Browser(
        # 禁用安全检查，允许访问使用自签名证书的网站
        disable_security=True,
        # 传递Chrome命令行参数以忽略证书错误
        args=["--ignore-certificate-errors", "--ignore-ssl-errors"],
        # 非无头模式以便查看浏览器
        headless=False,
    )

    # 创建 Agent
    agent = Agent(
        task="Go to https://github.com/browser-use/browser-use and find the number of stars the repository has.",
        llm=ChatBrowserUse(),  # 使用 browser-use 提供的优化模型
        browser=browser,
    )

    # 运行任务
    result = await agent.run()
    print(f"\n✅ 任务完成！")
    print(f"📊 结果: {result}")

if __name__ == "__main__":
    # 检查 API key
    if not os.getenv("BROWSER_USE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  警告: 未设置 API key")
        print("请设置环境变量:")
        print("  export BROWSER_USE_API_KEY='your-key'  # 从 https://app.browser-use.com 获取")
        print("  或者")
        print("  export OPENAI_API_KEY='your-openai-key'")
        print("\n或者修改代码使用其他 LLM")
        exit(1)

    asyncio.run(main())
