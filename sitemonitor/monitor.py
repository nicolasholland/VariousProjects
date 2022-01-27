from os.path import join, dirname
from selenium import webdriver
import yaml

with open(join(dirname(__file__), "config.yml")) as yml:
    CFG = yaml.safe_load(yml)

def init_webdriver():
    o = webdriver.ChromeOptions()

    o.add_argument('--headless')
    o.add_argument('--no-sandbox')
    o.add_argument('--disable-dev-shm-usage')
    d = webdriver.Chrome(CFG["path_to_driver"], options=o)
    return d


class SiteCheck(object):
    """
    Examples
    --------
    >>> sc1 = SiteCheck("sitename", CFG["urls"]["sitename"][0])
    >>> sc1.check_available()
    False
    """

    def __init__(self, site, url):
        self.site = site
        self.url = url
        self.driver = init_webdriver()

    def browse(self):
        self.driver.get(self.url)

    def check_available(self):
        self.browse()
        ele = self.driver.find_elements_by_class_name(
            CFG["elements"][self.site])
        text = [_.text for _ in ele]
        return CFG["marker"][self.site] in text

