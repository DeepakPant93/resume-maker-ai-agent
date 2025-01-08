import time
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _setup_driver() -> webdriver.Chrome:
    # Setup Chrome WebDriver (or other driver)
    options = webdriver.ChromeOptions()

    # Essential container arguments
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # JavaScript-specific configurations
    options.add_argument("--enable-javascript")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    # Performance optimizations
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-setuid-sandbox")

    # Memory management
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")

    # Handle Chrome Driver installation
    try:
        # For container environments, specify the Chrome version
        print("Setting up Chrome WebDriver")
        chrome_service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        # Fallback to direct path if ChromeDriverManager fails
        print(f"An error occurred: {e!s}")
        print("Falling back to direct path")

        driver = webdriver.Chrome(options=options)
    return driver


def _get_downloadable_audio_link(url: str) -> str:
    if not url:
        return ""

    # Extract the album ID and file ID from the URL
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split("/")
    album_id = path_parts[-2]
    file_id = path_parts[-1].split(".")[0]

    # Construct the downloadable audio link
    return f"https://aac.saavncdn.com/{album_id}/{file_id}.mp4"


def _extract_musician_name(url: str) -> str:
    return url.split("/")[-2].replace("-songs", "").replace("-", " ").title()


def scrape_dynamic_page(url: str, wait_time: int = 5) -> dict[str, Any]:
    """
    Scrape a webpage including content loaded by JavaScript

    Parameters:
    url (str): The URL to scrape
    wait_time (int): Maximum time to wait for dynamic content to load

    Returns:
    dict: Dictionary containing various elements from the page
    """
    driver = _setup_driver()

    try:
        # Load the page
        driver.get(url)

        # Wait for the button to be present
        button = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.c-btn.c-btn--primary[data-btn-icon="q"]'))
        )

        # Check visibility and enablement
        is_displayed = button.is_displayed()
        is_enabled = button.is_enabled()
        print(f"Button displayed: {is_displayed}, Button enabled: {is_enabled}")

        if is_displayed and is_enabled:
            # Click the button
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
        else:
            print("Button is not interactable!")

        # Wait a moment for any JavaScript updates
        time.sleep(5)

        # Get the updated HTML
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract elements
        details = {
            "album_title": soup.title.text if soup.title else "",
            "description": soup.find("meta", {"name": "description"})["content"]
            if soup.find("meta", {"name": "description"})
            else "",
            "album_description": soup.find("meta", {"property": "og:description"})["content"]
            if soup.find("meta", {"property": "og:description"})
            else "",
            "album_url": soup.find("meta", {"property": "music:album"})["content"]
            if soup.find("meta", {"property": "music:album"})
            else "",
            "album_image_url": soup.find("meta", {"property": "twitter:image"})["content"]
            if soup.find("meta", {"property": "twitter:image"})
            else "",
            "song_info": {
                "name": soup.title.text if soup.title else "",
                "title": soup.find("meta", {"property": "twitter:title"})["content"]
                if soup.find("meta", {"property": "twitter:title"})
                else "",
                "musician": [
                    _extract_musician_name(musician["content"])
                    for musician in soup.find_all("meta", {"property": "music:musician"})
                ],
                "release_date": datetime.strptime(
                    soup.find("meta", {"property": "music:release_date"})["content"],
                    "%Y-%m-%d",
                ).strftime("%B %d, %Y")
                if soup.find("meta", {"property": "music:release_date"})
                else "",
                "song_url": soup.find("meta", {"property": "twitter:url"})["content"]
                if soup.find("meta", {"property": "twitter:url"})
                else "",
                "description": soup.find("meta", {"property": "twitter:description"})["content"]
                if soup.find("meta", {"property": "twitter:description"})
                else "",
                "downloadable_url": _get_downloadable_audio_link(
                    soup.find("audio").find("source")["src"] if soup.find("audio").find("source") else ""
                ),
                "song_lyrics_url": "https://www.jiosaavn.com" + soup.find("a", title="Song Lyrics")["href"]
                if soup.find("a", title="Song Lyrics")
                else "",
            },
        }
    except TimeoutException:
        print(f"Timeout waiting for page to load: {url}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e!s}")
        return {}
    else:
        return details
    finally:
        driver.quit()


def scrape_pages(urls: list[str]) -> list[dict]:
    """
    Scrape multiple webpages and return a list of elements

    Parameters:
    urls (list of str): List of URLs to scrape
    wait_time (int): Maximum time to wait for dynamic content to load

    Returns:
    list of dict: List of dictionaries containing various elements from each page
    """
    results = []
    for url in urls:
        details = scrape_dynamic_page(url)
        if details:
            results.append(details)
    return results


def download_file(url: str) -> None:
    """
    Download a file from a URL and save it to a local file

    Parameters:
    url (str): URL of the file to be downloaded

    Returns:
    None
    """
    try:
        response = requests.get(url, stream=True, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            # Open a local file with the specified filename in binary write mode
            filename = _get_filename_name(url)
            filename = f"downloads/{filename}.mp4"

            with open(filename, "wb") as file:
                # Write the content of the response to the file in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File downloaded successfully as '{filename}'")
        else:
            print(f"Failed to download file. HTTP Status Code: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"Request to {url} timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Request to {url} failed: {e}")


def _get_filename_name(url: str) -> str:
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split("/")
    return path_parts[2]
