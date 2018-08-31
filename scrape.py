import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver import FirefoxOptions

import requests

periods = ["6months", "1year", "2year", "alltime"]

def main():
    login_url = "https://leetcode.com/accounts/login/"

    chrome_opts = webdriver.ChromeOptions()
    #chrome_opts.add_argument("--headless")

    opts = FirefoxOptions()
    #opts.add_argument("--headless")

    # Grab companies
    text_file = open("companies.txt", "r")
    companies = text_file.read().split('\n')
    text_file.close()

    driver = webdriver.Chrome(executable_path=r'/home/arthur/Programming/LeetcodePremiumScraper/chromedriver', chrome_options=opts)
    driver.maximize_window()
    driver.get(login_url)

    driver.find_element_by_id("id_login").send_keys("")
    driver.find_element_by_id("id_password").send_keys("")
    driver.find_element_by_id("id_password").submit()
    time.sleep(4)


    for company in companies:
        lc_url = "https://leetcode.com/company/" + company
        driver.get(lc_url)
        #driver.find_element_by_class_name("reactable-th-frequency").click()

        periods = ["6months", "1year", "2year", "alltime"]
        for period in periods:
            i = input("Please select {}".format(period))

            ans = ""

            soup = BeautifulSoup(driver.find_element_by_xpath(
                 "//*").get_attribute("outerHTML"), "html.parser")

            tables = soup.find_all("tbody", {"class": "reactable-data"})
            rows = soup.find_all("tr")
            for item in rows:
                data = item.find_all("td")
                if len(data) > 5:
                    number = data[1].text
                    title = data[2].text
                    acceptance = data[3].text
                    difficulty = data[4].text
                    frequency = data[5]['value']
                    ans += (number+ "," + title+ ","+ acceptance+ ","+ difficulty+ "," +frequency+ "\n")

            f = open(company + "_" + period, "w")
            f.write(ans)
            f.close()


if __name__ == "__main__":
    main()
