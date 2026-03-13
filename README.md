# CrawledMathData

A compliant web crawler for collecting mathematics-related data for AI training.

## Features

- Respects robots.txt directives
- Implements rate limiting with configurable delays
- Identifies with a proper User-Agent
- Filters for math-related content
- Extracts and cleans text from web pages
- Saves data in compressed JSON format
- Refines data into training-ready text files

## Legal Compliance

This crawler is designed for educational and research purposes only. It:

- Checks and obeys robots.txt files
- Uses polite crawling with delays to avoid overloading servers
- Does not redistribute copyrighted content
- Respects website terms of service
- Includes contact information in User-Agent

**Important:** Web scraping may violate terms of service or copyright laws. Use responsibly and only on sites that permit crawling. Consult legal advice for commercial use.

## Installation

```bash
pip install -e .
```

Or install dependencies manually:

```bash
pip install requests beautifulsoup4 lxml
```

## Usage

Run the crawler:

```bash
python scripts/run_crawler.py
```

This will crawl starting from predefined math-related URLs, collect up to 50 pages (configurable), and save to `math_data.json.gz`.

Refine the data:

```bash
python -c "from crawledmathdata.refiner import DataRefiner; refiner = DataRefiner('math_data.json.gz', 'math_training_data.txt'); refiner.refine_data()"
```

## Configuration

- `max_pages`: Maximum pages to crawl (default: 50)
- `delay`: Seconds between requests (default: 2.0)
- Start URLs are hardcoded in `run_crawler.py`

## Output

- `math_data.json.gz`: Compressed JSON with crawled page data
- `math_training_data.txt`: Refined text file for AI training

## Contributing

Ensure all changes maintain compliance with web scraping best practices.