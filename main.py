import requests
from bs4 import BeautifulSoup
import html5lib
import urllib.request

from sys import argv

from tqdm import tqdm
import inquirer

import math


url =  argv[1]


html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "html5lib")


title = soup.find_all("title")
title = (title[0]).text
title = title.strip()


quality_list = []
def find_qualitys(soup):
    for link in soup.find_all("span"):
        try:
            if(link.get("class")[0] == "text"):
                if("با کیفیت" in link.text):
                    quality_str = link.text
                    quality_str = quality_str.replace("با کیفیت ", "")
                    if(quality_str not in quality_list):
                        quality_list.append(quality_str)
        except TypeError: pass

def pick_quality(quality_list):
    questions = [
        inquirer.List("quality",
            message = "What quality do you want?",
            choices = quality_list,
        )
    ]

    answers = inquirer.prompt(questions)
    return answers


class DownloadProgressBar(tqdm):
    def update_to(self, b = 1, bsize = 1, tsize = None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def find_download_link(soup, quality):
    for link in soup.findAll('a'):
        if(quality in (link.get('href'))):
            return link.get("href")

def download(download_link, title):
    with DownloadProgressBar(desc = "Downloading: ", ncols = 100, unit = "B", unit_scale = True, miniters = 1) as t:
            urllib.request.urlretrieve(download_link, title + ".mp4", reporthook = t.update_to)


find_qualitys(soup)
quality = (pick_quality(quality_list))["quality"]
download_link = find_download_link(soup, quality)
download(download_link, title)
