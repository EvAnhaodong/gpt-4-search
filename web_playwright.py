"""Web scraping commands using Playwright"""
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "Playwright not installed. Please install it with 'pip install playwright' to use."
    )
from bs4 import BeautifulSoup

def scrape_text(url: str) -> str:
    """Scrape text from a webpage

    Args:
        url (str): The URL to scrape text from

    Returns:
        str: The scraped text
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            page.goto(url)
            html_content = page.content()
            soup = BeautifulSoup(html_content, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

        except Exception as e:
            text = f"Error: {str(e)}"

        finally:
            browser.close()

    return [text[i:i+900] for i in range(0,len(text)-900,800)]


def scrape_links(url: str) -> str | list[str]:
    """Scrape links from a webpage

    Args:
        url (str): The URL to scrape links from

    Returns:
        Union[str, List[str]]: The scraped links
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            page.goto(url)
            html_content = page.content()
            soup = BeautifulSoup(html_content, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            hyperlinks = extract_hyperlinks(soup, url)
            formatted_links = format_hyperlinks(hyperlinks)

        except Exception as e:
            formatted_links = f"Error: {str(e)}"

        finally:
            browser.close()

    return formatted_links

"""HTML processing functions"""
from requests.compat import urljoin


def extract_hyperlinks(soup: BeautifulSoup, base_url: str) -> list[tuple[str, str]]:
    """Extract hyperlinks from a BeautifulSoup object

    Args:
        soup (BeautifulSoup): The BeautifulSoup object
        base_url (str): The base URL

    Returns:
        List[Tuple[str, str]]: The extracted hyperlinks
    """
    return [
        (link.text, urljoin(base_url, link["href"]))
        for link in soup.find_all("a", href=True)
    ]


def format_hyperlinks(hyperlinks: list[tuple[str, str]]) -> list[str]:
    """Format hyperlinks to be displayed to the user

    Args:
        hyperlinks (List[Tuple[str, str]]): The hyperlinks to format

    Returns:
        List[str]: The formatted hyperlinks
    """
    return [f"{link_text} ({link_url})" for link_text, link_url in hyperlinks]

if __name__ == "__main__":
    url="https://www.google.com/finance/quote/300676:SHE"
    print(scrape_text(url))
