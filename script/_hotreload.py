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
    emailtest = self.emailrecovery
    if not "@" in emailtest:
        emailtest = self.user
    if not "@" in emailtest:
        emailtest = self.user + "@gmail.com"
    dau = emailtest.split("@")[0]
    duoi = "hotmail.com"
    newemailrecovery = dau + "1@" + duoi
    p = self.p
    url = p.url
    if not url.startswith("https://myaccount.google.com/recovery/email"):
        p.goto("https://myaccount.google.com/recovery/email?hl=en&rapt=" + self.rapt)
    timestart = time.time()
    while time.time() - timestart < 60:
        try:
            url = p.url
            if url.startswith("https://myaccount.google.com/recovery/email"):
                pass

            # url = p.url
            verifiCode = p.locatorSelector('*[maxlength="6"]')
            if verifiCode.first.is_visible(timeout=1000):
                return "ok"
            newEmail = p.locatorSelector('*[type="email"]')
            if newEmail.displayed():
                self.data["emailrecovery"] = newemailrecovery
                self.updateMail()
                newEmail.type(newemailrecovery, press="Enter")
                time.sleep(5)
        except Exception as e:
            print(e)
        time.sleep(1)
    return "Timeout"




def function2(args):
    classabc = args[0]
    classabc.chay()
