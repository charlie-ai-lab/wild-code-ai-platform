import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 访问skills.sh
        await page.goto("https://skills.sh/", wait_until="networkidle")
        
        # 等待内容加载
        await page.wait_for_timeout(5000)
        
        # 获取页面内容
        content = await page.content()
        
        print(content)
        
        await browser.close()
        
        return content

if __name__ == "__main__":
    asyncio.run(main())
