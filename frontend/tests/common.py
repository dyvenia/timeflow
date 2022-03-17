import os

site_url = "http://localhost:8001/client/index.html"


async def click_admin_button(page):
    """Click the admin button in the sidebar"""
    # Assign admin button selector to variable
    btn_admin = (
        "#app > div > div:nth-child(1) > div > div > nav > div.relative > button"
    )
    await page.waitForSelector(btn_admin)
    await page.click(btn_admin)


async def click_clients_button(page):
    """Click the clients button in the sidebar once admin is clicked"""
    btn_clients = "#app > div > div:nth-child(1) > div > div > nav > div.relative > div > div > div > button:nth-child(7)"
    await page.waitForSelector(btn_clients)
    await page.click(btn_clients)


async def click_epic_areas_button(page):
    """Click the epic areas button in the sidebar once admin is clicked"""
    btn_epic_areas = "#app > div > div:nth-child(1) > div > div > nav > div.relative > div > div > div > button:nth-child(4)"
    await page.waitForSelector(btn_epic_areas)
    await page.click(btn_epic_areas)


async def click_epics_button(page):
    """Click the epics button in the sidebar once admin is clicked"""
    btn_epics = "#app > div > div:nth-child(1) > div > div > nav > div.relative > div > div > div > button:nth-child(3)"
    await page.waitForSelector(btn_epics)
    await page.click(btn_epics)


async def click_forecasts_button(page):
    """Click the forecasts button in the sidebar"""
    btn_forecasts = "#app > div > div:nth-child(1) > div > div > nav > div:nth-child(1) > button.block.px-4.py-2.mt-2.text-sm.font-semibold.text-gray-900.bg-transparent.rounded-lg.dark-mode\:bg-transparent.dark-mode\:hover\:bg-gray-600.dark-mode\:focus\:bg-gray-600.dark-mode\:focus\:text-white.dark-mode\:hover\:text-white.dark-mode\:text-gray-200.hover\:text-gray-900.focus\:text-gray-900.hover\:bg-gray-200.focus\:bg-gray-200.focus\:outline-none.focus\:shadow-outline"
    await page.waitForSelector(btn_forecasts)
    await page.click(btn_forecasts)


async def click_rates_button(page):
    """Click the rates button in the sidebar once admin is clicked."""
    # Assign rates button selector to variable
    btn_rates = "#app > div > div:nth-child(1) > div > div > nav > div.relative > div > div > div > button:nth-child(8)"
    await page.waitForSelector(btn_rates)
    await page.click(btn_rates)


async def click_roles_button(page):
    """Click the roles button in the sidebar once admin is clicked."""
    # Assign roles button selector to variable
    btn_roles = "#app > div > div:nth-child(1) > div > div > nav > div.relative > div > div > div > button:nth-child(2)"
    await page.waitForSelector(btn_roles)
    await page.click(btn_roles)


async def click_sponsors_button(page):
    """Click the sponsors button in the sidebar once admin is clicked."""
    # Assign sponsors button selector to variable
    btn_sponsors = "#app > div > div:nth-child(1) > div > div > nav > div.relative > div > div > div > button:nth-child(6)"
    await page.waitForSelector(btn_sponsors)
    await page.click(btn_sponsors)


async def click_teams_button(page):
    """Click the teams button in the sidebar"""
    # Assign teams button selector to variable
    btn_teams = "#app > div > div:nth-child(1) > div > div > nav > div.relative > div > div > div > button:nth-child(5)"
    await page.waitForSelector(btn_teams)
    await page.click(btn_teams)


async def click_timelogs_button(page):
    """Click the timelogs button in the sidebar"""
    # Assign timelogs button selector to variable
    btn_timelogs = "#app > div > div:nth-child(1) > div > div > nav > div:nth-child(1) > button.block.px-4.py-2.mt-2.text-sm.font-semibold.text-gray-900.bg-gray-200.rounded-lg.dark-mode\:bg-transparent.dark-mode\:hover\:bg-gray-600.dark-mode\:focus\:bg-gray-600.dark-mode\:focus\:text-white.dark-mode\:hover\:text-white.dark-mode\:text-gray-200.hover\:text-gray-900.focus\:text-gray-900.hover\:bg-gray-200.focus\:bg-gray-200.focus\:outline-none.focus\:shadow-outline"
    await page.waitForSelector(btn_timelogs)
    await page.click(btn_timelogs)


async def click_users_button(page):
    """Click the users button in the sidebar once admin is clicked."""
    # Assign users button selector to variable
    btn_users = "#app > div > div:nth-child(1) > div > div > nav > div.relative > div > div > div > button:nth-child(1)"
    await page.waitForSelector(btn_users)
    await page.click(btn_users)


def get_chrome_path():
    """Return the path to a chrome file that is supported by the given os"""
    # If windows
    if os.name == "nt":
        path = r"chromium\961656\chrome-win\chrome.exe"
        return path
    # If linux
    elif os.name == "posix":
        path = r"chromium\961656\chrome-linux\chrome"
        return path


async def screenshot(page, name: str):
    """Screenshot the page and store it in the screenshots directory"""
    path = f"screenshots/{name}.png"
    await page.screenshot({"path": path})
    print(f"Screenshot saved as: {name}.png")
