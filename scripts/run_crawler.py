#!/usr/bin/env python3
"""
Script to run the math data crawler.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawledmathdata.crawler import MathDataCrawler

def main():
    # Start URLs
    start_urls = [
        'https://en.wikipedia.org/wiki/Mathematics',
        'https://math.stackexchange.com/questions',
        'https://www.khanacademy.org/math',
        'https://brilliant.org/courses/',
    ]

    # To reach 10GB, we need many pages. Adjust max_pages accordingly.
    # Each page ~10-50KB, so 10GB = ~200,000-1,000,000 pages. But that's impractical.
    # For demo, use smaller number.
    max_pages = 1000  # Adjust as needed

    crawler = MathDataCrawler(start_urls, max_pages=max_pages)
    crawler.crawl()
    crawler.save_data()
    print(f"Data collection complete. Size: {crawler.get_data_size():.2f} GB")

if __name__ == "__main__":
    main()