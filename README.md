# Automobile.tn Car Scraper

This script scrapes car data from [automobile.tn](https://www.automobile.tn/fr/neuf/recherche/) website, specifically looking for cars with HT price tags.

## Features

- Scrapes car listings from automobile.tn
- Automatically handles pagination
- Retry mechanism for failed page loads (3 attempts per page)
- Extracts complete price information including "à partir de" text
- Saves results in structured JSON format

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
3. Extract car information:
   - Car name
   - Complete normal price (including "à partir de" text)
   - HT price
   - Direct link to car details
4. Retry failed page loads up to 3 times
5. Save the results to `cars_with_ht_price.json`


## Error Handling

- The script includes automatic retry mechanism for failed page loads
- Each page load attempt has a 60-second timeout
- If a page fails to load after 3 attempts, the script will skip to the next page
- Detailed console output shows scraping progress and any errors encountered 


## Output

The script outputs a JSON file with the following structure:
```json
[
  {
    "name": "Bako B-Van",
    "normal_price": "à partir de 22 586 DT",
    "ht_price": "8 900 $ HT",
    "link": "https://www.automobile.tn/fr/neuf/bako/evan"
  },
  ...
]
```
