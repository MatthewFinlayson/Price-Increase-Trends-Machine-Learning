# Installation and Usage Guide

## Price Increase Trends Machine Learning Project

This guide provides step-by-step instructions for installing, configuring, and using the Price Increase Trends scraping system.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [Basic Usage](#basic-usage)
6. [Advanced Usage](#advanced-usage)
7. [Data Analysis](#data-analysis)
8. [Troubleshooting](#troubleshooting)
9. [Performance Optimization](#performance-optimization)

## Prerequisites

### System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 2GB RAM (4GB recommended)
- **Storage**: At least 1GB free space for data storage

### Required Knowledge

- Basic understanding of Python
- Familiarity with command-line interface
- Basic knowledge of web scraping concepts (helpful but not required)

## Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd Price-Increase-Trends-Machine-Learning
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Create a `requirements.txt` file in the project root:

```txt
scrapy>=2.5.0
itemadapter>=0.4.0
requests>=2.25.0
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Navigate to the scrapy project directory
cd scrapers/scrapers/shoes

# Test scrapy installation
scrapy version
```

Expected output:
```
Scrapy 2.x.x - no active project
```

## Project Structure

```
Price-Increase-Trends-Machine-Learning/
├── README.md                           # Project overview
├── API_DOCUMENTATION.md                # Comprehensive API docs
├── INSTALLATION_AND_USAGE.md          # This file
├── DEVELOPER_GUIDE.md                  # Developer documentation
├── requirements.txt                    # Python dependencies
├── scrapers/                          # Main scraping project
│   └── scrapers/
│       └── shoes/
│           ├── scrapy.cfg             # Scrapy configuration
│           └── shoes/                 # Python package
│               ├── __init__.py
│               ├── items.py           # Data structures
│               ├── middlewares.py     # Request/Response processing
│               ├── pipelines.py       # Data processing pipeline
│               ├── settings.py        # Configuration
│               └── spiders/           # Spider implementations
│                   ├── __init__.py
│                   └── shoespider.py  # Main spider
├── alldata/                           # Collected data
│   ├── AllData.csv                    # Combined dataset
│   └── Individual Data/               # Year-specific data
│       ├── AllNike.csv
│       ├── WomenAll.csv
│       └── allAdidas.csv
└── analysis/                          # Data analysis (to be created)
    ├── notebooks/                     # Jupyter notebooks
    ├── scripts/                       # Analysis scripts
    └── results/                       # Analysis results
```

## Configuration

### Basic Configuration

The main configuration file is located at:
`scrapers/scrapers/shoes/shoes/settings.py`

#### Essential Settings

```python
# Basic project settings
BOT_NAME = 'shoes'
SPIDER_MODULES = ['shoes.spiders']
NEWSPIDER_MODULE = 'shoes.spiders'

# Politeness settings
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1  # 1 second delay between requests

# Output settings
FEEDS = {
    'output.json': {'format': 'json'},
    'output.csv': {'format': 'csv'},
}
```

#### Performance Settings

For better performance, you can adjust these settings:

```python
# Concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# AutoThrottle (automatic delay adjustment)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
```

#### Enable Pipelines and Middlewares

Uncomment these lines in `settings.py`:

```python
# Enable pipelines
ITEM_PIPELINES = {
    'shoes.pipelines.ShoesPipeline': 300,
}

# Enable middlewares
SPIDER_MIDDLEWARES = {
    'shoes.middlewares.ShoesSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
    'shoes.middlewares.ShoesDownloaderMiddleware': 543,
}
```

### Environment Variables

Create a `.env` file in the project root for sensitive configurations:

```bash
# .env file
USER_AGENT=Price-Trends-Bot/1.0
PROXY_URL=http://your-proxy:8080
LOG_LEVEL=INFO
```

Load environment variables in `settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv('USER_AGENT', 'shoes (+http://www.yourdomain.com)')
```

## Basic Usage

### Running the Spider

#### Simple Execution

```bash
# Navigate to the scrapy project
cd scrapers/scrapers/shoes

# Run the spider
scrapy crawl shoes
```

#### Save Output to File

```bash
# Save as JSON
scrapy crawl shoes -o nike_shoes.json

# Save as CSV
scrapy crawl shoes -o nike_shoes.csv

# Save as JSON Lines
scrapy crawl shoes -o nike_shoes.jl
```

#### Custom Output Location

```bash
# Save to specific directory
scrapy crawl shoes -o /path/to/output/nike_data.json

# Save with timestamp
scrapy crawl shoes -o "nike_$(date +%Y%m%d_%H%M%S).json"
```

### Viewing Results

#### JSON Output
```bash
# Pretty print JSON
python -m json.tool nike_shoes.json
```

#### CSV Output
```bash
# View CSV (first 10 rows)
head -10 nike_shoes.csv

# View with column headers
csvlook nike_shoes.csv | head -20
```

### Basic Data Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_json('nike_shoes.json')

# Basic statistics
print(f"Total shoes scraped: {len(df)}")
print(f"Average price: ${df['price'].astype(float).mean():.2f}")
print(f"Price range: ${df['price'].astype(float).min():.2f} - ${df['price'].astype(float).max():.2f}")

# Plot price distribution
df['price'].astype(float).hist(bins=20)
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.title('Nike Shoe Price Distribution')
plt.show()
```

## Advanced Usage

### Custom Spider Configuration

#### Modifying Start URLs

Edit `shoespider.py` to scrape different years:

```python
# For 2020 data
start_urls = ['https://web.archive.org/web/20200331045809if_/https://www.nike.com/w/mens-shoes-nik1zy7ok']

# For multiple years
start_urls = [
    'https://web.archive.org/web/20200331045809if_/https://www.nike.com/w/mens-shoes-nik1zy7ok',
    'https://web.archive.org/web/20190331040349/https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3',
    'https://web.archive.org/web/20180927020453if_/https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3'
]
```

#### Custom Data Fields

Modify the spider to extract additional information:

```python
def parse(self, response):
    for products in response.css('div.grid-item'):
        yield {
            'name': products.css('p.griditem-display-name::text').get(),
            'price': products.css('span.local::text').get(),
            'url': response.url,  # Add source URL
            'scrape_date': datetime.now().isoformat(),  # Add timestamp
            'year': self.extract_year_from_url(response.url)  # Add year
        }

def extract_year_from_url(self, url):
    # Extract year from Wayback Machine URL
    import re
    match = re.search(r'/web/(\d{4})', url)
    return match.group(1) if match else 'unknown'
```

### Batch Processing

#### Process Multiple Years

Create a script to run multiple scraping sessions:

```python
# batch_scrape.py
import subprocess
import time
from datetime import datetime

years = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

for year in years:
    print(f"Scraping {year} data...")
    
    # Modify spider for specific year (you'd need to implement this)
    cmd = f"scrapy crawl shoes -o nike_{year}.json"
    
    result = subprocess.run(cmd, shell=True, cwd='scrapers/scrapers/shoes')
    
    if result.returncode == 0:
        print(f"✓ {year} data scraped successfully")
    else:
        print(f"✗ Failed to scrape {year} data")
    
    # Delay between requests
    time.sleep(10)

print("Batch scraping completed!")
```

#### Combine Multiple Datasets

```python
# combine_data.py
import pandas as pd
import glob
import os

# Find all JSON files
json_files = glob.glob('nike_*.json')

# Combine all datasets
all_data = []
for file in json_files:
    year = file.replace('nike_', '').replace('.json', '')
    df = pd.read_json(file)
    df['year'] = year
    all_data.append(df)

# Combine into single dataset
combined_df = pd.concat(all_data, ignore_index=True)

# Save combined dataset
combined_df.to_csv('all_nike_data.csv', index=False)
combined_df.to_json('all_nike_data.json', orient='records', indent=2)

print(f"Combined {len(combined_df)} records from {len(json_files)} files")
```

### Custom Pipelines

Create custom data processing pipelines:

```python
# In pipelines.py
import pandas as pd
from datetime import datetime
from itemadapter import ItemAdapter

class DataValidationPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Validate price
        if not adapter.get('price'):
            raise DropItem("Missing price")
        
        try:
            price = float(adapter['price'])
            if price <= 0:
                raise DropItem("Invalid price")
            adapter['price'] = price
        except ValueError:
            raise DropItem("Invalid price format")
        
        # Validate name
        if not adapter.get('name') or len(adapter['name'].strip()) == 0:
            raise DropItem("Missing or empty name")
        
        adapter['name'] = adapter['name'].strip()
        return item

class DataEnrichmentPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Add metadata
        adapter['scrape_timestamp'] = datetime.now().isoformat()
        adapter['spider_name'] = spider.name
        
        # Categorize by price range
        price = adapter['price']
        if price < 50:
            adapter['price_category'] = 'budget'
        elif price < 100:
            adapter['price_category'] = 'mid-range'
        elif price < 200:
            adapter['price_category'] = 'premium'
        else:
            adapter['price_category'] = 'luxury'
        
        return item

class CSVExportPipeline:
    def __init__(self):
        self.items = []
    
    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        return item
    
    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        filename = f"{spider.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        spider.logger.info(f"Saved {len(df)} items to {filename}")
```

Enable the pipelines in `settings.py`:

```python
ITEM_PIPELINES = {
    'shoes.pipelines.DataValidationPipeline': 200,
    'shoes.pipelines.DataEnrichmentPipeline': 300,
    'shoes.pipelines.CSVExportPipeline': 400,
}
```

### Scheduling and Automation

#### Using Cron (Linux/macOS)

```bash
# Edit crontab
crontab -e

# Add daily scraping at 2 AM
0 2 * * * cd /path/to/project/scrapers/scrapers/shoes && /path/to/venv/bin/scrapy crawl shoes -o daily_$(date +\%Y\%m\%d).json
```

#### Using Task Scheduler (Windows)

Create a batch file `run_scraper.bat`:

```batch
@echo off
cd /d "C:\path\to\project\scrapers\scrapers\shoes"
call "C:\path\to\venv\Scripts\activate.bat"
scrapy crawl shoes -o nike_%date:~-4,4%%date:~-10,2%%date:~-7,2%.json
```

#### Python Scheduler

```python
# scheduler.py
import schedule
import time
import subprocess
import os
from datetime import datetime

def run_scraper():
    """Run the spider and save with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    cmd = f"scrapy crawl shoes -o nike_{timestamp}.json"
    
    os.chdir('scrapers/scrapers/shoes')
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"✓ Scraping completed: nike_{timestamp}.json")
    else:
        print(f"✗ Scraping failed")

# Schedule daily scraping
schedule.every().day.at("02:00").do(run_scraper)

# Schedule weekly scraping
schedule.every().monday.at("10:00").do(run_scraper)

print("Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

## Data Analysis

### Loading and Exploring Data

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
df = pd.read_json('nike_shoes.json')

# Basic info
print("Dataset Overview:")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print("\nData types:")
print(df.dtypes)
print("\nFirst few rows:")
print(df.head())
```

### Price Analysis

```python
# Convert price to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Remove invalid prices
df = df.dropna(subset=['price'])
df = df[df['price'] > 0]

# Basic statistics
print("Price Statistics:")
print(df['price'].describe())

# Price distribution
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
df['price'].hist(bins=30, alpha=0.7)
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.title('Price Distribution')

plt.subplot(1, 2, 2)
df.boxplot(column='price')
plt.ylabel('Price ($)')
plt.title('Price Box Plot')

plt.tight_layout()
plt.show()
```

### Trend Analysis (Multiple Years)

```python
# If you have year data
if 'year' in df.columns:
    # Price trends over years
    yearly_stats = df.groupby('year')['price'].agg(['mean', 'median', 'count']).round(2)
    print("Yearly Price Statistics:")
    print(yearly_stats)
    
    # Plot trends
    plt.figure(figsize=(10, 6))
    yearly_stats['mean'].plot(kind='line', marker='o', label='Average Price')
    yearly_stats['median'].plot(kind='line', marker='s', label='Median Price')
    plt.xlabel('Year')
    plt.ylabel('Price ($)')
    plt.title('Nike Shoe Price Trends Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
```

### Product Name Analysis

```python
# Most common words in product names
from collections import Counter
import re

# Extract words from product names
all_words = []
for name in df['name'].dropna():
    words = re.findall(r'\b[A-Za-z]+\b', name.lower())
    all_words.extend(words)

# Most common words
word_counts = Counter(all_words)
top_words = word_counts.most_common(20)

print("Most Common Words in Product Names:")
for word, count in top_words:
    print(f"{word}: {count}")

# Visualize
words, counts = zip(*top_words)
plt.figure(figsize=(12, 6))
plt.bar(words, counts)
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Most Common Words in Nike Shoe Names')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Export Analysis Results

```python
# Create analysis report
analysis_results = {
    'total_products': len(df),
    'avg_price': df['price'].mean(),
    'median_price': df['price'].median(),
    'price_std': df['price'].std(),
    'min_price': df['price'].min(),
    'max_price': df['price'].max(),
    'analysis_date': datetime.now().isoformat()
}

# Save to JSON
import json
with open('analysis_results.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)

# Save detailed statistics
df.describe().to_csv('price_statistics.csv')

print("Analysis results saved!")
```

## Troubleshooting

### Common Issues

#### 1. Spider Not Finding Products

**Problem**: Spider returns empty results

**Solutions**:
```python
# Add debugging to spider
def parse(self, response):
    # Debug: Check if page loaded correctly
    self.logger.info(f"Response status: {response.status}")
    self.logger.info(f"Response URL: {response.url}")
    
    # Debug: Check CSS selectors
    products = response.css('div.grid-item')
    self.logger.info(f"Found {len(products)} product containers")
    
    if not products:
        # Try alternative selectors
        products = response.css('div.product-card')
        self.logger.info(f"Found {len(products)} products with alternative selector")
```

#### 2. Rate Limiting / Blocked Requests

**Problem**: Getting 429 or 403 errors

**Solutions**:
```python
# In settings.py
DOWNLOAD_DELAY = 3  # Increase delay
RANDOMIZE_DOWNLOAD_DELAY = 0.5  # Add randomization

# Use AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10

# Change User Agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Add proxy support
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}
```

#### 3. Memory Issues

**Problem**: Spider consumes too much memory

**Solutions**:
```python
# In settings.py
# Limit concurrent requests
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Disable caching
HTTPCACHE_ENABLED = False

# Use streaming for large datasets
FEEDS = {
    'output.jsonl': {
        'format': 'jsonlines',
        'store_empty': False,
    }
}
```

#### 4. Data Quality Issues

**Problem**: Scraped data contains errors

**Solutions**:
```python
# Add data validation in pipeline
class DataCleaningPipeline:
    def process_item(self, item, spider):
        # Clean price
        if item.get('price'):
            price = re.sub(r'[^\d.]', '', item['price'])
            try:
                item['price'] = float(price)
            except ValueError:
                item['price'] = None
        
        # Clean name
        if item.get('name'):
            item['name'] = ' '.join(item['name'].split())
            item['name'] = item['name'].replace('\n', '').replace('\t', '')
        
        return item
```

### Debugging Tools

#### Enable Detailed Logging

```python
# In settings.py
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'scrapy.log'

# Custom log format
LOG_FORMAT = '%(levelname)s: %(message)s'
```

#### Use Scrapy Shell

```bash
# Interactive debugging
scrapy shell "https://web.archive.org/web/20200331045809if_/https://www.nike.com/w/mens-shoes-nik1zy7ok"

# Test selectors
response.css('div.product-card').getall()
response.css('div.product-card__title::text').getall()
```

#### Monitor Spider Performance

```python
# Add stats collection
class StatsCollectionPipeline:
    def __init__(self):
        self.stats = {
            'items_processed': 0,
            'items_dropped': 0,
            'start_time': None,
            'end_time': None
        }
    
    def open_spider(self, spider):
        self.stats['start_time'] = datetime.now()
    
    def close_spider(self, spider):
        self.stats['end_time'] = datetime.now()
        duration = self.stats['end_time'] - self.stats['start_time']
        
        spider.logger.info(f"Spider Statistics:")
        spider.logger.info(f"Items processed: {self.stats['items_processed']}")
        spider.logger.info(f"Items dropped: {self.stats['items_dropped']}")
        spider.logger.info(f"Duration: {duration}")
        spider.logger.info(f"Items/second: {self.stats['items_processed']/duration.total_seconds():.2f}")
```

## Performance Optimization

### Scrapy Settings Optimization

```python
# Optimal settings for performance
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = 0.5

# Enable compression
COMPRESSION_ENABLED = True

# Optimize DNS
DNSCACHE_ENABLED = True
DNSCACHE_SIZE = 10000
DNS_TIMEOUT = 60

# Connection pooling
REACTOR_THREADPOOL_MAXSIZE = 20
```

### Memory Optimization

```python
# Streaming data export
FEEDS = {
    'output.jsonl': {
        'format': 'jsonlines',
        'store_empty': False,
    }
}

# Disable item caching
ITEM_PIPELINES = {
    'shoes.pipelines.StreamingPipeline': 300,
}

class StreamingPipeline:
    def __init__(self):
        self.file = open('streaming_output.jsonl', 'w')
    
    def process_item(self, item, spider):
        import json
        self.file.write(json.dumps(dict(item)) + '\n')
        self.file.flush()  # Write immediately
        return item
    
    def close_spider(self, spider):
        self.file.close()
```

### Database Storage

For large-scale data collection, consider using a database:

```python
# Database pipeline
import sqlite3
import json

class DatabasePipeline:
    def __init__(self):
        self.connection = sqlite3.connect('nike_shoes.db')
        self.cursor = self.connection.cursor()
        
        # Create table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                url TEXT,
                scrape_date TEXT,
                year INTEGER
            )
        ''')
        self.connection.commit()
    
    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO shoes (name, price, url, scrape_date, year)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            item.get('name'),
            item.get('price'),
            item.get('url'),
            item.get('scrape_date'),
            item.get('year')
        ))
        self.connection.commit()
        return item
    
    def close_spider(self, spider):
        self.connection.close()
```

This comprehensive installation and usage guide provides everything needed to set up, configure, and use the Price Increase Trends scraping system effectively.