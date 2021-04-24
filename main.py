# For web scrapping and downloading files
import requests
from bs4 import BeautifulSoup
import html5lib
import urllib.request

# For command line arguments
from sys import argv

# For user interface
from tqdm import tqdm
import inquirer


if argv[1] == "-p":
    playlist = True
    url = argv[2]
else:
    playlist = False
    url = argv[1]


def make_soup(url):
    html_contents = requests.get(url).text
    soup = BeautifulSoup(html_contents, "html5lib")

    return soup

# Find video title
def get_video_title(soup):
    title = soup.find_all("title")
    title = (title[0]).text
    title = title.strip()

    return title


def find_qualitys(soup):
    qualitys_list = []
    for link in soup.find_all("span"):
        try:
            if(link.get("class")[0] == "text"):
                if("با کیفیت" in link.text):
                    quality = link.text
                    quality = quality.replace("با کیفیت ", "")
                    if(quality not in qualitys_list):
                        qualitys_list.append(quality)
        except TypeError:
            pass

    return qualitys_list

def pick_quality(quality_lists):
    questions = [
        inquirer.List("quality",
            message = "What quality do you want?",
            choices = quality_lists,
        )
    ]

    answers = inquirer.prompt(questions)
    return answers


def find_download_link(soup, quality):
    for link in soup.findAll('a'):
        if(quality in (link.get('href'))):
            return link.get("href")


class Progress_Bar(tqdm):
    def update_to(self, b = 1, bsize = 1, tsize = None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download(download_link, title):
    with Progress_Bar(desc = ("Downloading " + title + ": "), ncols = 100, unit = "B", unit_scale = True, miniters = 1) as t:
            urllib.request.urlretrieve(download_link, title + ".mp4", reporthook = t.update_to)

def download_playlist(soup):
    for link in soup.findAll("a"):
        try:
            if(link.get("class")[0] == "light-80" and link.get("class")[1] == "dark-10"):
                page_url = "https://www.aparat.com" + link["href"]
                new_soup = make_soup(page_url)
                qualitys_list = find_qualitys(new_soup)
                quality = (pick_quality(qualitys_list))["quality"]
                download_link = find_download_link(new_soup, quality)
                download(download_link, get_video_title(new_soup))
        except TypeError:
            pass


soup = make_soup(url)

if playlist == True:
    download_playlist(soup)
else:
    qualitys_list = find_qualitys(soup)
    quality = (pick_quality(qualitys_list))["quality"]
    download_link = find_download_link(soup, quality)
    download(download_link, get_video_title(soup))
