import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import asyncio
from src.api.browser import BrowserSession
from src.api.server import ServerController
from src.api.console import ConsoleMonitor
from src.config_loader import get_config



async def start_browser_bridge(log_callback, command_queue: asyncio.Queue):
    config = get_config()

    session = BrowserSession(config)
    page = await session.start()

    try:
        await session.login()

        server = ServerController(page, config)
        console = ConsoleMonitor(page, config)

        async def process_log(text: str):
            await log_callback(text)
            if any(k in text.lower() for k in config.hardcore_plus.death_keywords):
                await server.hardcore_reset()

        await console.connect(process_log)
        await console.poll_commands(command_queue)

    finally:
        await session.stop()