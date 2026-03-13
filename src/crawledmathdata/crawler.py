"""
Web crawler for collecting mathematics-related data.
Crawls math websites, extracts text content, and refines it for AI training.
"""

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import gzip
from collections import deque

class MathDataCrawler:
    def __init__(self, start_urls, max_pages=10000, output_file="math_data.json.gz", delay=1.0):
        self.start_urls = start_urls
        self.max_pages = max_pages
        self.output_file = output_file
        self.visited = set()
        self.queue = deque(start_urls)
        self.data = []
        self.delay = delay  # seconds between requests
        self.last_request_time = 0
        self.robot_parsers = {}  # Cache robots.txt parsers per domain
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MathDataCrawler/1.0 (Educational AI Training; https://github.com/brilliantsam/crawledmathdata)'
        })

    def get_robot_parser(self, domain):
        """Get or create a robot parser for the domain."""
        if domain not in self.robot_parsers:
            rp = RobotFileParser()
            rp.set_url(f"https://{domain}/robots.txt")
            try:
                rp.read()
            except Exception as e:
                print(f"Could not read robots.txt for {domain}: {e}")
                # Assume allowed if can't read
                rp = None
            self.robot_parsers[domain] = rp
        return self.robot_parsers[domain]

    def can_fetch(self, url):
        """Check if we can fetch the URL according to robots.txt."""
        parsed = urlparse(url)
        domain = parsed.netloc
        rp = self.get_robot_parser(domain)
        if rp:
            return rp.can_fetch(self.session.headers['User-Agent'], url)
        return True  # If no robots.txt, assume allowed

    def is_math_related(self, url, content):
        """Check if the page is math-related."""
        math_keywords = [
            'mathematics', 'math', 'algebra', 'geometry', 'calculus', 'theorem',
            'proof', 'equation', 'formula', 'integral', 'derivative', 'matrix',
            'vector', 'probability', 'statistics', 'topology', 'analysis'
        ]
        url_lower = url.lower()
        content_lower = content.lower()
        return any(keyword in url_lower or keyword in content_lower for keyword in math_keywords)

    def extract_text(self, soup):
        """Extract clean text from HTML."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def crawl_page(self, url):
        """Crawl a single page."""
        if not self.can_fetch(url):
            print(f"Disallowed by robots.txt: {url}")
            return

        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else ""
            text = self.extract_text(soup)

            if self.is_math_related(url, text):
                page_data = {
                    'url': url,
                    'title': title,
                    'content': text,
                    'timestamp': time.time()
                }
                self.data.append(page_data)
                print(f"Crawled: {url} ({len(text)} chars)")

                # Find links to crawl next
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(url, link['href'])
                    parsed = urlparse(next_url)
                    if parsed.scheme in ['http', 'https'] and parsed.netloc == urlparse(url).netloc:
                        if next_url not in self.visited and len(self.queue) < self.max_pages:
                            self.queue.append(next_url)

        except requests.exceptions.RequestException as e:
            print(f"Request error for {url}: {e}")
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def crawl(self):
        """Main crawling loop."""
        while self.queue and len(self.visited) < self.max_pages:
            url = self.queue.popleft()
            if url in self.visited:
                continue
            self.visited.add(url)
            self.crawl_page(url)

    def save_data(self):
        """Save collected data to file."""
        with gzip.open(self.output_file, 'wt', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.data)} pages to {self.output_file}")

    def get_data_size(self):
        """Get approximate size of data in GB."""
        content_size = sum(len(page['content']) for page in self.data)
        return content_size / (1024**3)  # GB

    def is_math_related(self, url, content):
        """Check if the page is math-related."""
        math_keywords = [
            'mathematics', 'math', 'algebra', 'geometry', 'calculus', 'theorem',
            'proof', 'equation', 'formula', 'integral', 'derivative', 'matrix',
            'vector', 'probability', 'statistics', 'topology', 'analysis'
        ]
        url_lower = url.lower()
        content_lower = content.lower()
        return any(keyword in url_lower or keyword in content_lower for keyword in math_keywords)

    def extract_text(self, soup):
        """Extract clean text from HTML."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def crawl_page(self, url):
        """Crawl a single page."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else ""
            text = self.extract_text(soup)

            if self.is_math_related(url, text):
                page_data = {
                    'url': url,
                    'title': title,
                    'content': text,
                    'timestamp': time.time()
                }
                self.data.append(page_data)
                print(f"Crawled: {url} ({len(text)} chars)")

                # Find links to crawl next
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(url, link['href'])
                    parsed = urlparse(next_url)
                    if parsed.scheme in ['http', 'https'] and parsed.netloc == urlparse(url).netloc:
                        if next_url not in self.visited and len(self.queue) < self.max_pages:
                            self.queue.append(next_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def crawl(self):
        """Main crawling loop."""
        while self.queue and len(self.visited) < self.max_pages:
            url = self.queue.popleft()
            if url in self.visited:
                continue
            self.visited.add(url)
            self.crawl_page(url)
            time.sleep(1)  # Be polite

    def save_data(self):
        """Save collected data to file."""
        with gzip.open(self.output_file, 'wt', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.data)} pages to {self.output_file}")

    def get_data_size(self):
        """Get approximate size of data in GB."""
        content_size = sum(len(page['content']) for page in self.data)
        return content_size / (1024**3)  # GB

if __name__ == "__main__":
    # Start URLs for math-related sites
    start_urls = [
        'https://en.wikipedia.org/wiki/Mathematics',
        'https://math.stackexchange.com/questions',
        'https://www.khanacademy.org/math',
        'https://brilliant.org/courses/',
    ]

    crawler = MathDataCrawler(start_urls, max_pages=5000)  # Adjust for more data
    crawler.crawl()
    crawler.save_data()
    print(f"Collected approximately {crawler.get_data_size():.2f} GB of data")