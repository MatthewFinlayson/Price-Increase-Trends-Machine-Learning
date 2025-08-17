# API Documentation

## Price Increase Trends Machine Learning Project

This documentation provides comprehensive information about all public APIs, functions, and components in the Price Increase Trends scraping project.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Core Components](#core-components)
3. [Spider API](#spider-api)
4. [Data Structures](#data-structures)
5. [Middleware Components](#middleware-components)
6. [Pipeline Components](#pipeline-components)
7. [Configuration](#configuration)
8. [Usage Examples](#usage-examples)

## Project Overview

The Price Increase Trends project is a web scraping system built using Scrapy framework to collect historical shoe price data from Nike's website using the Wayback Machine. The project tracks price trends across multiple years (2012-2021) to enable machine learning analysis of price increase patterns.

### Architecture

```
scrapers/
├── scrapers/
    └── shoes/
        ├── scrapy.cfg          # Scrapy configuration
        └── shoes/
            ├── __init__.py
            ├── items.py        # Data structure definitions
            ├── middlewares.py  # Request/Response processing
            ├── pipelines.py    # Data processing pipeline
            ├── settings.py     # Project configuration
            └── spiders/
                ├── __init__.py
                └── shoespider.py  # Main spider implementation
```

## Core Components

### ShoeSpider Class

The main spider class responsible for scraping shoe data from archived Nike store pages.

**Location**: `scrapers/scrapers/shoes/shoes/spiders/shoespider.py`

## Spider API

### Class: `ShoeSpider`

**Inheritance**: `scrapy.Spider`

**Description**: Main spider class that scrapes shoe price and name data from archived Nike store pages using the Wayback Machine.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Spider identifier: `'shoes'` |
| `start_urls` | `list[str]` | List of URLs to begin crawling |

#### Methods

##### `parse(self, response)`

**Description**: Main parsing method that extracts shoe data from the response.

**Parameters**:
- `response` (`scrapy.http.Response`): The HTTP response object containing the webpage data

**Returns**: 
- `Generator[dict]`: Yields dictionaries containing shoe data

**Yields**:
```python
{
    'name': str,   # Shoe name (cleaned of unwanted characters)
    'price': str   # Shoe price (with '$' symbol removed)
}
```

**Example Usage**:
```python
# The parse method is automatically called by Scrapy
# It processes responses and yields data dictionaries
for product_data in spider.parse(response):
    print(f"Shoe: {product_data['name']}, Price: ${product_data['price']}")
```

**CSS Selectors Used**:

The spider uses different CSS selectors depending on the year/URL format:

- **2012-2019 Format**:
  - Container: `div.grid-item`
  - Name: `p.griditem-display-name::text` or `p.product-display-name::text`
  - Price: `span.local::text`

- **2020+ Format**:
  - Container: `div.product-card` or `div.product-card__info`
  - Name: `div.product-card__title::text`
  - Price: `div.css-b9fpep::text` or `div.product-price::text`

**Data Cleaning**:
- Removes `'iD\n'` and `'\t\t'` from product names
- Removes `'$'` symbol from prices

## Data Structures

### Class: `ShoesItem`

**Location**: `scrapers/scrapers/shoes/shoes/items.py`

**Inheritance**: `scrapy.Item`

**Description**: Defines the data structure for scraped items. Currently implemented as a pass-through class.

**Current Implementation**:
```python
class ShoesItem(scrapy.Item):
    pass
```

**Recommended Fields** (not currently implemented):
```python
class ShoesItem(scrapy.Item):
    name = scrapy.Field()        # Shoe name
    price = scrapy.Field()       # Shoe price
    url = scrapy.Field()         # Source URL
    scrape_date = scrapy.Field() # Date when scraped
    year = scrapy.Field()        # Year of the data
```

## Middleware Components

### Class: `ShoesSpiderMiddleware`

**Location**: `scrapers/scrapers/shoes/shoes/middlewares.py`

**Description**: Handles spider-level request and response processing.

#### Methods

##### `from_crawler(cls, crawler)`

**Class Method**: Creates middleware instance from crawler.

**Parameters**:
- `crawler` (`scrapy.crawler.Crawler`): The crawler instance

**Returns**: `ShoesSpiderMiddleware` instance

##### `process_spider_input(self, response, spider)`

**Description**: Processes responses before they reach the spider.

**Parameters**:
- `response` (`scrapy.http.Response`): HTTP response
- `spider` (`scrapy.Spider`): Spider instance

**Returns**: `None` or raises exception

##### `process_spider_output(self, response, result, spider)`

**Description**: Processes results returned from the spider.

**Parameters**:
- `response` (`scrapy.http.Response`): HTTP response
- `result` (`iterable`): Spider results
- `spider` (`scrapy.Spider`): Spider instance

**Yields**: Individual result items

##### `process_spider_exception(self, response, exception, spider)`

**Description**: Handles exceptions raised by spider processing.

**Parameters**:
- `response` (`scrapy.http.Response`): HTTP response
- `exception` (`Exception`): Raised exception
- `spider` (`scrapy.Spider`): Spider instance

##### `process_start_requests(self, start_requests, spider)`

**Description**: Processes initial requests from the spider.

**Parameters**:
- `start_requests` (`iterable`): Initial requests
- `spider` (`scrapy.Spider`): Spider instance

**Yields**: Request objects

##### `spider_opened(self, spider)`

**Description**: Called when spider is opened.

**Parameters**:
- `spider` (`scrapy.Spider`): Spider instance

### Class: `ShoesDownloaderMiddleware`

**Location**: `scrapers/scrapers/shoes/shoes/middlewares.py`

**Description**: Handles downloader-level request and response processing.

#### Methods

##### `from_crawler(cls, crawler)`

**Class Method**: Creates middleware instance from crawler.

##### `process_request(self, request, spider)`

**Description**: Processes requests before they are downloaded.

**Parameters**:
- `request` (`scrapy.http.Request`): HTTP request
- `spider` (`scrapy.Spider`): Spider instance

**Returns**: `None`, `Response`, `Request`, or raises `IgnoreRequest`

##### `process_response(self, request, response, spider)`

**Description**: Processes responses after download.

**Parameters**:
- `request` (`scrapy.http.Request`): HTTP request
- `response` (`scrapy.http.Response`): HTTP response
- `spider` (`scrapy.Spider`): Spider instance

**Returns**: `Response` or `Request` object

##### `process_exception(self, request, exception, spider)`

**Description**: Handles download exceptions.

**Parameters**:
- `request` (`scrapy.http.Request`): HTTP request
- `exception` (`Exception`): Download exception
- `spider` (`scrapy.Spider`): Spider instance

**Returns**: `None`, `Response`, or `Request`

## Pipeline Components

### Class: `ShoesPipeline`

**Location**: `scrapers/scrapers/shoes/shoes/pipelines.py`

**Description**: Processes scraped items before they are stored or exported.

#### Methods

##### `process_item(self, item, spider)`

**Description**: Processes individual scraped items.

**Parameters**:
- `item` (`dict` or `scrapy.Item`): Scraped item data
- `spider` (`scrapy.Spider`): Spider instance that scraped the item

**Returns**: `item` - The processed item

**Current Implementation**: Pass-through (no processing)

**Recommended Enhancements**:
```python
def process_item(self, item, spider):
    # Validate required fields
    if not item.get('name') or not item.get('price'):
        raise DropItem("Missing name or price")
    
    # Clean and validate price
    try:
        item['price'] = float(item['price'])
    except ValueError:
        raise DropItem("Invalid price format")
    
    # Add metadata
    item['scrape_timestamp'] = datetime.now().isoformat()
    item['spider_name'] = spider.name
    
    return item
```

## Configuration

### Settings Overview

**Location**: `scrapers/scrapers/shoes/shoes/settings.py`

The settings file contains all configuration options for the Scrapy project.

#### Core Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `BOT_NAME` | `'shoes'` | Project identifier |
| `SPIDER_MODULES` | `['shoes.spiders']` | Module containing spiders |
| `NEWSPIDER_MODULE` | `'shoes.spiders'` | Module for new spiders |
| `ROBOTSTXT_OBEY` | `True` | Respect robots.txt files |

#### Performance Settings (Commented)

```python
# Concurrent requests (default: 16)
CONCURRENT_REQUESTS = 32

# Download delay between requests
DOWNLOAD_DELAY = 3

# Per-domain concurrent requests
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# Per-IP concurrent requests  
CONCURRENT_REQUESTS_PER_IP = 16
```

#### Middleware Configuration (Commented)

```python
# Spider middlewares
SPIDER_MIDDLEWARES = {
    'shoes.middlewares.ShoesSpiderMiddleware': 543,
}

# Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'shoes.middlewares.ShoesDownloaderMiddleware': 543,
}

# Item pipelines
ITEM_PIPELINES = {
    'shoes.pipelines.ShoesPipeline': 300,
}
```

#### AutoThrottle Settings (Commented)

```python
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
```

## Usage Examples

### Basic Spider Execution

```bash
# Navigate to the project directory
cd /workspace/scrapers/scrapers/shoes

# Run the spider
scrapy crawl shoes

# Save output to JSON
scrapy crawl shoes -o output.json

# Save output to CSV
scrapy crawl shoes -o output.csv
```

### Programmatic Usage

```python
import scrapy
from scrapy.crawler import CrawlerProcess
from shoes.spiders.shoespider import ShoeSpider

# Create crawler process
process = CrawlerProcess({
    'USER_AGENT': 'price-trends-bot'
})

# Schedule spider
process.crawl(ShoeSpider)

# Start crawling
process.start()
```

### Custom Settings

```python
# Custom settings for the spider
custom_settings = {
    'DOWNLOAD_DELAY': 2,
    'CONCURRENT_REQUESTS': 1,
    'ITEM_PIPELINES': {
        'shoes.pipelines.ShoesPipeline': 300,
    }
}

process.crawl(ShoeSpider, custom_settings=custom_settings)
```

### Data Processing Example

```python
import json

# Load scraped data
with open('output.json', 'r') as f:
    shoes_data = json.load(f)

# Process data
for shoe in shoes_data:
    print(f"Product: {shoe['name']}")
    print(f"Price: ${shoe['price']}")
    print("-" * 30)

# Calculate average price
prices = [float(shoe['price']) for shoe in shoes_data if shoe['price']]
avg_price = sum(prices) / len(prices)
print(f"Average price: ${avg_price:.2f}")
```

## Historical Data Collection

The spider is designed to collect data from multiple years using Wayback Machine URLs:

### Supported Years and URL Patterns

- **2012**: `https://web.archive.org/web/20120704035744/http://store.nike.com/...`
- **2013**: `https://web.archive.org/web/20130629025923if_/http://store.nike.com/...`
- **2014**: `https://web.archive.org/web/20140223034104if_/http://store.nike.com/...`
- **2015**: `https://web.archive.org/web/20150408161543if_/http://store.nike.com/...`
- **2016**: `https://web.archive.org/web/20160806015038if_/http://store.nike.com/...`
- **2017**: `https://web.archive.org/web/20170925012126if_/https://store.nike.com/...`
- **2018**: `https://web.archive.org/web/20180927020453if_/https://store.nike.com/...`
- **2019**: `https://web.archive.org/web/20190331040349/https://store.nike.com/...`
- **2020**: `https://web.archive.org/web/20200331045809if_/https://www.nike.com/...`
- **2021**: `https://www.nike.com/ca/w/new-mens-shoes-3n82yznik1zy7ok`

### Modifying for Different Years

To scrape a specific year, uncomment the corresponding section in `shoespider.py` and comment out others:

```python
# Example: To scrape 2015 data
start_urls = ['https://web.archive.org/web/20150408161543if_/http://store.nike.com/us/en_us/pw/mens-shoes/7puZbrk']

def parse(self, response):
    for products in response.css('div.grid-item'):
        yield{
            'name': products.css('p.product-display-name::text').get().replace('iD\n','').replace('\t\t',''),
            'price': products.css('span.local::text').get().replace('$',''),
        }
```

## Error Handling and Debugging

### Common Issues

1. **Empty Results**: Check if the CSS selectors match the webpage structure
2. **Rate Limiting**: Increase `DOWNLOAD_DELAY` in settings
3. **Blocked Requests**: Modify `USER_AGENT` or add proxy support

### Debugging Tips

```python
# Add logging to spider
import logging

class ShoeSpider(scrapy.Spider):
    def parse(self, response):
        self.logger.info(f"Processing {response.url}")
        
        products = response.css('div.grid-item')
        self.logger.info(f"Found {len(products)} products")
        
        for product in products:
            # ... processing code
```

### Validation

```python
def parse(self, response):
    for products in response.css('div.grid-item'):
        name = products.css('p.griditem-display-name::text').get()
        price = products.css('span.local::text').get()
        
        # Validate data before yielding
        if name and price:
            yield {
                'name': name.replace('iD\n','').replace('\t\t',''),
                'price': price.replace('$',''),
            }
        else:
            self.logger.warning(f"Missing data: name={name}, price={price}")
```

## Extension Points

### Adding New Data Fields

1. Update the `ShoesItem` class:
```python
class ShoesItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()  # New field
    image_url = scrapy.Field()    # New field
```

2. Modify the spider to extract additional data:
```python
def parse(self, response):
    for products in response.css('div.grid-item'):
        yield {
            'name': products.css('p.griditem-display-name::text').get(),
            'price': products.css('span.local::text').get(),
            'description': products.css('p.description::text').get(),
            'image_url': products.css('img::attr(src)').get(),
        }
```

### Adding New Websites

Create a new spider class for different retailers:

```python
class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    start_urls = ['https://web.archive.org/web/.../adidas.com/...']
    
    def parse(self, response):
        # Implement Adidas-specific parsing logic
        pass
```

This API documentation provides comprehensive coverage of all public components, methods, and usage patterns in the Price Increase Trends scraping project.