#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time

# Initialize the WebDriver with Firefox options
options = Options()
# Optional: Enable headless mode if you don't need the browser UI
# options.add_argument('--headless')

# Initialize the WebDriver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

links = []

try:
    driver.get("https://www.amazon.com/s?k=mens+clothing&i=fashion-mens-intl-ship&crid=11Z8ZPUTC4H6P&sprefix=mens+clothing%2Cfashion-mens-intl-ship%2C376&ref=nb_sb_noss_2")

    first_click =driver.find_element(By.XPATH,"/html/body/div/div/a")
    first_click.click()
   
    driver.get("https://www.amazon.com/s?k=mens+clothing&i=fashion-mens-intl-ship&crid=11Z8ZPUTC4H6P&sprefix=mens+clothing%2Cfashion-mens-intl-ship%2C376&ref=nb_sb_noss_2")


    while len(links) < 1000:
        # Wait for the links to load and be clickable
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")))
        # Collect links
        page_links = [element.get_attribute('href') for element in driver.find_elements(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")]
        
        links.extend(page_links)
        links = list(set(links))  # Remove duplicates if needed

        if len(links) >= 1000:
            break

        # Try to find the Next button and click it to go to the next page
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".s-pagination-item.s-pagination-next")))
            next_button.click()
            time.sleep(2)  # Adjust sleep time based on your internet speed and how quickly the page loads
        except Exception as e:
            print("Could not find the 'Next' button or no more pages are available.")
            break

finally:
    driver.quit()

# Trim the list to 1000 links if it exceeded the limit
links = links[:1000]

print(f"Collected {len(links)} links.")
# Do something with the links, like printing them or processing them further.


# In[3]:


for url in links:
    print(url)


# In[5]:


# Initialize the WebDriver with Firefox options
options = Options()
# Optional: Enable headless mode if you don't need the browser UI
# options.add_argument('--headless')

# Initialize the WebDriver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

links = []

try:
    driver.get("https://www.amazon.com/s?k=mens+clothing&i=fashion-mens-intl-ship&crid=11Z8ZPUTC4H6P&sprefix=mens+clothing%2Cfashion-mens-intl-ship%2C376&ref=nb_sb_noss_2")

    first_click = driver.find_element(By.XPATH, "/html/body/div/div/a")
    first_click.click()

    driver.get("https://www.amazon.com/s?k=mens+clothing&i=fashion-mens-intl-ship&crid=11Z8ZPUTC4H6P&sprefix=mens+clothing%2Cfashion-mens-intl-ship%2C376&ref=nb_sb_noss_2")

    while len(links) < 10: 
        # Wait for the links to load and be clickable
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")))
        # Collect links
        page_links = [element.get_attribute('href') for element in
                      driver.find_elements(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")]

        links.extend(page_links)
        links = list(set(links))  # Remove duplicates if needed

        if len(links) >= 10:  # Break if we have collected information from 10 products
            break

        # Try to find the Next button and click it to go to the next page
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".s-pagination-item.s-pagination-next")))
            next_button.click()
            time.sleep(2)  # Adjust sleep time based on your internet speed and how quickly the page loads
        except Exception as e:
            print("Could not find the 'Next' button or no more pages are available.")
            break

    # Now let's visit each product page and extract information
    for link in links:
        driver.get(link)
        
        # Example: Extracting product title and price
        try:
            title = wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text
        except Exception as e:
            title = "N/A"

        try:
            price = wait.until(EC.presence_of_element_located((By.ID, "priceblock_ourprice"))).text
        except Exception as e:
            price = "N/A"
        
        # Print or store the extracted information
        print("Title:", title)
        print("Price:", price)
        print("URL:", link)
        print("")

finally:
    driver.quit()


# In[ ]:


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# Reinitialize the WebDriver for further operations
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

product_details_list = []  # List to store details of all products

for link in links:
    try:
        # Navigate to the product page
        driver.get(link)

        # Wait for the product details section to load
        wait.until(EC.visibility_of_element_located((By.ID, "detailBullets_feature_div")))

        product_details = {"productUrl": link}  # Dictionary to store details of a single product

        # Extracting ASIN directly from the URL
        asin = link.split('/dp/')[1].split('/')[0]
        product_details["productId"] = asin

        # Find the 'detailBullets_feature_div' and then extract information from its 'li' elements
        detail_bullets = driver.find_element(By.ID, "detailBullets_feature_div")
        lis = detail_bullets.find_elements(By.CSS_SELECTOR, "span.a-list-item")  # Find all 'li' elements within the div

        for li in lis:
            text = li.text.split('\n')
            if len(text) >= 2:  # Making sure there's a key-value pair
                key = text[0].strip(': ')
                value = text[1]
                product_details[key] = value

        product_details_list.append(product_details)  # Add the details to the list

    except Exception as e:
        print(f"Failed to extract details for {link}: {e}")

driver.quit()  # Close the WebDriver

# At this point, product_details_list contains the details of all visited products.
# You can print it, save it to a file, or process it further as needed.


# In[ ]:




