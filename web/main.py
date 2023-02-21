from script._download import *
title = "Gmail Changer"
setupPythonPath(title)


sys.path.append(scriptPathAppend)




from hwin import *
from hthread import *
import eel
from script._sqlalchemy import Session, insert, or_, func

from script._sqlalchemy import mailTable, Database, mailClass, Result
from script.gmail import Gmail



@eel.expose
def openFile(filename):
    hfile.openWithNotepad("/data/" + filename)

@eel.expose
def loadChucNang():
    try:
        lang_en = {
            # "checkinfoyoutube": "Check info youtube",
            # "checkdatecreate": "Check date create",
            "changepass": "Change pass",
            "changeemailrecovery": "Change email recovery",
            # "deletephonerecovery": "Delete phone recovery",
            # "checkemailgmailcom": "Check email @gmail.com",
            # "checkchplay": "Check chplay",
            # "checkgooglevoice": "Check google voice",
            # "checkpaymentmethod": "Check payment method",
            # "deletepaymentmethod": "Delete payment method",
            # "checklivedie": "Check live die",
            # "restoredisable": "Restore disable",
            # "changelanguage": "Change language",
            # "checkgoogleadw": "Check google adw",
            # "checkphonerecovery": "Check phone recovery",
            # "checkcountry": "Check country",
            # "checkgoogleadsense": "Check google adsense",
            # "devicelogout": "Device logout",
            # "closepaymentmethod": "Close payment method",
            # "createchannelyoutue": "Create channel youtue",
            # "confirmsecurity": "Confirm security",
            # "disableimagechrome": "Disable image chrome",
            # "verifyphone": "Verify phone",
            # "verifyyoutube": "Verify youtube"
        }
        return Result(data=lang_en).to_dict()
    except Exception as e:
        return Result(False, "adding mails failed", e.args).to_dict()


@eel.expose
def oimport(iaccount: str):
    try:
        # s = time.time()
        with Database() as db:
            accounts = iaccount.splitlines()
            if hfile.checkExists(accounts[0].strip()):
                accounts = hfile.readLines(accounts[0].strip())
            listdic = []
            for i in accounts:
                line = i.split("|")
                if len(line) < 2:
                    continue
                email, password = map(str.strip, line[:2])
                emailrecovery = line[2].strip() if len(line) > 2 else ""
                dic = {"email": email, "password": password, "emailrecovery": emailrecovery, "status": ""}
                listdic.append(dic)
            # print(time.time() - s)
            # db.execute(insert(Mails), listdic)
            db.bulk_insert_mappings(mailTable, listdic)
            db.commit()
            # print(time.time() - s)
            return Result().to_dict()
    except Exception as e:
        db.rollback()
        return Result(False, "adding mails failed", e.args).to_dict()

def updateMail(id: int, update: mailClass):
    try:
        with Database() as db:
            old_mail = db.query(mailTable).filter(mailTable.id == id).first()
            if not old_mail:
                return Result(False, "id not found")
            if update["email"] and update["email"] != old_mail.email:
                old_emails =  old_mail.email.split('\n')
                if old_mail.email and not old_mail.email in old_emails:
                    old_emails.insert(0, old_mail.email)
                    if "" in old_emails:
                        old_emails.remove("")
                    update["oldpassword"] = '\n'.join(old_emails)
            if update["password"] and update["password"] != old_mail.password:
                old_passwords =  old_mail.oldpassword.split('\n')
                if old_mail.password and not old_mail.password in old_passwords:
                    old_passwords.insert(0, old_mail.password)
                    if "" in old_passwords:
                        old_passwords.remove("")
                    update["oldpassword"] = '\n'.join(old_passwords)
            if update["emailrecovery"] and update["emailrecovery"] != old_mail.emailrecovery:
                old_emailrecoverys = old_mail.oldemailrecovery.split('\n')
                if old_mail.emailrecovery and not old_mail.emailrecovery in old_emailrecoverys:
                    old_emailrecoverys.insert(0, old_mail.emailrecovery)
                    if "" in old_emailrecoverys:
                        old_emailrecoverys.remove("")
                    update["oldemailrecovery"] ='\n'.join(old_emailrecoverys)
            update_dict = {k: v for k, v in update.items() if v}
            db.query(mailTable).filter(mailTable.id == id).update(update_dict)
            db.commit()
            return Result()
    except Exception as e:
        db.rollback()
        return Result(False, "update_mail fail", e.args)

