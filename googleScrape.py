import pandas as pd
from splinter import Browser
import argparse

parser = argparse.ArgumentParser(description='Google Search scraper')
parser.add_argument(
    '-k', '--keyword', help='Keyword you want to scrape', required=True)
parser.add_argument(
    '-p', '--page', help='How many pages you want to scrape', required=True)
args = parser.parse_args()

browser = Browser('chrome')


browser.driver.set_window_size(640, 480)
browser.visit('https://www.google.com')
search_bar_path = '//*[@id="lst-ib"]'
search_bar = browser.find_by_xpath(search_bar_path)[0]
search_bar.fill(args.keyword)
search_button_path = '//*[@id="tsf"]/div[2]/div[3]/center/input[1]'
search_button = browser.find_by_xpath(search_button_path)[0]
search_button.click()
scraped_data = []
page_num = int(args.page)


def get_page_results(browser):
    global scraped_data
    search_results_xpath = '//h3[@class="r"]/a'
    search_results = browser.find_by_xpath(search_results_xpath)
    for search_result in search_results:
        title = search_result.text.encode('utf8')
        link = search_result['href']
        scraped_data.append((title, link))


get_page_results(browser)

for i in range(2, page_num):
    page_button_xpath = '//*[@id="nav"]/tbody/tr/td[' + str(i + 1) + ']/a'
    browser.is_element_not_present_by_xpath(page_button_xpath, wait_time=1)
    page_button = browser.find_by_xpath(page_button_xpath)[0]
    page_button.click()
    get_page_results(browser)


df = pd.DataFrame(data=scraped_data, columns=['Title', 'Link'])
df.to_csv('links.csv')
browser.quit()
