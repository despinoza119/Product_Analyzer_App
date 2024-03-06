import numpy as np
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def scrapper(head, produbuscar, nombre_archivo):
    option = webdriver.ChromeOptions()
    option.add_argument(head)
    driver = uc.Chrome(options=option)

    name_list = []
    price_list = []
    image_list = []
    seller_name_list = []
    seller_rating_list = []
    condition_list = []

    driver.get("https://www.ebay.com/")

    input = produbuscar
    keywords = driver.find_element(By.XPATH, '//input[@class="gh-tb ui-autocomplete-input"]')
    # To clear the searchbar
    keywords.clear()
    # Puts the input in the search bar
    keywords.send_keys(input)
    # Clicks search
    search_bt = driver.find_element(By.XPATH, '//input[@class="btn btn-prim gh-spr"]').click()

    # Getting the links for each product
    products = driver.find_elements(By.XPATH, '//div[@class="s-item__info clearfix"]/a')
    link_list = []
    for product in products:
        link_list.append(product.get_attribute('href'))

    for link in link_list:
        sleep(2)
        driver.get(link)
        try:
            name_list.append(driver.find_element(By.XPATH, '//h1[@class="x-item-title__mainTitle"]/span').text)
            price_list.append(driver.find_element(By.XPATH, '//div[@class="x-price-primary"]/span').text)
            try:
                image = driver.find_element(By.XPATH,
                                            '//div[@class="ux-image-carousel-item image-treatment active  image"]/img')
                image_list.append(image.get_attribute('src'))
            except:
                print("Could not process image. Try another way")
                image_list.append(np.nan)
            seller_name_list.append(
                driver.find_element(By.XPATH, '//div[@class="x-sellercard-atf__info__about-seller"]/a/span').text)
            seller_rating_list.append(
                driver.find_element(By.XPATH, '//li[@data-testid="x-sellercard-atf__data-item"]/a/span').text)
            condition_list.append(driver.find_element(By.XPATH, '//div[@class="ux-icon-text"]/span/span/span').text)

        except:
            name_list.append(np.nan)
            price_list.append(np.nan)
            image_list.append(np.nan)
            seller_name_list.append(np.nan)
            seller_rating_list.append(np.nan)
            condition_list.append(np.nan)

    df = pd.DataFrame({"Product": name_list,
                       "Price": price_list,
                       "Image": image_list, "Seller Name": seller_name_list,
                       "Seller Rating": seller_rating_list,
                       "Condition": condition_list})
    df.dropna(axis=0, inplace=True)

    df.to_excel(f"output/{nombre_archivo}.xlsx", index=False)
    print(f"{produbuscar}.xlsx creado con exito")