def run(listidaccount):
    for id in listidaccount:
        try:
            #1104
            mail = getMailById(id)
            msg = mail["msg"]
            gmail = Gmail()
            gmail.ck = ck
            gmail.orbita_browser_108_check = orbita_browser_108_check
            gmail.msg = msg
            login = gmail.login(msg["email"], msg["password"], msg["emailrecovery"])
            msg["status"] = login
            updateMail(id, msg)
            if not gmail.rapt:
                gmail.p.close()
                continue
            gmail.changePass()
            print(mail)
        except Exception as e:
            print(e.args)
from hthread import *
@eel.expose
def runAccounts(listidaccount: list):
    hthread.start(run, [listidaccount])

@eel.expose
def quit():
    try:
        hwnd = hwin.getHandleByTitle(title)
        hwin.killHwnd(hwnd)
    except Exception as e:
        print(e)
    hwin.killApp()

@eel.expose
def getTitle():
    return title




def getMailById(id):
    try:
        with Database() as db:
            mail = db.query(mailTable).filter(mailTable.id==id).first()
            if not mail:
                return Result().to_dict()
            db.commit()
            msg={field.name: getattr(mail, field.name) for field in mailTable.__table__.columns}
            return Result(data=msg).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get mail failed", e.args).to_dict()
def get_mail():
    try:
        with Database() as db:
            mail = db.query(mailTable).filter(or_(mailTable.status == None, mailTable.status == "")).first()
            if not mail:
                return Result().to_dict()
            mail.status = "đã dùng"
            db.commit()
            msg={field.name: getattr(mail, field.name) for field in mailTable.__table__.columns}

            return Result(data=msg).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get mail failed", e.args).to_dict()
@eel.expose
def get_count_mail():
    try:
        with Database() as db:
            count = db.query(func.count(mailTable.id)).scalar()
            return Result(data=count).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get get_count_mail failed", e.args).to_dict()


@eel.expose
def get_mails(skip:int = 0, limit:int = 100):
    try:
        with Database() as db:
            mails = db.query(mailTable).offset(skip).limit(limit).all()
            if not mails:
                return Result().to_dict()
            db.commit()
            msg = [{field.name: getattr(mail, field.name) for field in mailTable.__table__.columns} for mail in mails]
            return Result(data=msg).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get mail failed", e.args).to_dict()

@eel.expose
def selectMails():
    try:
        with Database() as db:
            # mails = db.query(mailTable.id).all()
            mails = [id[0] for id in db.query(mailTable.id).all()]
            if not mails:
                return Result().to_dict()
            db.commit()
            data = mails
            return Result(data=data).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get mail failed", e.args).to_dict()
# time.sleep(10)
# for i in range(100):
#     hthread.start(get_mail)



def startEel(port=8786, mode="chrome", folder_init="web", index="index.html", host="localhost"):
    pid = hwin.getPidByPort(port)
    if pid:
        hwin.killPid2(pid)
    eel.init(folder_init)
    eel.start(index, mode=mode, size=(1300, 800), position=(200, 300), host="localhost", port=port)
    quit()





from reload import *

import time

from hplaywright import *




from hmahoa import *
from hthread import *
import importlib


