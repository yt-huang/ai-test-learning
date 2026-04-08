#!/usr/bin/env python3
"""
browser-use demo - 使用 OpenAI 模型
需要先设置: export OPENAI_API_KEY="your-key"
"""

import asyncio
import os
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI

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

    # 使用 OpenAI 模型
    agent = Agent(
        task="搜索最新的人工智能新闻，总结3条最重要的",
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,
    )

    result = await agent.run()
    print(f"\n✅ 任务完成！")
    print(f"📊 结果: {result}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请先设置 OPENAI_API_KEY 环境变量")
        exit(1)
    asyncio.run(main())
