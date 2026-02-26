import asyncio
from playwright.async_api import Page
from src.schemas.config_schema import AppConfig


class ServerController:
    def __init__(self, page: Page, config: AppConfig):
        self.page = page
        self.config = config

    async def stop(self):
        await self.page.goto(self.config.server.url)
        stop_btn = self.page.locator('button:has-text("Stop"), button:has-text("Kill")').first
        await stop_btn.click()
        print("Waiting for server to stop...")
        await asyncio.sleep(10)

    async def start(self):
        await self.page.goto(self.config.server.url)
        await self.page.click('button:has-text("Start")')
        print("Server is starting fresh!")

    async def delete_world(self):
        await self.page.goto(self.config.server.files_url)
        world_name = self.config.hardcore_plus.world_folder

        try:
            folder_link = self.page.get_by_role("cell", name=world_name, exact=True)
            world_row = self.page.locator("tr").filter(has=folder_link)
            await world_row.locator("button").last.click()
            await self.page.click('text=Delete')
            await self.page.click('text=Delete')
            print(f"Deleted folder: {world_name}")
        except Exception as e:
            print(f"Error deleting world: {e}")
            
    async def hardcore_reset(self):
        print("[HARDCORE PLUS] Player death detected! Resetting server...")
        await self.stop()
        await self.delete_world()
        await self.start()