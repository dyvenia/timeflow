import asyncio
import os
from pyppeteer import launch
from common import (
    click_forecasts_button,
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
    """Navigate to forecasts page"""
    await click_forecasts_button(page)

    await screenshot(page, "forecasts_main")


asyncio.run(main())
