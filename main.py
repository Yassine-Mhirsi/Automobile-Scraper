from playwright.sync_api import sync_playwright, TimeoutError
import time
import json

def scrape_page(page, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} for URL: {url}")
            page.goto(url)
            page.wait_for_load_state("networkidle", timeout=60000)
            return True
        except TimeoutError:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                print("Waiting 5 seconds before retrying...")
                time.sleep(5)
            else:
                print(f"Failed after {max_retries} attempts")
                return False
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print("Waiting 5 seconds before retrying...")
                time.sleep(5)
            else:
                print(f"Failed after {max_retries} attempts")
                return False
    return False

def scrape_cars():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        cars_with_ht = []
        current_page = 1
        max_pages = 13
        
        while current_page <= max_pages:
            url = f"https://www.automobile.tn/fr/neuf/recherche/s=sort%21price?sort=price&page={current_page}"
            print(f"\nScraping page {current_page}: {url}")
            
            # Try to load the page with retries
            if not scrape_page(page, url):
                print(f"Skipping page {current_page} after all retries failed")
                current_page += 1
                continue
            
            # Find all car items on the page
            car_items = page.query_selector_all('.versions-item')
            print(f"Found {len(car_items)} cars on this page")
            
            if len(car_items) == 0:
                print("No cars found on this page, stopping pagination")
                break
            
            found_ht_on_page = False
            for car_item in car_items:
                try:
                    # Check if the car has HT price
                    ht_price_element = car_item.query_selector('.price-ht')
                    
                    if ht_price_element:
                        found_ht_on_page = True
                        # Extract car information
                        car_name_element = car_item.query_selector('h2')
                        car_name = car_name_element.inner_text().strip() if car_name_element else "Unknown Car"
                        
                        # Get normal price - using the correct structure from HTML
                        price_div = car_item.query_selector('.price')
                        if price_div:
                            # Get all text nodes including "à partir de" and the price
                            price_text = price_div.inner_text().strip()
                            normal_price = price_text if price_text else "N/A"
                        else:
                            normal_price = "N/A"
                        
                        # Get HT price
                        ht_price = ht_price_element.inner_text().strip()
                        
                        # Get link to details
                        link_element = car_item.query_selector('a')
                        link = link_element.get_attribute('href') if link_element else ""
                        full_link = f"https://www.automobile.tn{link}" if link else "N/A"
                        
                        # Add to our list
                        cars_with_ht.append({
                            "name": car_name,
                            "normal_price": normal_price,
                            "ht_price": ht_price,
                            "link": full_link
                        })
                        
                        print(f"Found car with HT price: {car_name} - Normal: {normal_price} - HT: {ht_price}")
                except Exception as e:
                    print(f"Error processing car item: {e}")
                    continue
            
            if not found_ht_on_page:
                print("No cars with HT prices found on this page")
            
            # Check if we've reached the last page or max_pages
            try:
                # Try to find the next page button
                next_page = page.query_selector('.pagination li.active + li')
                if not next_page or current_page >= max_pages:
                    print(f"No more pages or reached max limit of {max_pages} pages")
                    break
                    
                # Go to the next page
                current_page += 1
                time.sleep(3)  # Delay between pages
            except Exception as e:
                print(f"Error during pagination: {e}")
                break
        
        browser.close()
        return cars_with_ht

if __name__ == "__main__":
    cars = scrape_cars()
    
    # Save the results to a JSON file
    with open("cars_with_ht_price.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=4)
    
    print(f"\nScraped {len(cars)} cars with HT price tag")
    print("Results saved to cars_with_ht_price.json")
