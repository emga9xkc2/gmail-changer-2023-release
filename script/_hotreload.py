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
    url = p.url
    newPwd = p.locatorName("password")
    newRePwd = p.locatorName("confirmation_password")
    if newPwd.isDisplayed() and newRePwd.isDisplayed():
        newPwd.type("hxjyVNwOTPPH1")
        newRePwd.type("hxjyVNwOTPPH1", press="Enter")
        newRePwd.waitHidden()
        print("abc")
    if url.startswith("https://myaccount.google.com/security-checkup-welcome"):
        return "ok"




def function2(args):
    classabc = args[0]
    classabc.chay()
