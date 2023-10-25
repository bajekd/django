import datetime
import re
import time

from dateutil.relativedelta import relativedelta
from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .models import ScrapedItem, ScrapeRecord

# class Scraper:
#     def __init__(self, base_url):
#         self.base_url = base_url
#         self.options = webdriver.ChromeOptions()
#         self.options.add_argument(" - incognito")
#         self.browser = webdriver.Chrome(executable_path="./chromedriver", chrome_options=self.options)

#         def scrape_python_tagged_articles_from_dev_to(self):
#             pass


def scrape_python_tagged_articles_from_dev_to(base_url):
    url = f"{base_url}t/python/top/infinity"  # infinity
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito")

    browser = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)
    browser.get(url)
    timeout = 3
    items_save_to_db_counter = 0

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='crayons-story '][last()]"))
        )
    except TimeoutException:
        print(f"{timeout} sec has passed -> Timeout!")
        browser.quit()

    articles = browser.find_elements_by_xpath("//div[@class='crayons-story ']")
    for article in articles:
        result = article.find_element_by_xpath(".//a[@class='crayons-story__hidden-navigation-link']")

        link = result.get_attribute("href")
        # result.text --> .text is only for visible text. For hidden use .get_attribute("textContent")
        title = result.get_attribute("textContent")

        publish_date = article.find_element_by_tag_name("time").text
        if "'" in publish_date:
            # May 31, 2020
            publish_date = datetime.datetime.strptime(publish_date, "%b %d '%y").date()
        else:
            # May 31 --> current year
            publish_date = datetime.datetime.strptime(publish_date, "%b %d")
            today = datetime.date.today()
            publish_date = publish_date.replace(year=today.year).date()

        tags = []
        article_tags = article.find_elements_by_xpath(".//a[@class='crayons-tag']")
        for tag in article_tags:
            tag = tag.text.replace("#", "")
            tags.append(tag)
        article_tags = " ".join(tags)

        likes = article.find_element_by_xpath(
            ".//a[@class='crayons-btn crayons-btn--s crayons-btn--ghost crayons-btn--icon-left']"
        ).text
        likes = re.search("[0-9]+", likes)
        likes = int(likes.group())

        date_no_older_than = getattr(settings, "DEV_TO_ITEMS_DATE_NO_OLDER_THAN")
        reactions_no_less_than = getattr(settings, "DEV_TO_ITEMS_REACTIONS_NO_LESS_THAN")

        if (publish_date >= date_no_older_than) and (likes >= reactions_no_less_than):

            try:
                ScrapedItem.objects.get(link=link, title=title)
            except ScrapedItem.DoesNotExist:
                ScrapedItem.objects.create(
                    source="Dev.to",
                    link=link,
                    title=title,
                    publish_date=publish_date,
                    likes=likes,
                )
                items_save_to_db_counter += 1

    ScrapeRecord.objects.create(source="Dev.to", link=url, items_added=items_save_to_db_counter)
    browser.quit()


def scrape_python_tagged_articles_from_medium_com(base_url):
    url = f"{base_url}tag/python/top/all-time"
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito")

    browser = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)
    browser.get(url)
    timeout = 5
    items_save_to_db_counter = 0

    for _ in range(20):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3)

    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='ae fa']")))
    except TimeoutException:
        print(f"{timeout} sec has passed -> Timeout!")
        browser.quit()

    articles = browser.find_elements_by_xpath("//div[@class='ae fa']")
    for article in articles:
        link = article.find_elements_by_xpath(".//a[@class='bm bn ay az ba bb bc bd be bf bo bp bi bq br']")[
            2
        ].get_attribute("href")
        title = article.find_element_by_xpath(
            ".//h2[@class='as cj hc hd he hf hg hh hi hj hk hl hm hn ho hp hq hr hs ht hu hv gq gs gt hw gv gw ch']"
        ).text

        publish_date = article.find_element_by_xpath(".//p[@class='as b ep au gq ia gs gt gu gv gw av']").text
        if "ago" in publish_date:
            # "4 days ago"
            days_amount = int(publish_date.split()[0])
            dt = relativedelta(days=days_amount)
            publish_date = datetime.date.today() - dt
        elif "," in publish_date:
            # "Jan 7, 2017"
            publish_date = datetime.datetime.strptime(publish_date, "%b %d, %Y").date()
        else:
            # "Jan 7" --> current year
            publish_date = datetime.datetime.strptime(publish_date, "%b %d").date()
            today = datetime.date.today()
            publish_date = publish_date.replace(year=today.year)

        likes = article.find_element_by_xpath(".//button[@class='bm bn ay az ba bb bc bd be bf bo bp bi bq br']").text
        digits = re.search("[0-9]+", likes)
        digits = float(digits.group())
        likes = digits * 1000 if "K" in likes else digits
        likes = int(likes)

        date_no_older_than = getattr(settings, "MEDIUM_COM_ITEMS_DATE_NO_OLDER_THAN")
        reactions_no_less_than = getattr(settings, "MEDIUM_COM_ITEMS_REACTIONS_NO_LESS_THAN")

        if (publish_date >= date_no_older_than) and (likes >= reactions_no_less_than):
            try:
                ScrapedItem.objects.get(publish_date=publish_date, title=title)
            except ScrapedItem.DoesNotExist:
                ScrapedItem.objects.create(
                    source="Medium.com",
                    link=link,
                    title=title,
                    publish_date=publish_date,
                    likes=likes,
                )
                items_save_to_db_counter += 1

    ScrapeRecord.objects.create(source="Medium.com", link=url, items_added=items_save_to_db_counter)
    browser.quit()


# def scrape_python_tagged_jobs_from_bulldogjob(url):
#     soup = BeautifulSoup(bulldogjob, "lxml")

#     for ad in soup.find_all("a", class_="search-list-item"):
#         company = ad.find("div", class_="company").text
#         company = company_spliter(company)
#         companies_great_list.add(company)
