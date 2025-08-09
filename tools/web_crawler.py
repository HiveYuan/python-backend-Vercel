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
    Web crawler tool that supports extracting and analyzing web content from any URL
    
    Features:
    - Intelligent web content extraction
    - Automatic conversion to markdown format
    - Content optimization and extraction using GPT-4o
    - Supports asynchronous operations
    - Handles various web page types and dynamic content
    """
    
    name: str = "web_crawler"
    description: str = """
Web content extraction tool that supports extracting and analyzing web content from any URL.

Features:
- Intelligent web content extraction
- Automatic conversion to markdown format
- Content optimization and extraction using GPT-4o
- Supports asynchronous operations
- Handles various web page types and dynamic content

Input parameters:
- url: The web page URL to crawl (required)

Returns:
- Web content in markdown format
""".strip()

    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The web page URL to extract content from",
                "format": "uri"
            }
        },
        "required": ["url"]
    }
    
    # OpenAI client instance
    openai_client: Optional[OpenAI] = None
    
    class Config:
        arbitrary_types_allowed = True

    def __init__(self):
        super().__init__()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not found, please check .env file")
        
        self.openai_client = OpenAI(api_key=api_key)

    def execute(self, **kwargs) -> str:
        """Synchronous execution method that internally calls the asynchronous method"""
        url = kwargs.get("url")
        if not url:
            return "Error: URL parameter not provided"
        
        try:
            return asyncio.run(self.aexecute(url=url))
        except Exception as e:
            return f"Execution failed: {str(e)}"

    async def aexecute(self, **kwargs) -> str:
        """Asynchronously execute web crawling"""
        url = kwargs.get("url")
        if not url:
            return "Error: URL parameter not provided"

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
                    return f"Web crawling failed: {result.error_message}"

                content = result.markdown
                if not content or len(content.strip()) < 50:
                    return "Error: Failed to extract valid web content"

                optimized_content = await self._optimize_content_with_gpt(content, url)
                return optimized_content

        except Exception as e:
            return f"Web crawling error: {str(e)}"

    async def _optimize_content_with_gpt(self, content: str, url: str) -> str:
        """Optimize extracted content using GPT-4o"""
        try:
            max_content_length = 80000
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a professional content extraction assistant. Please extract the most important and useful information from the provided web content and return it in clear markdown format.

Requirements:
1. Preserve title structure and hierarchy
2. Extract main content and key information
3. Remove ads, navigation, copyright notices and other irrelevant content
4. Maintain logical and readable content
5. For news articles, retain title, date, author, and body text
6. For product pages, retain product name, description, specifications, etc.
7. Respond in the same language as the original content"""
                    },
                    {
                        "role": "user", 
                        "content": f"Please optimize the following content extracted from webpage {url}:\n\n{content}"
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )

            optimized_content = response.choices[0].message.content
            return optimized_content or content

        except Exception as e:
            return f"Content optimization failed, returning original content:\n\n{content}\n\nError: {str(e)}"
