import os
from playwright.async_api import async_playwright, Page, Browser
from dotenv import load_dotenv
from src.schemas.config_schema import AppConfig

load_dotenv()


class BrowserSession:
    def __init__(self, config: AppConfig):
        self.config = config
        self._playwright = None
        self._browser: Browser | None = None
        self.page: Page | None = None

    async def start(self) -> Page:
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=True)
        self.page = await self._browser.new_page()
        return self.page

    async def login(self):
        await self.page.goto(self.config.auth.login_url)
        await self.page.fill('input[name="email"]', os.getenv("EMAIL"))
        await self.page.fill('input[name="password"]', os.getenv("PASSWORD"))
        await self.page.click('button[type="submit"]')
        await self.page.wait_for_url(self.config.auth.panel_url)

    async def stop(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()