import time
import re
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


INPUT_FILE = "datasets/processed/indore_restaurants_cafes_master_gold.csv"
OUTPUT_FILE = "datasets/processed/indore_restaurants_cafes_details_gold.csv"


df = pd.read_csv(INPUT_FILE)


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver


driver = setup_driver()


def safe_text(xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text.strip()
    except:
        return ""


def safe_attr(xpath, attr):
    try:
        return driver.find_element(By.XPATH, xpath).get_attribute(attr)
    except:
        return ""


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)
    text = text.replace("", "")
    text = text.replace("", "")
    text = text.replace("", "")
    text = text.replace("", "")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_rating_and_reviews():
    rating = ""
    reviews = ""

    try:
        rating_text = safe_text('//div[contains(@class, "F7nice")]')
        rating_text = rating_text.replace("\n", " ")

        rating_match = re.search(r"(\d+\.\d+)", rating_text)
        review_match = re.search(r"\(([\d,]+)\)", rating_text)

        if rating_match:
            rating = rating_match.group(1)

        if review_match:
            reviews = review_match.group(1).replace(",", "")

    except:
        pass

    return rating, reviews


def extract_category():
    category = safe_text('//button[contains(@class, "DkEaL")]')

    if not category:
        category = safe_text('//button[contains(@jsaction, "pane.rating.category")]')

    return clean_text(category)


def extract_address():
    address = safe_text('//button[contains(@data-item-id, "address")]')

    if not address:
        address = safe_text('//button[contains(@aria-label, "Address")]')

    return clean_text(address)


def extract_phone():
    phone = safe_text('//button[contains(@data-item-id, "phone")]')

    if not phone:
        phone = safe_text('//button[contains(@aria-label, "Phone")]')

    phone = clean_text(phone)

    phone_match = re.search(r"(\+?\d[\d\s\-]{7,})", phone)

    if phone_match:
        return phone_match.group(1).strip()

    return phone


def extract_website():
    website = safe_attr('//a[contains(@data-item-id, "authority")]', "href")

    if not website:
        website = safe_attr('//a[contains(@aria-label, "Website")]', "href")

    return website.strip() if website else ""


# Resume logic
restaurants = []

if os.path.exists(OUTPUT_FILE):
    existing_df = pd.read_csv(OUTPUT_FILE)
    restaurants = existing_df.to_dict("records")

    scraped_names = set(
        existing_df["restaurant_name"].astype(str).str.lower().str.strip()
    )

    df = df[
        ~df["name"].astype(str).str.lower().str.strip().isin(scraped_names)
    ]

    print("Resuming scraper...")
    print("Already scraped:", len(existing_df))
    print("Remaining:", len(df))


for index, row in df.iterrows():
    name = row["name"]
    url = row["url"]

    print(f"Scraping: {name}")

    try:
        driver.get(url)
        time.sleep(6)

        rating, total_reviews = extract_rating_and_reviews()
        category = extract_category()
        address = extract_address()
        phone = extract_phone()
        website = extract_website()

        restaurants.append({
            "restaurant_name": name,
            "rating": rating,
            "total_reviews": total_reviews,
            "category": category,
            "address": address,
            "phone": phone,
            "website": website,
            "google_maps_url": url
        })

        details_df = pd.DataFrame(restaurants)
        details_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

        time.sleep(2)

    except (InvalidSessionIdException, WebDriverException):
        print("Chrome session crashed. Saving progress and stopping safely...")
        break

    except Exception as e:
        print("Error while scraping:", name)
        print(e)
        continue


driver.quit()

print("Details scraping completed or safely stopped.")
print("Saved to:", OUTPUT_FILE)
print("Current saved rows:", len(restaurants))