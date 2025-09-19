import asyncio
import json
from playwright.async_api import async_playwright


async def scrape_popular_highlights(query, max_books=3):
    base_url = "https://www.amazon.com.au"
    search_url = f"{base_url}/s?k={query.replace(' ', '+')}&i=stripbooks"

    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Go to search page
        await page.goto(search_url)
        await page.wait_for_timeout(2000)

        # Grab book links
        links = []
        anchors = await page.query_selector_all("h2 a")
        for a in anchors[:max_books]:
            href = await a.get_attribute("href")
            if href and href.startswith("/"):
                links.append(base_url + href)

        # Visit each book
        for link in links:
            await page.goto(link)
            await page.wait_for_timeout(3000)

            # Title
            title = None
            el = await page.query_selector("#productTitle")
            if el:
                title = (await el.inner_text()).strip()

            # Author
            author = None
            el = await page.query_selector(".author a")
            if el:
                author = (await el.inner_text()).strip()

            # Highlights (Popular Highlights section)
            highlights = []
            els = await page.query_selector_all(".kp-notebook-highlight")
            for h in els:
                text = (await h.inner_text()).strip()
                if text:
                    highlights.append(text)

            for h in highlights:
                results.append({
                    "quote": h,
                    "author": author,
                    "book": title
                })

        await browser.close()

    return results


if __name__ == "__main__":
    query = "The Holy Grail of Investing"   # change this query to whatever you want
    data = asyncio.run(scrape_popular_highlights(query))
    print(json.dumps(data, indent=2, ensure_ascii=False))
