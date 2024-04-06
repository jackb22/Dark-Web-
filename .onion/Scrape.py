from Connection import get_user_agent
from bs4 import BeautifulSoup
import pycurl
from io import BytesIO
import logging
from pymongo import MongoClient
from urllib.parse import urljoin

# Define the Crawler class
class Crawler():
    """
    Class to crawl a website and scrape its pages. 
    Utilzing Depth First Search Algorithm

    Attributes
    ----------
    initial_url : str
        the starting URL for the crawl
    proxy_port : int, optional
        the port number for the proxy server (default is None)
    max_depth : int, optional
        the maximum depth to crawl (default is 2)
    client : MongoClient
        the MongoDB client
    db : Database
        the MongoDB database
    crawled_urls : Collection
        the MongoDB collection for storing crawled URLs

    Methods
    -------
    urlopen(url)
        Opens the URL and returns the HTML content.
    scrape_page(url, current_depth=0)
        Scrapes the page at the URL and recursively crawls all links.
    """

    def __init__(self, initial_url, proxy_port=None, max_depth=2, db_uri='mongodb://mongo:27017/', db_name='crawler'):
        """Initializes the Crawler with the given parameters and connects to MongoDB."""
        self.initial_url = initial_url
        self.proxy_port = proxy_port
        self.max_depth = max_depth
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.crawled_urls = self.db.crawled_urls

    def urlopen(self, url):
        """Opens the URL and returns the HTML content."""
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.USERAGENT, get_user_agent())  # Set the User-Agent header
        c.setopt(c.WRITEDATA, buffer)
        try:
            c.perform()  # Perform the request
            return buffer.getvalue()  # Return the HTML content
        except pycurl.error as e:
            logging.error(f"Failed to open {url}: {e}")
            return None
        finally:
            c.close()  # Always close the Curl object

    def scrape_page(self, url, current_depth=0):
        """Scrapes the page at the URL and recursively crawls all links."""
        if current_depth > self.max_depth:
            return
        html = self.urlopen(url)
        if html is None:
            return
        try:
            parsed = BeautifulSoup(html, 'html.parser')
            for tag in parsed.find_all("a", href=True):
                href = tag["href"]
                new_url = urljoin(url, href)
                if self.crawled_urls.find_one({'url': new_url}) is None:
                    # If the URL hasn't been crawled before, insert it into the database and crawl it
                    self.crawled_urls.insert_one({'url': new_url})
                    self.scrape_page(new_url, current_depth + 1)
        except Exception as e:
            logging.error(f"Failed to scrape {url}: {e}")

    def __del__(self):
        """Destructor to close the MongoDB connection when the Crawler is destroyed."""
        self.client.close()