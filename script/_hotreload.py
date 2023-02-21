from playwright.sync_api import sync_playwright, TimeoutError
from playwright.sync_api._generated import Page
import time
import sys

sys.path.append("..")

from hstr import *
from hplaywrightExtended import ExtendedLocator, ExtendedPage
# from hplaywright_element import ExtendedLocator

# from main import Gmail #nhớ xóa dòng này khi chạy
# def function1(self: Gmail):
def function1(self):
    p: ExtendedPage = self.p
    p = self.p
    url = p.url
    if not "https://myaccount.google.com/language" in url:
        p.goto("https://myaccount.google.com/language?hl=en&utm_source=google-account&utm_medium=web&pli=1")
    timestart = time.time()
    while time.time() - timestart < 2:
        try:
            url = p.url
            text = p.locatorSelector(".xsr7od").text()
            if "United States" in text:
                return "ok"
            displaylang = False
            enterlang = p.locatorAriaLabel("English")
            if enterlang.isDisplayed():
                displaylang = True
                enterlang.click()
            enterlang = p.locatorAriaLabel("United States")
            if enterlang.isDisplayed():
                displaylang = True
                enterlang.click()
            select = p.locatorText('Select')
            if select.displayed():
                select.click()

            if not displaylang:
                edits = p.locatorSelector("span[class=VfPpkd-kBDsod]").findLocatorDisplay()
                if edits:
                    edits.click(force = True)


        except Exception as e:
            print(e)
        time.sleep(1)
    return "Timeout"




def function2(args):
    classabc = args[0]
    classabc.chay()
