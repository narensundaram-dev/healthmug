import os
import sys
import math
import time
import json
import argparse
import traceback
from datetime import datetime as dt
from concurrent.futures import as_completed, ThreadPoolExecutor

import requests
import pandas as pd
from bs4 import BeautifulSoup, NavigableString

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from constants import *
from soup import extract
from logger import get_logger


log = get_logger(__file__)


class HealthMugScraper(object):

    dir_output = "output"
    
    def __init__(self, category, page_from, page_to, settings, args):
        self.args = args
        self.base_url = BASE_URL
        self.category = category
        self.category_id = CATEGORIES[self.category]["id"]
        self.page_from = page_from
        self.page_to = page_to
        self.settings = settings
        self.dir_output = os.path.join(HealthMugScraper.dir_output, self.category)
        self.xl_output = os.path.join(self.dir_output,
                                      "{}_{}_{}.xlsx".format(self.category, self.page_from, self.page_to))
        self.url_product_failed = []
        self.data = []

    def get_urls(self):
        pgno = self.page_from
        url_products = []
        while True:
            url = URL_PRODUCTLIST.format(category_id=self.category_id, pgno=pgno)
            response = requests.get(url).json()
            items = response["itemlist"]["items"]
            if not items or pgno > self.page_to:
                break
            
            for item in items:
                url_product = self.base_url + item["url"]
                url_products.append(url_product)

            log.info("Fetched product urls from: {}".format(url.format(pgno)))
            pgno += 1
        return url_products

    def get_info(self, url_product):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        log_path = '/dev/null' if sys.platform == "linux" else "NUL"
        chrome = webdriver.Chrome(self.settings["driver_path"]["value"], chrome_options=options, service_log_path=log_path)
        chrome.get(url_product)
        try:
            wait = self.settings["page_load_timeout"]["value"]
            WebDriverWait(chrome, wait).until(EC.presence_of_element_located((By.CLASS_NAME, "prodcutDetailTitle")))
            soup = BeautifulSoup(chrome.page_source, "html.parser")
            info = extract(soup)
            info["url[do-not-delete]"] = url_product
            return info
        except (TimeoutException, Exception) as err:
            log.error(f"Error on loading the product info: {url_product}")
            log.error(f"Error Message: {err}")
            self.url_product_failed.append(url_product)
        finally:
            chrome.close()

    def get(self):
        url_products = self.get_urls()

        count, workers = 1, self.settings["workers"]["value"]
        with ThreadPoolExecutor(max_workers=workers) as executor:        
            for info in executor.map(self.get_info, url_products):
                if info:
                    self.data.append(info)
                if count % 20 == 0:
                    log.info("So far {} has been fetched ...".format(count))
                count += 1

    def save(self):
        df = pd.DataFrame(self.data)
        df.to_excel(self.xl_output, index=False)
        log.info("Fetched data has been stored in {} file".format(self.xl_output))
        
        with open("url_failed.txt", "a+") as f:
            f.write("\n".join(self.url_product_failed))
            log.info("Failed URLs has been updated in url_failed.txt")

    def setup(self):
        os.makedirs(self.dir_output, exist_ok=True)


def list_category():
    info = {}
    for category in CATEGORIES:
        pgno, category_id = 1, CATEGORIES[category]["id"]
        response = requests.get(URL_PRODUCTLIST.format(category_id=category_id, pgno=pgno)).json()
        count = response["itemlist"]["count"]
        info[category] = count
    
    sno = 1
    print("sno | category | count | pages")
    print("------------------------------")
    for k, v in info.items():
        pages = math.ceil(v/20)
        print("{}. {} - {} - {}".format(sno, k, v, pages))
        sno += 1


def get_settings():
    with open("settings.json", "r") as f:
        return json.load(f)


def validate_args(args):
    if args.category:
        if not (args.page_from or args.page_to):
            raise Exception("-p1 && -p2 args are required!")


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-lc', "--list_category", action='store_true', required=False)
    arg_parser.add_argument('-c', "--category", type=str, choices=list(CATEGORIES.keys()), required=False)
    arg_parser.add_argument('-p1', "--page_from", type=int, required=False)
    arg_parser.add_argument('-p2', "--page_to", type=int, required=False)
    arg_parser.add_argument('-log-level', '--log_level', type=str, choices=(INFO, DEBUG), default=INFO)
    return arg_parser.parse_args()


def main():
    start = dt.now()
    log.info("Script starts at: {}".format(start.strftime("%d-%m-%Y %H:%M:%S %p")))

    args = get_args()
    validate_args(args)

    if args.list_category:
        list_category()

    elif args.category:
        settings = get_settings()
        healthmug = HealthMugScraper(args.category, args.page_from, args.page_to, settings, args)

        healthmug.setup()
        healthmug.get()
        healthmug.save()
    
    end = dt.now()
    log.info("Script ends at: {}".format(end.strftime("%d-%m-%Y %H:%M:%S %p")))
    elapsed = round(((end - start).seconds / 60), 4)
    log.info("Time Elapsed: {} minutes".format(elapsed))


if __name__ == "__main__":
    main()
