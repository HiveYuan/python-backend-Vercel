import asyncio
import os
from typing import Any, Optional

from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import NoExtractionStrategy
from dotenv import load_dotenv
from openai import OpenAI

from .base_tool import Tool

load_dotenv()


class WebCrawler(Tool):
    """
    网页爬虫工具，支持从任何URL提取和分析网页内容
    
    功能特点：
    - 智能网页内容抓取
    - 自动转换为markdown格式
    - 使用GPT-4o进行内容优化和提取
    - 支持异步操作
    - 处理各种网页类型和动态内容
    """
    
    name: str = "web_crawler"
    description: str = """
获取网页内容的工具，支持从任何URL提取和分析网页内容。

功能特点：
- 智能网页内容抓取
- 自动转换为markdown格式
- 使用GPT-4o进行内容优化和提取
- 支持异步操作
- 处理各种网页类型和动态内容

输入参数：
- url: 要抓取的网页URL（必需）

返回：
- 网页内容的markdown格式文本
""".strip()

    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "要抓取内容的网页URL",
                "format": "uri"
            }
        },
        "required": ["url"]
    }
    
    # OpenAI客户端实例
    openai_client: Optional[OpenAI] = None
    
    class Config:
        arbitrary_types_allowed = True

    def __init__(self):
        super().__init__()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("未找到OPENAI_API_KEY环境变量，请检查.env文件")
        
        self.openai_client = OpenAI(api_key=api_key)

    def execute(self, **kwargs) -> str:
        """同步执行方法，内部调用异步方法"""
        url = kwargs.get("url")
        if not url:
            return "错误：未提供URL参数"
        
        try:
            return asyncio.run(self.aexecute(url=url))
        except Exception as e:
            return f"执行失败：{str(e)}"

    async def aexecute(self, **kwargs) -> str:
        """异步执行网页抓取"""
        url = kwargs.get("url")
        if not url:
            return "错误：未提供URL参数"

        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            async with AsyncWebCrawler(verbose=False) as crawler:
                result = await crawler.arun(
                    url=url,
                    extraction_strategy=NoExtractionStrategy(),
                    excluded_tags=['script', 'style', 'nav', 'footer', 'header'],
                    wait_for_selector="body",
                    page_timeout=30000
                )

                if not result.success:
                    return f"网页抓取失败：{result.error_message}"

                content = result.markdown
                if not content or len(content.strip()) < 50:
                    return "错误：未能提取到有效的网页内容"

                optimized_content = await self._optimize_content_with_gpt(content, url)
                return optimized_content

        except Exception as e:
            return f"网页抓取错误：{str(e)}"

    async def _optimize_content_with_gpt(self, content: str, url: str) -> str:
        """使用GPT-4o优化提取的内容"""
        try:
            max_content_length = 80000
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """你是一个专业的内容提取助手。请从提供的网页内容中提取最重要和有用的信息，并以清晰的markdown格式返回。

要求：
1. 保留标题结构和层次
2. 提取主要内容和关键信息
3. 移除广告、导航、版权声明等无关内容
4. 保持内容的逻辑性和可读性
5. 如果是新闻文章，保留标题、时间、作者、正文
6. 如果是产品页面，保留产品名称、描述、规格等
7. 使用中文回复（除非原内容是其他语言）"""
                    },
                    {
                        "role": "user", 
                        "content": f"请优化以下从网页 {url} 提取的内容：\n\n{content}"
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )

            optimized_content = response.choices[0].message.content
            return optimized_content or content

        except Exception as e:
            return f"内容优化失败，返回原始内容：\n\n{content}\n\n错误：{str(e)}"