class checkKey:
    def __init__(self, sv, nameapp, delmodule="", keyapp=""):
        if not keyapp:
            keyapp = nameapp
        self.sv = sv
        self.nameapp = nameapp
        self.keyapp = keyapp
        self.hwid = hmahoa.getHwid(keyapp + "24")
        self.message = ""
        self.status = {}
        self.__module = ""
        self.__delmodule = delmodule

    def start(self):

        while True:
            try:
                hashgoc = hmahoa.randomHash()
                hash = hmahoa.encryptAes256(hashgoc, "hash_encryptAes256_server")
                hash_del_module = hmahoa.encryptAes256(self.__delmodule, "hash_encryptAes256_server")
                nameapp = hstr.encodeUrl(self.nameapp)
                url = f"http://{self.sv}:8000/checkkey?hwid={self.hwid}&nameapp={nameapp}&format=json&hash={hash}&del_hash={hash_del_module}"
                text = hmahoa.get(url)
                if not text:
                    self.message = "Cannot load server"
                    time.sleep(1)
                    continue
                content = hmahoa.decryptAes256(text, hashgoc)
                if not content:
                    self.message = text
                    time.sleep(1)
                    continue
                status = json.loads(content)
                hash_response = status.get("hash", "")
                if not hash_response:
                    self.message = "Cannot load hash"
                    time.sleep(1)
                    continue
                keymahoa = hmahoa.decryptAes256(hash_response, hashgoc)
                module = keymahoa.replace("_" + hashgoc, "")
                if not module or module != self.__delmodule:
                    time.sleep(1)
                    continue
                # del socket
                self.message = ""
                self.status = status
                self.status.pop("version")
                self.status.pop("hash")
                self.__module = module

                time.sleep(30)
            except ModuleNotFoundError as e:
                time.sleep(1)
            except Exception as e:
                self.message = e
                time.sleep(1)

    def reloadModule(self):
        function_string = self.__module + "." + self.__module
        mod_name, func_name = function_string.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        # importlib.reload(mod)
        hpw = getattr(mod, func_name)
        hpw = hpw()
        return hpw


# hpw = hplaywright()
# hpw.proxyBypassList = ["appleid.cdn-apple.com", "*.icanhazip.com", "*.clarity.ms", "*.snapchat.com", "accounts.google.com", "*.hotjar.com"]
# proxy = ""
# # proxy = "45.155.68.129:8133:sgtpxvzw:d2x2sf3vd4eh"
# p = hpw.openChrome(proxy, executable=r"C:\Users\Admin\.gologin\browser\orbita-browser-108\chrome.exe")
# # p.goto("https://iphey.com")
# # p.goto("https://browserleaks.com/canvas")
# # p.goto(
# #     "https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?redirect_uri=storagerelay%3A%2F%2Fhttps%2Fwww.textnow.com%3Fid%3Dauth816418&response_type=permission%20id_token&scope=email%20profile%20openid&openid.realm&include_granted_scopes=true&client_id=302791216486-uvga7gfpsv09349lkhe1c8rmg73of0h5.apps.googleusercontent.com&ss_domain=https%3A%2F%2Fwww.textnow.com&fetch_basic_profile=true&gsiwebsdk=2&service=lso&o2v=1&flowName=GeneralOAuthFlow"
# # )
# # p.goto("https://ipv4.icanhazip.com")

# # p.goto("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_link_target")
# p.goto("https://textnow.com/login")
# # time.sleep(100)
# while True:
#     try:
#         content = p.context
#         print("a")
#         # p.locator("#google-login").click()
#         # print()
#     except:
#         pass
#     time.sleep(1)
sv = "45.32.118.181"
# sv = "localhost"
keyapp = "WKQI@!MDAO)Qekj193inaD@!30ADAma"
nameapp = "Gmail Changer"


def deleteModule(delmodule):
    from sys import modules

    del modules[delmodule]
    for mod in modules.values():
        try:
            delattr(mod, delmodule)
        except AttributeError:
            pass


delmodule = "hplaywright"
deleteModule(delmodule)
ck = checkKey(sv, nameapp, delmodule, keyapp)

hthread.start(ck.start)
while True:
    if ck.message:
        print(ck.message)
    if ck.status:
        break
    time.sleep(1)





if __name__ == "__main__":
    startEel(host="127.0.0.1", port= 12312)
    # proxy = "185.199.231.45:8382"
    gmail = Gmail()
    mail = "202006349@udv.edu.gt|Guate@123"
    mails = mail.split("|")
    email = mails[0]
    passs = mails[1]
    # emailkp = mail.split("|")[2]
    emailkp = mails.split("|")[2].strip() if len(mails) > 2 else ""
    gmail.login(email, passs, emailkp)
