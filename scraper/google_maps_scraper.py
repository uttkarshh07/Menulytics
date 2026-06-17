import os
import time
import pandas as pd
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_DIR = os.path.join(BASE_DIR, "datasets", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "datasets", "processed")

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


QUERIES = [
    "restaurants in Indore",
    "cafes in Indore",
    "new cafes in Indore",
    "new restaurants in Indore",
    "best cafes in Indore",
    "trending cafes in Indore",
    "best restaurants in Indore",
    "fine dining restaurants in Indore",
    "date night restaurants in Indore",
    "viral cafes in Indore",
    "rooftop cafes in Indore",
    "coffee shops in Indore"
]


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver


def scroll_results(driver, scroll_count=10):
    time.sleep(5)

    try:
        scrollable_div = driver.find_element(
            By.XPATH,
            '//div[@role="feed"]'
        )

        for i in range(scroll_count):
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scrollable_div
            )
            time.sleep(2)

    except Exception as e:
        print("Scrolling failed:", e)


def scrape_google_maps_query(driver, query):
    print(f"\nScraping query: {query}")

    encoded_query = quote_plus(query)
    url = f"https://www.google.com/maps/search/{encoded_query}"

    driver.get(url)
    time.sleep(5)

    scroll_results(driver, scroll_count=12)

    places = []

    cards = driver.find_elements(By.XPATH, '//a[contains(@href, "/maps/place/")]')

    for card in cards:
        try:
            name = card.get_attribute("aria-label")
            place_url = card.get_attribute("href")

            if name and place_url:
                places.append({
                    "name": name.strip(),
                    "url": place_url,
                    "search_query": query
                })

        except Exception:
            continue

    df = pd.DataFrame(places)

    if not df.empty:
        safe_query = query.replace(" ", "_").replace("/", "_").lower()
        file_path = os.path.join(RAW_DATA_DIR, f"google_maps_{safe_query}.csv")
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"Saved {len(df)} records to {file_path}")
    else:
        print("No records found for this query.")

    return df


def clean_name(name):
    return str(name).lower().strip()


def main():
    driver = setup_driver()

    all_dataframes = []

    try:
        for query in QUERIES:
            df = scrape_google_maps_query(driver, query)

            if not df.empty:
                all_dataframes.append(df)

            time.sleep(3)

    finally:
        driver.quit()

    if not all_dataframes:
        print("No data scraped.")
        return

    master_df = pd.concat(all_dataframes, ignore_index=True)

    before_dedup = len(master_df)

    master_df["name_clean"] = master_df["name"].apply(clean_name)

    master_df = master_df.drop_duplicates(subset=["name_clean"], keep="first")

    master_df = master_df.drop(columns=["name_clean"])

    after_dedup = len(master_df)

    master_path = os.path.join(
        PROCESSED_DATA_DIR,
        "indore_restaurants_cafes_master.csv"
    )

    master_df.to_csv(master_path, index=False, encoding="utf-8-sig")

    print("\nMASTER DATASET CREATED")
    print(f"Total scraped records before deduplication: {before_dedup}")
    print(f"Unique restaurants/cafes after deduplication: {after_dedup}")
    print(f"Saved master dataset to: {master_path}")


if __name__ == "__main__":
    main()