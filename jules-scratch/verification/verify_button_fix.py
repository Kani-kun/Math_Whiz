import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # --- Test 1: Main menu button functionality ---
        await page.goto("file:///app/index.html")

        try:
            # Click the "Timed Test" button for multiply/divide
            await page.click("#content-multiply-divide button:has-text('Timed Test')")

            # Wait for the game page to be visible
            await expect(page.locator("#game-page")).to_be_visible()
            await expect(page.locator("#game-title")).to_have_text("Multiply/Divide Test")

        except Exception as e:
            print(f"An error occurred: {e}")
            # Take a screenshot on failure
            await page.screenshot(path="jules-scratch/verification/error.png")

        # --- Test 2: Reward menu back button ---
        # Manually show the reward menu page to test its back button.
        await page.evaluate("showPage('reward-menu-page')")
        await expect(page.locator("#reward-menu-page")).to_be_visible()

        # Click the "Back to Main Menu" button.
        await page.locator("#reward-menu-page footer button").click()

        # Verify it navigates back to the home page.
        await expect(page.locator("#home-page")).to_be_visible()

        # Final screenshot of the home page after testing.
        await page.screenshot(path="jules-scratch/verification/verification.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())