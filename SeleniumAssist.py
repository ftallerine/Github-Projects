#bs4 and selenium modules
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import sys

class PageHasURL(object):
    '''
    Do you know what's going on here

    targetURL, the url that is being check against the driver's
                current url
    returns the WebElement once it has a particular url
    '''
    def __init__(self, targetURL):
        self.targetURL = targetURL

    def __call__(self, driver):
        if driver.current_url == self.targetURL:
            return True
        else:
            return False


def WaitForPage(wait_obj, pageurl, max_wait):
    timer = 0
    PageLoaded = False
    while (not (PageLoaded) and timer < 30):
        try:
         PageLoaded = wait_obj.until(PageHasURL(pageurl))
        except TimeoutException:
            time.sleep(timer)
            timer += 5
    return PageLoaded

def IsElementVisible(wait_obj, locator , max_wait):
    timer = 0
    Wait = wait_obj
    elementVisible = False
    while (not (elementVisible) and timer < max_wait):
        try:
            elemnent = Wait.until(
                (EC.visibility_of_element_located(locator))
            )
            elementVisible = True
        except TimeoutException:
            time.sleep(timer)
            timer += 5
    return elementVisible


