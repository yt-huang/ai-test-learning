# Browser-Use 学习笔记

## 简介

browser-use 是一个开源的 AI 浏览器自动化工具，可以让 AI 代理像人类一样操作浏览器完成各种任务。

**核心功能:**
- 自动填写表单
- 网上购物
- 个人助理任务
- 数据抓取
- 网页自动化测试

## 安装步骤

```bash
# 1. 安装 uv (如果未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安装 Python 3.11+
uv python install 3.11
uv python pin 3.11

# 3. 初始化项目
uv init

# 4. 安装 browser-use 和 playwright
uv add browser-use playwright

# 5. 安装 Chromium 浏览器
uv run playwright install chromium
```

## 快速开始

### 方式1: 使用 browser-use 官方模型 (推荐)

```python
from browser_use import Agent, Browser
from browser_use.sdk import ChatBrowserUse
import asyncio

async def main():
    browser = Browser()
    agent = Agent(
        task="访问 github.com/browser-use/browser-use 获取星标数",
        llm=ChatBrowserUse(),  # 官方优化模型，速度提升3-5倍
        browser=browser,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

**定价:**
- Input: $0.20/1M tokens
- Output: $2.00/1M tokens

### 方式2: 使用 OpenAI

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser

agent = Agent(
    task="你的任务描述",
    llm=ChatOpenAI(model="gpt-4o"),
    browser=browser,
)
```

### 方式3: 使用其他模型

支持多种 LLM:
- Anthropic (Claude)
- Google (Gemini)
- Groq
- Ollama (本地模型)
- Azure OpenAI

## 核心 API

### Agent

```python
Agent(
    task="任务描述",           # 必需 - AI要完成的任务
    llm=llm_instance,          # 必需 - 语言模型实例
    browser=browser,           # 可选 - 浏览器实例
    use_vision=True,           # 可选 - 启用视觉能力
    save_conversation_path="", # 可选 - 保存对话记录
)
```

### Browser

```python
browser = Browser(
    use_cloud=True,  # 使用云端浏览器
)

# 常用方法
await browser.open("https://example.com")
await browser.click("selector")
await browser.type("selector", "text")
await browser.screenshot()
await browser.close()
```

### CLI 命令

```bash
# 打开网页
browser-use open https://example.com

# 获取页面状态
browser-use state

# 点击元素
browser-use click "button#submit"

# 输入文本
browser-use type "input#search" "search text"

# 截图
browser-use screenshot

# 关闭浏览器
browser-use close
```

## 高级用法

### 使用云端浏览器

```python
browser = Browser(use_cloud=True)
```

### 启用视觉能力

```python
agent = Agent(
    task="任务描述",
    llm=llm,
    browser=browser,
    use_vision=True,  # 启用视觉理解
)
```

### 保存对话记录

```python
agent = Agent(
    task="任务描述",
    llm=llm,
    save_conversation_path="conversation.json",
)
```

## 运行 Demo

```bash
# 使用 browser-use 官方模型
export BROWSER_USE_API_KEY="your-key"
uv run python demo.py

# 使用 OpenAI
export OPENAI_API_KEY="your-key"
uv run python demo_openai.py
```

## 获取 API Key

1. **browser-use**: https://app.browser-use.com
2. **OpenAI**: https://platform.openai.com

## 参考资料

- GitHub: https://github.com/browser-use/browser-use
- 文档: https://docs.browser-use.com
- 社区: Discord 服务器
