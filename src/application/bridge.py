import yaml
import asyncio
from playwright.async_api import async_playwright
import re
from dotenv import load_dotenv
import os


load_dotenv()  

# Load the YAML configuration
with open("../config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

async def hardcore_plus_reset(page):
    """Stops server, deletes world folder, and restarts."""
    print("[HARDCORE PLUS] Player death detected! Resetting server...")
    
    # 1. STOP SERVER
    await page.goto(cfg['server']['url'])
    # Try clicking 'Stop', if not responsive, try 'Kill'
    stop_btn = page.locator('button:has-text("Stop"), button:has-text("Kill")').first
    await stop_btn.click()
    print("Waiting for server to stop...")
    await asyncio.sleep(10) 

    # 2. DELETE WORLD
    await page.goto(cfg['server']['files_url'])
    world_name = cfg['hardcore_plus']['world_folder']
    try:
        # Locate the row with the world folder and click its action menu
        folder_link = page.get_by_text(world_name, exact=True)
        world_row = page.locator("tr").filter(has=folder_link)
        await world_row.locator('button').last.click()
        await page.click('text=Delete')
        await page.click('button:has-text("Delete files")')
        print(f"Deleted folder: {world_name}")
    except Exception as e:
        print(f"Error deleting world: {e}")
        
   

    # 3. START SERVER
    await page.goto(cfg['server']['url'])
    await page.click('button:has-text("Start")')
    print("Server is starting fresh!")

async def start_browser_bridge(log_callback, command_queue):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Login
        await page.goto("https://www.powerupstack.com/auth/login")
        await page.fill('input[name="email"]', os.getenv("EMAIL"))
        await page.fill('input[name="password"]',os.getenv("PASSWORD"))
        await page.click('button[type="submit"]')
        await page.wait_for_url("https://www.powerupstack.com/panel/instances")

        # Connect to Console
        await page.goto(cfg['server']['url'])
        await page.wait_for_selector(cfg['server']['terminal_selector'])

        # Log Processor
        async def process_logs(text):
            await log_callback(text) # Update UI
            
            # Death Check
            if any(k in text.lower() for k in cfg['hardcore_plus']['death_keywords']):
                await hardcore_plus_reset(page)

        await page.expose_function("onConsoleUpdate", process_logs)

        # Inject MutationObserver (with escaped braces for f-string)
        await page.evaluate(f"""
            const target = document.querySelector('{cfg['server']['terminal_selector']}');
            const observer = new MutationObserver(mutations => {{
                mutations.forEach(m => {{
                    if(m.addedNodes.length) window.onConsoleUpdate(m.addedNodes[0].innerText);
                }});
            }});
            observer.observe(target, {{ childList: true, subtree: true }});
        """)

        # Main Loop for UI commands
        while True:
            if not command_queue.empty():
                cmd = command_queue.get_nowait()
                await page.fill('input[type="text"]', cmd)
                await page.keyboard.press("Enter")
            await asyncio.sleep(0.5)