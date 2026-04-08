#!/usr/bin/env python3
"""
browser-use demo - 使用 NVIDIA API + kimi-k2.5 模型
API 地址: https://integrate.api.nvidia.com
模型: moonshotai/kimi-k2.5
"""

import asyncio
import os
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI

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

    # 配置 NVIDIA API
    llm = ChatOpenAI(
        model="moonshotai/kimi-k2.5",
        api_key="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",
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.7,
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
