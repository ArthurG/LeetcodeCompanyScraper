import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os

from selenium.webdriver import FirefoxOptions

import requests

periods = ["6months", "1year", "2year", "alltime"]

def main():
    if not os.path.exists("scraped"):
        os.makedirs("scraped")

    login_url = "https://leetcode.com/accounts/login/"

    chrome_opts = webdriver.ChromeOptions()
    #chrome_opts.add_argument("--headless")

    opts = FirefoxOptions()
    #opts.add_argument("--headless")

    # Grab companies
    text_file = open("companies.txt", "r")
    companies = text_file.read().split('\n')
    text_file.close()

    driver = webdriver.Chrome(executable_path=r'./chromedriver', chrome_options=opts)
    driver.maximize_window()
    driver.get(login_url)

    username = input("Enter username/email: ")
    passwd = input("Enter password: ")

    time.sleep(5)

    while True:
        try:
            driver.find_element_by_id("id_login").send_keys(username)
            driver.find_element_by_id("id_password").send_keys(passwd)
            driver.find_element_by_id("signin_btn").click();
            break;
        except:
            time.sleep(1)

    time.sleep(5)

    for company in companies:
        lc_url = "https://leetcode.com/company/" + company
        driver.get(lc_url)

        periodNames = ['6months', '1year', '2year', 'alltime']
        periodSelectors = ["react-select-2--option-0", "react-select-2--option-1", "react-select-2--option-2", "react-select-2--option-3" ]
        for period_selector, period_name in zip(periodSelectors, periodNames):
            while True:
                try:
                    driver.find_element_by_class_name('Select-control').click();
                    break
                except:
                    print("Dropdown menu not found. Retrying.")
                    # quick hack to make the question bubble go away
                    try:
                        driver.find_element_by_id('app').click();
                        time.sleep(1)
                    except:
                        break

            try:
                time.sleep(0.05)
                driver.find_element_by_id(period_selector).click()
            except:
                try:
                     print("Dropdown menu item not found. Continuing.")
                     # quick hack to make the dropdown go away
                     driver.find_element_by_id('app').click();
                     continue
                except:
                    continue

            time.sleep(0.05)

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
                    if data[5].get("value"):
                        frequency = data[5]['value']
                    else:
                        frequency = 'N/A'
                    ans += (number+ "," + title+ ","+ acceptance+ ","+ difficulty+ "," +frequency+ "\n")

            f = open("./scraped/" + company + "_" + period_name, "w")
            f.write(ans)
            f.close()


if __name__ == "__main__":
    main()

