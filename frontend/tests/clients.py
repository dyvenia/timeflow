import asyncio
import os
from pyppeteer import launch
from common import (
    click_admin_button,
    click_clients_button,
    get_chrome_path,
    screenshot,
    site_url,
)


os.environ["PYPPETEER_CHROMIUM_REVISION"] = "961656"


async def main():
    chrome_path = get_chrome_path()
    browser = await launch(
        executablePath=chrome_path,
    )
    page = await browser.newPage()
    await page.setViewport({"width": 1280, "height": 720, "deviceScaleFactor": 2})
    await page.goto(site_url, {"waitUntil": "networkidle0"})

    await navigate_main(page)

    await browser.close()


async def navigate_main(page):
    """Navigate to clients page"""
    await click_admin_button(page)
    await click_clients_button(page)

    await screenshot(page, "clients_main")


asyncio.run(main())
