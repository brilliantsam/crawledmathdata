"""
Data refiner for processing crawled math data into training format.
"""

import json
import gzip
import re
from pathlib import Path

class DataRefiner:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def clean_text(self, text):
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove non-printable characters
        text = re.sub(r'[^\x20-\x7E\n]', '', text)
        return text.strip()

    def extract_math_content(self, page_data):
        """Extract relevant math content from page data."""
        title = self.clean_text(page_data.get('title', ''))
        content = self.clean_text(page_data.get('content', ''))

        # For training, we can concatenate title and content
        full_text = f"{title}\n{content}"

        # Split into sentences or keep as is
        return full_text

    def refine_data(self):
        """Refine the crawled data."""
        refined_data = []

        with gzip.open(self.input_file, 'rt', encoding='utf-8') as f:
            data = json.load(f)

        for page in data:
            refined_text = self.extract_math_content(page)
            if len(refined_text) > 100:  # Filter short content
                refined_data.append(refined_text)

        # To reach 10GB, we might need to duplicate or expand
        # For demo, just save as is
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for text in refined_data:
                f.write(text + '\n\n')

        print(f"Refined {len(refined_data)} pages into {self.output_file}")

if __name__ == "__main__":
    refiner = DataRefiner('math_data.json.gz', 'math_training_data.txt')
    refiner.refine_data()