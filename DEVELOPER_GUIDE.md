# Developer Guide

## Price Increase Trends Machine Learning Project

This guide provides comprehensive information for developers who want to extend, modify, or contribute to the Price Increase Trends scraping project.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Architecture Overview](#architecture-overview)
3. [Code Structure](#code-structure)
4. [Extending the Spider](#extending-the-spider)
5. [Custom Middlewares](#custom-middlewares)
6. [Custom Pipelines](#custom-pipelines)
7. [Adding New Spiders](#adding-new-spiders)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Best Practices](#best-practices)
11. [Contributing](#contributing)

## Development Setup

### Prerequisites for Development

- Python 3.7+
- Git
- Code editor (VS Code, PyCharm, etc.)
- Understanding of Scrapy framework
- Basic knowledge of HTML/CSS selectors
- Familiarity with web development concepts

### Development Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd Price-Increase-Trends-Machine-Learning

# Create and activate virtual environment
python -m venv dev-env
source dev-env/bin/activate  # On Windows: dev-env\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install project in development mode
pip install -e .
```

### Development Dependencies

Create `requirements-dev.txt`:

```txt
# Production dependencies
scrapy>=2.5.0
itemadapter>=0.4.0
requests>=2.25.0
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0

# Development dependencies
pytest>=6.2.0
pytest-cov>=2.12.0
black>=21.0.0
flake8>=3.9.0
mypy>=0.812
pre-commit>=2.13.0
jupyter>=1.0.0
ipython>=7.0.0

# Testing utilities
responses>=0.13.0
scrapy-test>=0.1.0
mock>=4.0.0
```

### IDE Configuration

#### VS Code Configuration

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./dev-env/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

#### Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 21.9b0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 3.9.2
    hooks:
      - id: flake8
        args: [--max-line-length=88]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.812
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

## Architecture Overview

### System Components

```
Price-Increase-Trends-ML/
├── scrapers/scrapers/shoes/shoes/
│   ├── spiders/
│   │   └── shoespider.py      # Main spider logic
│   ├── items.py               # Data structures
│   ├── pipelines.py           # Data processing
│   ├── middlewares.py         # Request/response processing
│   └── settings.py            # Configuration
├── analysis/
│   ├── data_processor.py      # Data analysis utilities
│   └── ml_models.py           # Machine learning models
├── tests/
│   ├── test_spiders.py        # Spider tests
│   ├── test_pipelines.py      # Pipeline tests
│   └── fixtures/              # Test data
└── docs/                      # Documentation
```

### Data Flow

```
1. Spider Request → 2. Middleware Processing → 3. Response Processing
                                                         ↓
6. Data Export ← 5. Pipeline Processing ← 4. Item Extraction
```

### Key Design Patterns

1. **Factory Pattern**: Used in spider creation and middleware initialization
2. **Pipeline Pattern**: For sequential data processing
3. **Observer Pattern**: For signal handling and event processing
4. **Strategy Pattern**: For different parsing strategies per year/site

## Code Structure

### Spider Structure

```python
# shoespider.py structure
class ShoeSpider(scrapy.Spider):
    name = 'shoes'
    
    # Configuration
    custom_settings = {}
    
    # URL generation
    def start_requests(self):
        pass
    
    # Main parsing logic
    def parse(self, response):
        pass
    
    # Helper methods
    def extract_year_from_url(self, url):
        pass
    
    def clean_product_name(self, name):
        pass
```

### Item Structure

```python
# items.py - Recommended structure
class ShoesItem(scrapy.Item):
    # Required fields
    name = scrapy.Field()
    price = scrapy.Field()
    
    # Metadata fields
    url = scrapy.Field()
    scrape_date = scrapy.Field()
    year = scrapy.Field()
    
    # Optional fields
    description = scrapy.Field()
    image_url = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    
    # Validation
    def __setitem__(self, key, value):
        if key == 'price' and value:
            # Ensure price is numeric
            try:
                value = float(str(value).replace('$', '').replace(',', ''))
            except ValueError:
                raise ValueError(f"Invalid price format: {value}")
        super().__setitem__(key, value)
```

### Pipeline Structure

```python
# pipelines.py - Recommended structure
from abc import ABC, abstractmethod
from itemadapter import ItemAdapter

class BasePipeline(ABC):
    """Base class for all pipelines"""
    
    @abstractmethod
    def process_item(self, item, spider):
        pass
    
    def open_spider(self, spider):
        """Called when spider is opened"""
        pass
    
    def close_spider(self, spider):
        """Called when spider is closed"""
        pass

class ValidationPipeline(BasePipeline):
    """Validates item data"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Implement validation logic
        self._validate_required_fields(adapter)
        self._validate_data_types(adapter)
        
        return item

class EnrichmentPipeline(BasePipeline):
    """Enriches items with additional data"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Add computed fields
        self._add_price_category(adapter)
        self._add_metadata(adapter, spider)
        
        return item
```

## Extending the Spider

### Adding New Data Fields

1. **Update Items Definition**:

```python
# items.py
class ShoesItem(scrapy.Item):
    # Existing fields
    name = scrapy.Field()
    price = scrapy.Field()
    
    # New fields
    brand = scrapy.Field()
    color = scrapy.Field()
    size_range = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
```

2. **Modify Spider Parsing Logic**:

```python
# shoespider.py
def parse(self, response):
    for product in response.css('div.grid-item'):
        item = ShoesItem()
        
        # Existing extraction
        item['name'] = product.css('p.griditem-display-name::text').get()
        item['price'] = product.css('span.local::text').get()
        
        # New field extraction
        item['brand'] = self.extract_brand(product)
        item['color'] = self.extract_color(product)
        item['size_range'] = self.extract_size_range(product)
        item['availability'] = self.extract_availability(product)
        item['rating'] = self.extract_rating(product)
        item['review_count'] = self.extract_review_count(product)
        
        yield item

def extract_brand(self, product):
    """Extract brand from product element"""
    brand = product.css('.brand::text').get()
    return brand.strip() if brand else 'Nike'  # Default brand

def extract_color(self, product):
    """Extract color information"""
    color_element = product.css('.color-info::text').get()
    if color_element:
        # Parse color from text like "Available in Black, White"
        colors = re.findall(r'Available in (.+)', color_element)
        return colors[0] if colors else None
    return None

def extract_size_range(self, product):
    """Extract available size range"""
    sizes = product.css('.size-option::text').getall()
    if sizes:
        size_numbers = [float(s) for s in sizes if s.replace('.', '').isdigit()]
        if size_numbers:
            return f"{min(size_numbers)}-{max(size_numbers)}"
    return None
```

### Adding Multi-Page Support

```python
class ShoeSpider(scrapy.Spider):
    name = 'shoes'
    
    def parse(self, response):
        # Extract items from current page
        for product in response.css('div.grid-item'):
            yield self.parse_product(product, response)
        
        # Follow pagination
        next_page = response.css('.pagination .next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_product(self, product, response):
        """Extract data from individual product"""
        item = ShoesItem()
        
        # Basic extraction
        item['name'] = product.css('p.griditem-display-name::text').get()
        item['price'] = product.css('span.local::text').get()
        
        # Check if detailed page exists
        product_url = product.css('a::attr(href)').get()
        if product_url:
            # Follow to detailed page
            return response.follow(
                product_url,
                self.parse_product_detail,
                meta={'item': item}
            )
        else:
            return item
    
    def parse_product_detail(self, response):
        """Parse detailed product page"""
        item = response.meta['item']
        
        # Extract additional details
        item['description'] = response.css('.product-description::text').get()
        item['image_url'] = response.css('.product-image img::attr(src)').get()
        item['rating'] = response.css('.rating::attr(data-rating)').get()
        
        return item
```

### Handling Different Site Layouts

```python
class ShoeSpider(scrapy.Spider):
    name = 'shoes'
    
    def parse(self, response):
        # Determine site layout based on URL or page structure
        layout_version = self.detect_layout_version(response)
        
        if layout_version == 'v1':
            yield from self.parse_v1_layout(response)
        elif layout_version == 'v2':
            yield from self.parse_v2_layout(response)
        else:
            self.logger.warning(f"Unknown layout for {response.url}")
    
    def detect_layout_version(self, response):
        """Detect which layout version the page uses"""
        if response.css('div.grid-item'):
            return 'v1'
        elif response.css('div.product-card'):
            return 'v2'
        return 'unknown'
    
    def parse_v1_layout(self, response):
        """Parse old layout (2012-2019)"""
        for product in response.css('div.grid-item'):
            yield {
                'name': product.css('p.griditem-display-name::text').get(),
                'price': product.css('span.local::text').get(),
                'layout_version': 'v1'
            }
    
    def parse_v2_layout(self, response):
        """Parse new layout (2020+)"""
        for product in response.css('div.product-card'):
            yield {
                'name': product.css('div.product-card__title::text').get(),
                'price': product.css('div.product-price::text').get(),
                'layout_version': 'v2'
            }
```

## Custom Middlewares

### Request Processing Middleware

```python
# middlewares.py
import random
import time
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class CustomRetryMiddleware(RetryMiddleware):
    """Custom retry logic with exponential backoff"""
    
    def process_response(self, request, response, spider):
        if response.status in [429, 503]:  # Rate limited
            reason = f'HTTP {response.status}'
            retry_times = request.meta.get('retry_times', 0) + 1
            
            if retry_times <= self.max_retry_times:
                # Exponential backoff
                delay = (2 ** retry_times) + random.uniform(0, 1)
                spider.logger.info(f"Retrying {request.url} in {delay:.2f}s")
                
                time.sleep(delay)
                retryreq = request.copy()
                retryreq.meta['retry_times'] = retry_times
                return retryreq
        
        return super().process_response(request, response, spider)

class UserAgentRotationMiddleware:
    """Rotate user agents to avoid detection"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
    
    def process_request(self, request, spider):
        ua = random.choice(self.user_agents)
        request.headers['User-Agent'] = ua
        return None

class ProxyMiddleware:
    """Handle proxy rotation"""
    
    def __init__(self, proxy_list):
        self.proxies = proxy_list
        self.current_proxy = 0
    
    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.getlist('PROXY_LIST')
        return cls(proxy_list)
    
    def process_request(self, request, spider):
        if self.proxies:
            proxy = self.proxies[self.current_proxy]
            request.meta['proxy'] = proxy
            self.current_proxy = (self.current_proxy + 1) % len(self.proxies)
        return None
```

### Response Processing Middleware

```python
class ResponseValidationMiddleware:
    """Validate response content"""
    
    def process_response(self, request, response, spider):
        # Check if page loaded correctly
        if b'Access Denied' in response.body:
            spider.logger.warning(f"Access denied for {response.url}")
            # Return None to retry or handle differently
            return None
        
        # Check for minimum content length
        if len(response.body) < 1000:
            spider.logger.warning(f"Suspicious short response from {response.url}")
        
        return response

class CacheMiddleware:
    """Simple caching middleware"""
    
    def __init__(self):
        self.cache = {}
    
    def process_request(self, request, spider):
        cache_key = self.get_cache_key(request)
        if cache_key in self.cache:
            spider.logger.info(f"Cache hit for {request.url}")
            return self.cache[cache_key]
        return None
    
    def process_response(self, request, response, spider):
        cache_key = self.get_cache_key(request)
        self.cache[cache_key] = response
        return response
    
    def get_cache_key(self, request):
        return request.url
```

## Custom Pipelines

### Data Validation Pipeline

```python
from scrapy.exceptions import DropItem
import re

class DataValidationPipeline:
    """Comprehensive data validation"""
    
    def __init__(self):
        self.price_pattern = re.compile(r'^\d+(\.\d{2})?$')
        self.required_fields = ['name', 'price']
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Check required fields
        for field in self.required_fields:
            if not adapter.get(field):
                raise DropItem(f"Missing required field: {field}")
        
        # Validate price format
        price = str(adapter['price']).replace('$', '').replace(',', '')
        if not self.price_pattern.match(price):
            raise DropItem(f"Invalid price format: {adapter['price']}")
        
        # Convert price to float
        adapter['price'] = float(price)
        
        # Validate name
        name = adapter['name'].strip()
        if len(name) < 3:
            raise DropItem(f"Product name too short: {name}")
        
        adapter['name'] = name
        
        return item

class DuplicateFilterPipeline:
    """Filter duplicate items"""
    
    def __init__(self):
        self.seen_items = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Create unique identifier
        identifier = (adapter['name'], adapter['price'])
        
        if identifier in self.seen_items:
            spider.logger.info(f"Duplicate item filtered: {adapter['name']}")
            raise DropItem("Duplicate item")
        
        self.seen_items.add(identifier)
        return item

class DataEnrichmentPipeline:
    """Enrich items with additional data"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Add price category
        price = adapter['price']
        if price < 50:
            adapter['price_category'] = 'budget'
        elif price < 100:
            adapter['price_category'] = 'mid-range'
        elif price < 200:
            adapter['price_category'] = 'premium'
        else:
            adapter['price_category'] = 'luxury'
        
        # Add brand extraction from name
        name = adapter['name'].lower()
        if 'air' in name:
            adapter['product_line'] = 'Air'
        elif 'zoom' in name:
            adapter['product_line'] = 'Zoom'
        elif 'free' in name:
            adapter['product_line'] = 'Free'
        else:
            adapter['product_line'] = 'Other'
        
        # Add metadata
        adapter['scrape_timestamp'] = datetime.now().isoformat()
        adapter['spider_name'] = spider.name
        
        return item
```

### Export Pipelines

```python
import json
import csv
import sqlite3
from datetime import datetime

class JSONExportPipeline:
    """Export to JSON with custom formatting"""
    
    def __init__(self, filename='output.json'):
        self.filename = filename
        self.items = []
    
    @classmethod
    def from_crawler(cls, crawler):
        filename = crawler.settings.get('JSON_EXPORT_FILE', 'output.json')
        return cls(filename)
    
    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        return item
    
    def close_spider(self, spider):
        with open(self.filename, 'w') as f:
            json.dump({
                'metadata': {
                    'spider': spider.name,
                    'timestamp': datetime.now().isoformat(),
                    'total_items': len(self.items)
                },
                'items': self.items
            }, f, indent=2)
        spider.logger.info(f"Exported {len(self.items)} items to {self.filename}")

class DatabaseExportPipeline:
    """Export to SQLite database"""
    
    def __init__(self, db_path='shoes.db'):
        self.db_path = db_path
        self.connection = None
    
    def open_spider(self, spider):
        self.connection = sqlite3.connect(self.db_path)
        self.create_tables()
    
    def close_spider(self, spider):
        if self.connection:
            self.connection.close()
    
    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                price_category TEXT,
                product_line TEXT,
                url TEXT,
                year INTEGER,
                scrape_timestamp TEXT,
                spider_name TEXT
            )
        ''')
        self.connection.commit()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO shoes (name, price, price_category, product_line, 
                             url, year, scrape_timestamp, spider_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            adapter.get('name'),
            adapter.get('price'),
            adapter.get('price_category'),
            adapter.get('product_line'),
            adapter.get('url'),
            adapter.get('year'),
            adapter.get('scrape_timestamp'),
            adapter.get('spider_name')
        ))
        self.connection.commit()
        
        return item
```

## Adding New Spiders

### Creating a New Spider

```python
# spiders/adidas_spider.py
import scrapy
from shoes.items import ShoesItem

class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    allowed_domains = ['adidas.com', 'web.archive.org']
    
    start_urls = [
        'https://web.archive.org/web/20200331045809if_/https://www.adidas.com/us/men-shoes'
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
    }
    
    def parse(self, response):
        """Parse Adidas product listings"""
        products = response.css('.grid-item')
        
        for product in products:
            item = ShoesItem()
            
            item['name'] = product.css('.itemTitle::text').get()
            item['price'] = product.css('.price::text').get()
            item['brand'] = 'Adidas'
            item['url'] = response.url
            
            # Clean data
            if item['name']:
                item['name'] = item['name'].strip()
            
            if item['price']:
                item['price'] = item['price'].replace('$', '').replace(',', '')
            
            yield item
        
        # Follow pagination
        next_page = response.css('.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

class PumaSpider(scrapy.Spider):
    name = 'puma'
    allowed_domains = ['puma.com', 'web.archive.org']
    
    def start_requests(self):
        """Generate requests for multiple years"""
        base_urls = [
            'https://web.archive.org/web/{}/https://us.puma.com/en/us/men/shoes'
        ]
        
        years = ['20200331', '20190331', '20180331']
        
        for year in years:
            for base_url in base_urls:
                url = base_url.format(year + '045809if_')
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={'year': year[:4]}
                )
    
    def parse(self, response):
        """Parse Puma product listings"""
        year = response.meta.get('year')
        
        # Different selectors based on year
        if int(year) >= 2020:
            products = response.css('.product-tile')
            name_selector = '.product-tile-title::text'
            price_selector = '.product-tile-price::text'
        else:
            products = response.css('.product-item')
            name_selector = '.product-name::text'
            price_selector = '.price::text'
        
        for product in products:
            item = ShoesItem()
            
            item['name'] = product.css(name_selector).get()
            item['price'] = product.css(price_selector).get()
            item['brand'] = 'Puma'
            item['year'] = int(year)
            item['url'] = response.url
            
            yield item
```

### Multi-Brand Spider

```python
class MultiBrandSpider(scrapy.Spider):
    name = 'multibrands'
    
    brand_configs = {
        'nike': {
            'urls': ['https://web.archive.org/web/.../nike.com/...'],
            'selectors': {
                'container': 'div.grid-item',
                'name': 'p.griditem-display-name::text',
                'price': 'span.local::text'
            }
        },
        'adidas': {
            'urls': ['https://web.archive.org/web/.../adidas.com/...'],
            'selectors': {
                'container': '.grid-item',
                'name': '.itemTitle::text',
                'price': '.price::text'
            }
        }
    }
    
    def start_requests(self):
        for brand, config in self.brand_configs.items():
            for url in config['urls']:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={'brand': brand, 'selectors': config['selectors']}
                )
    
    def parse(self, response):
        brand = response.meta['brand']
        selectors = response.meta['selectors']
        
        products = response.css(selectors['container'])
        
        for product in products:
            item = ShoesItem()
            
            item['name'] = product.css(selectors['name']).get()
            item['price'] = product.css(selectors['price']).get()
            item['brand'] = brand.title()
            item['url'] = response.url
            
            yield item
```

## Testing

### Unit Tests

```python
# tests/test_spiders.py
import unittest
from scrapy.http import HtmlResponse, Request
from shoes.spiders.shoespider import ShoeSpider

class TestShoeSpider(unittest.TestCase):
    
    def setUp(self):
        self.spider = ShoeSpider()
    
    def test_parse(self):
        """Test basic parsing functionality"""
        # Create mock HTML response
        html = '''
        <html>
            <div class="grid-item">
                <p class="griditem-display-name">Air Max 90</p>
                <span class="local">$120</span>
            </div>
            <div class="grid-item">
                <p class="griditem-display-name">Air Force 1</p>
                <span class="local">$90</span>
            </div>
        </html>
        '''
        
        response = HtmlResponse(
            url='https://example.com',
            body=html,
            encoding='utf-8'
        )
        
        # Test parsing
        results = list(self.spider.parse(response))
        
        # Assertions
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['name'], 'Air Max 90')
        self.assertEqual(results[0]['price'], '120')
        self.assertEqual(results[1]['name'], 'Air Force 1')
        self.assertEqual(results[1]['price'], '90')
    
    def test_extract_year_from_url(self):
        """Test year extraction from Wayback Machine URLs"""
        url = 'https://web.archive.org/web/20200331045809if_/https://www.nike.com/...'
        year = self.spider.extract_year_from_url(url)
        self.assertEqual(year, '2020')
    
    def test_clean_product_name(self):
        """Test product name cleaning"""
        dirty_name = 'iD\n\t\tAir Max 90\t\t'
        clean_name = self.spider.clean_product_name(dirty_name)
        self.assertEqual(clean_name, 'Air Max 90')

# tests/test_pipelines.py
from scrapy.exceptions import DropItem
from shoes.pipelines import DataValidationPipeline
from shoes.items import ShoesItem

class TestDataValidationPipeline(unittest.TestCase):
    
    def setUp(self):
        self.pipeline = DataValidationPipeline()
        self.spider = None  # Mock spider
    
    def test_valid_item(self):
        """Test processing of valid item"""
        item = ShoesItem()
        item['name'] = 'Air Max 90'
        item['price'] = '120.00'
        
        result = self.pipeline.process_item(item, self.spider)
        
        self.assertEqual(result['name'], 'Air Max 90')
        self.assertEqual(result['price'], 120.0)
    
    def test_missing_required_field(self):
        """Test handling of missing required fields"""
        item = ShoesItem()
        item['name'] = 'Air Max 90'
        # Missing price
        
        with self.assertRaises(DropItem):
            self.pipeline.process_item(item, self.spider)
    
    def test_invalid_price_format(self):
        """Test handling of invalid price format"""
        item = ShoesItem()
        item['name'] = 'Air Max 90'
        item['price'] = 'invalid_price'
        
        with self.assertRaises(DropItem):
            self.pipeline.process_item(item, self.spider)
```

### Integration Tests

```python
# tests/test_integration.py
import tempfile
import json
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor
from shoes.spiders.shoespider import ShoeSpider

class TestIntegration(unittest.TestCase):
    
    @defer.inlineCallbacks
    def test_full_spider_run(self):
        """Test complete spider execution"""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
            output_file = f.name
        
        runner = CrawlerRunner({
            'FEEDS': {
                output_file: {'format': 'json'}
            }
        })
        
        yield runner.crawl(ShoeSpider)
        
        # Verify output
        with open(output_file, 'r') as f:
            results = json.load(f)
        
        self.assertGreater(len(results), 0)
        
        # Verify data structure
        for item in results:
            self.assertIn('name', item)
            self.assertIn('price', item)
```

### Test Fixtures

```python
# tests/fixtures/responses.py
NIKE_2020_HTML = '''
<html>
    <div class="product-card">
        <div class="product-card__title">Air Max 90</div>
        <div class="product-price">$120</div>
    </div>
    <div class="product-card">
        <div class="product-card__title">Air Force 1</div>
        <div class="product-price">$90</div>
    </div>
</html>
'''

NIKE_2015_HTML = '''
<html>
    <div class="grid-item">
        <p class="product-display-name">Air Max 90</p>
        <span class="local">$120</span>
    </div>
    <div class="grid-item">
        <p class="product-display-name">Air Force 1</p>
        <span class="local">$90</span>
    </div>
</html>
'''
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=shoes tests/

# Run specific test file
pytest tests/test_spiders.py

# Run with verbose output
pytest -v tests/

# Generate HTML coverage report
pytest --cov=shoes --cov-report=html tests/
```

## Deployment

### Production Configuration

```python
# settings/production.py
from .base import *

# Production-specific settings
DEBUG = False

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = '/var/log/scrapy/shoes.log'

# Performance settings
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 8
DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = 0.5

# AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = '/tmp/scrapy_cache'

# Database settings
DATABASE_URL = os.getenv('DATABASE_URL')

# Monitoring
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install application
RUN pip install -e .

# Create user for running the application
RUN useradd --create-home --shell /bin/bash scraper
USER scraper

# Default command
CMD ["scrapy", "crawl", "shoes"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  scraper:
    build: .
    environment:
      - DATABASE_URL=sqlite:///data/shoes.db
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - database
  
  database:
    image: postgres:13
    environment:
      - POSTGRES_DB=shoes
      - POSTGRES_USER=scraper
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  scheduler:
    build: .
    command: python scheduler.py
    environment:
      - DATABASE_URL=postgresql://scraper:password@database:5432/shoes
    depends_on:
      - database

volumes:
  postgres_data:
```

### Monitoring and Logging

```python
# monitoring.py
import logging
from scrapy.statscollectors import StatsCollector
from scrapy.utils.serialize import ScrapyJSONEncoder
import json

class CustomStatsCollector(StatsCollector):
    """Custom stats collector with external monitoring"""
    
    def _persist_stats(self, stats, spider):
        # Send stats to monitoring system
        stats_data = {
            'spider': spider.name,
            'stats': dict(stats),
            'timestamp': datetime.now().isoformat()
        }
        
        # Log to file
        with open('/var/log/scrapy/stats.json', 'a') as f:
            f.write(json.dumps(stats_data, cls=ScrapyJSONEncoder) + '\n')
        
        # Send to monitoring service (e.g., Prometheus, DataDog)
        # self.send_to_monitoring_service(stats_data)

class SlackNotificationPipeline:
    """Send notifications to Slack"""
    
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    @classmethod
    def from_crawler(cls, crawler):
        webhook_url = crawler.settings.get('SLACK_WEBHOOK_URL')
        return cls(webhook_url)
    
    def close_spider(self, spider):
        stats = spider.crawler.stats.get_stats()
        
        message = f"""
        Spider {spider.name} completed:
        - Items scraped: {stats.get('item_scraped_count', 0)}
        - Items dropped: {stats.get('item_dropped_count', 0)}
        - Requests: {stats.get('downloader/request_count', 0)}
        - Duration: {stats.get('elapsed_time_seconds', 0):.2f}s
        """
        
        # Send to Slack
        # requests.post(self.webhook_url, json={'text': message})
```

## Best Practices

### Code Organization

1. **Separation of Concerns**: Keep spiders, pipelines, and middlewares focused on single responsibilities
2. **Configuration Management**: Use environment-specific settings files
3. **Error Handling**: Implement comprehensive error handling and logging
4. **Documentation**: Document all public methods and complex logic

### Performance Optimization

1. **Use Appropriate Delays**: Balance speed with server politeness
2. **Enable Compression**: Reduce bandwidth usage
3. **Optimize Selectors**: Use efficient CSS/XPath selectors
4. **Memory Management**: Process items in streams for large datasets

### Security Considerations

1. **Respect robots.txt**: Always check and respect site policies
2. **Rate Limiting**: Implement appropriate delays and concurrency limits
3. **User Agent Rotation**: Avoid detection with varied user agents
4. **Proxy Usage**: Use proxies for sensitive or large-scale scraping

### Data Quality

1. **Validation**: Implement comprehensive data validation
2. **Deduplication**: Remove duplicate items
3. **Cleaning**: Clean and normalize data consistently
4. **Monitoring**: Track data quality metrics

## Contributing

### Development Workflow

1. **Fork the Repository**: Create your own fork
2. **Create Feature Branch**: `git checkout -b feature/new-feature`
3. **Make Changes**: Implement your changes with tests
4. **Run Tests**: Ensure all tests pass
5. **Submit Pull Request**: Create PR with description

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write comprehensive tests
- Document all public APIs
- Use meaningful commit messages

### Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure CI/CD pipeline passes
4. Request review from maintainers
5. Address feedback promptly

This developer guide provides comprehensive information for extending and contributing to the Price Increase Trends scraping project.