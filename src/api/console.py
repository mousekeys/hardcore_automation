import asyncio
from playwright.async_api import Page
from src.schemas.config_schema import AppConfig


class ConsoleMonitor:
    def __init__(self, page: Page, config: AppConfig):
        self.page = page
        self.config = config

    async def connect(self, on_log):
        """Connect to the terminal and expose a log callback."""
        await self.page.goto(self.config.server.url)
        await self.page.wait_for_selector(self.config.server.terminal_selector)
        await self.page.expose_function("onConsoleUpdate", on_log)
        await self._inject_observer()

    async def _inject_observer(self):
        selector = self.config.server.terminal_selector
        await self.page.evaluate(f"""
            const target = document.querySelector('{selector}');
            const observer = new MutationObserver(mutations => {{
                mutations.forEach(m => {{
                    if (m.addedNodes.length) window.onConsoleUpdate(m.addedNodes[0].innerText);
                }});
            }});
            observer.observe(target, {{ childList: true, subtree: true }});
        """)

    async def send_command(self, cmd: str):
        await self.page.fill('input[type="text"]', cmd)
        await self.page.keyboard.press("Enter")

    async def poll_commands(self, command_queue: asyncio.Queue):
        """Main loop — drains the command queue and forwards to console."""
        while True:
            if not command_queue.empty():
                cmd = command_queue.get_nowait()
                await self.send_command(cmd)
            await asyncio.sleep(0.5)