# Automobile.tn Car Scraper

This script scrapes car data from [automobile.tn](https://www.automobile.tn/fr/neuf/recherche/) website, specifically looking for cars with HT price tags.

## Requirements

- Python 3.7+
- Playwright

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```
   playwright install
   ```

## Usage

Run the script:
```
python main.py
```

The script will:
1. Visit automobile.tn car listings pages (up to page 13)
2. Find cars with HT price tags
3. Extract car name, normal price, and HT price
4. Save the results to `cars_with_ht_price.json`

## Output

The script outputs a JSON file with the following structure:
```json
[
  {
        "name": "BAKO B-VAN",
        "normal_price": "à partir de 22 586 DT",
        "ht_price": "8 900 $ HT",
        "link": "https://www.automobile.tn/fr/neuf/bako/evan"
  },
  ...
]
``` 
