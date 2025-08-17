# Price Increase Trends Machine Learning

A comprehensive web scraping system for collecting and analyzing historical shoe price data to identify price increase trends using machine learning techniques.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd Price-Increase-Trends-Machine-Learning

# Install dependencies
pip install -r requirements.txt

# Navigate to the scraper directory
cd scrapers/scrapers/shoes

# Run the spider
scrapy crawl shoes -o nike_shoes.json
```

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Data Analysis](#data-analysis)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project uses web scraping techniques to collect historical shoe price data from Nike's website via the Wayback Machine, covering data from 2012 to 2021. The collected data enables machine learning analysis to identify price increase trends and patterns in the footwear market.

### Key Features

- **Historical Data Collection**: Scrapes price data across multiple years (2012-2021)
- **Robust Web Scraping**: Built with Scrapy framework for reliable data extraction
- **Data Processing Pipeline**: Comprehensive data validation and cleaning
- **Multiple Export Formats**: Support for JSON, CSV, and database export
- **Extensible Architecture**: Easy to add new brands and data sources
- **Comprehensive Documentation**: Full API documentation and usage guides

## 🏗️ Project Structure

```
Price-Increase-Trends-Machine-Learning/
├── 📁 scrapers/                    # Main scraping project
│   └── scrapers/shoes/
│       ├── scrapy.cfg              # Scrapy configuration
│       └── shoes/                  # Python package
│           ├── items.py            # Data structures
│           ├── middlewares.py      # Request/Response processing
│           ├── pipelines.py        # Data processing pipeline
│           ├── settings.py         # Configuration
│           └── spiders/
│               └── shoespider.py   # Main spider implementation
├── 📁 alldata/                     # Collected datasets
│   ├── AllData.csv                 # Combined dataset
│   └── Individual Data/            # Year-specific data
├── 📄 API_DOCUMENTATION.md         # Comprehensive API docs
├── 📄 INSTALLATION_AND_USAGE.md    # Installation & usage guide
├── 📄 DEVELOPER_GUIDE.md           # Developer documentation
├── 📄 requirements.txt             # Python dependencies
└── 📄 README.md                    # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager
- 2GB RAM minimum (4GB recommended)
- 1GB free disk space

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Price-Increase-Trends-Machine-Learning
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   cd scrapers/scrapers/shoes
   scrapy version
   ```

## 🚀 Usage

### Basic Usage

```bash
# Navigate to the scraper directory
cd scrapers/scrapers/shoes

# Run the spider and save to JSON
scrapy crawl shoes -o nike_shoes.json

# Run the spider and save to CSV
scrapy crawl shoes -o nike_shoes.csv
```

### Advanced Usage

```python
# Programmatic usage
from scrapy.crawler import CrawlerProcess
from shoes.spiders.shoespider import ShoeSpider

process = CrawlerProcess({
    'FEEDS': {
        'output.json': {'format': 'json'}
    }
})

process.crawl(ShoeSpider)
process.start()
```

### Data Analysis Example

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load scraped data
df = pd.read_json('nike_shoes.json')

# Basic analysis
print(f"Total shoes: {len(df)}")
print(f"Average price: ${df['price'].astype(float).mean():.2f}")

# Plot price distribution
df['price'].astype(float).hist(bins=20)
plt.title('Nike Shoe Price Distribution')
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.show()
```

## 📚 Documentation

This project includes comprehensive documentation:

- **[API Documentation](API_DOCUMENTATION.md)**: Complete API reference for all classes and methods
- **[Installation & Usage Guide](INSTALLATION_AND_USAGE.md)**: Detailed setup and usage instructions
- **[Developer Guide](DEVELOPER_GUIDE.md)**: Information for developers wanting to extend the project

### Quick Reference

#### Spider Configuration

The main spider supports different years and URL patterns:

```python
# 2012-2019: Uses grid-item layout
start_urls = ['https://web.archive.org/web/20150408161543if_/http://store.nike.com/...']

# 2020+: Uses product-card layout  
start_urls = ['https://web.archive.org/web/20200331045809if_/https://www.nike.com/...']
```

#### Data Fields

Each scraped item contains:
- `name`: Product name (cleaned)
- `price`: Product price (numeric, $ removed)
- `url`: Source URL
- `year`: Data year (if available)

## 📊 Data Analysis

The project includes historical price data that enables various analyses:

### Price Trend Analysis

```python
# Analyze price trends over time
yearly_avg = df.groupby('year')['price'].mean()
yearly_avg.plot(kind='line', title='Average Nike Shoe Prices Over Time')
```

### Product Category Analysis

```python
# Analyze product lines
df['product_line'] = df['name'].str.extract(r'(Air|Zoom|Free)')
df.groupby('product_line')['price'].mean().plot(kind='bar')
```

### Market Insights

The collected data reveals:
- Price evolution patterns from 2012-2021
- Product line pricing strategies
- Seasonal price variations
- Market positioning trends

## 🤝 Contributing

We welcome contributions! Please see our [Developer Guide](DEVELOPER_GUIDE.md) for detailed information.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes with tests
4. Run tests: `pytest tests/`
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ --cov=shoes
```

## 📈 Future Enhancements

- [ ] Add support for additional brands (Adidas, Puma, etc.)
- [ ] Implement machine learning models for price prediction
- [ ] Add real-time price monitoring
- [ ] Create web dashboard for data visualization
- [ ] Add automated data quality monitoring
- [ ] Implement advanced analytics and reporting

## 🛡️ Legal and Ethical Considerations

This project is designed for educational and research purposes. Please ensure you:

- Respect website terms of service
- Follow robots.txt guidelines
- Use appropriate delays between requests
- Consider the impact on target servers
- Comply with relevant data protection laws

## 📞 Support

If you encounter issues or have questions:

1. Check the [Installation & Usage Guide](INSTALLATION_AND_USAGE.md)
2. Review the [API Documentation](API_DOCUMENTATION.md)
3. Look through existing issues
4. Create a new issue with detailed information

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Scrapy](https://scrapy.org/) framework
- Data visualization with [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/)
- Analysis powered by [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/)

---

**Note**: This project is for educational purposes. Always respect website terms of service and use responsible scraping practices.
