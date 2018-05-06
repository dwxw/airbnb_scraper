#!/usr/local/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class BasePage(object):
    """Bass class for scraping classes"""

    def __init__(self, driver):
        self.driver = driver


class PropertyPage(BasePage):
    """Basic information about an Airbnb property"""

    def __init__(self, url, driver):
        self.url = url
        super().__init__(driver)

        try:
            self.driver.get(self.url)

            self.summary_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='summary']"))
            )
        except NoSuchElementException:
            print("Summary not located, something went wrong.")
            raise

    def property_name(self):
        try:
            return self.summary_element.find_element_by_xpath("//h1").text
        except NoSuchElementException:
            return "Unknown"

    def property_type(self):
        try:
            type_text = self.summary_element.find_element_by_xpath("//span[@class='_bt56vz6']").text
            return type_text.split(' ')[1].capitalize()
        except NoSuchElementException:
            return "Unknown"

    def number_of_bedrooms(self):
        try:
            bedroom_text = self.summary_element.find_element_by_xpath("//div[@class='_36rlri'][2]//span[@class='_y8ard79']").text
            return 0 if 'Studio' in bedroom_text else bedroom_text.split(' ')[0]
        except NoSuchElementException:
            return "Unknown"

    def number_of_bathrooms(self):
        try:
            bathroom_text = self.summary_element.find_element_by_xpath("//div[@class='_36rlri'][4]//span[@class='_y8ard79']").text
            return bathroom_text.split(' ')[0]
        except NoSuchElementException:
            return "Unknown"

    def amenities(self):
        try:
            amenities = self.driver.find_element_by_xpath("//div[contains(.//span, 'Amenities')]")
            amenities_btn = amenities.find_element_by_tag_name("button")
            amenities_btn.click()
            all_amenities = driver.find_elements_by_xpath("//div[@class='_wpwi48']//div[@class='_rotqmn2']")
            return [a.text for a in all_amenities]
        except NoSuchElementException:
            return []


if __name__ == "__main__":

    print("Retrieving property info from Airbnb")

    PROPERTY_URLS = [
        "https://www.airbnb.co.uk/rooms/14531512?s=51",
        "https://www.airbnb.co.uk/rooms/19278160?s=51",
        "https://www.airbnb.co.uk/rooms/19292873?s=51",
    ]

    driver = webdriver.Chrome()

    for property_url in PROPERTY_URLS:

        print(property_url)

        try:
            property_page = PropertyPage(property_url, driver)

            print("Name: {}\nType: {}\nBedrooms: {}\nBathrooms: {}\nAmenities:".format(
                property_page.property_name(),
                property_page.property_type(),
                property_page.number_of_bedrooms(),
                property_page.number_of_bathrooms()))
            for a in property_page.amenities():
                print("    {}".format(a))
        except:
            print("Failed to retrieve property info.")

        print()

    driver.close()
