import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = "sanvihita@gmail.com"
PASSWORD = "Testacc@1"

def linkedin_search(prompt):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Step 1: Login
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Step 2: Search for prompt
    search_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Search')]"))
    )
    search_box.clear()
    search_box.send_keys(prompt)
    search_box.send_keys(Keys.RETURN)

    # Step 3: Wait for results page and click "People" filter
    try:
        people_tab = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='People']"))
        )
    except:
        # Sometimes LinkedIn uses <a> instead of <button>
        people_tab = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='People']"))
        )
    people_tab.click()

    # Step 4: Wait for people results to load
    time.sleep(3)

    # Step 5: Scrape first 20 profiles
    profiles = []
    results = driver.find_elements(By.XPATH, "//li[contains(@class,'reusable-search__result-container')]")[:20]

    for result in results:
        try:
            name_elem = result.find_element(By.XPATH, ".//span[@aria-hidden='true']")
            link_elem = result.find_element(By.TAG_NAME, "a")
            name = name_elem.text.strip()
            link = link_elem.get_attribute("href").split("?")[0]
            if name and "linkedin.com/in" in link:
                profiles.append((name, link))
        except:
            continue

    # Step 6: Save to CSV
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Profile URL"])
        writer.writerows(profiles)

    print(f"✅ Saved {len(profiles)} profiles to results.csv")

    return driver
