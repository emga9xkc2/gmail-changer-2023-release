import sys, signal, os, threading, hashlib
import zipfile
import requests, shutil
from distutils.dir_util import copy_tree
from os import listdir
import io, os, sys, random, re, time
import winreg as reg

# PYTHONPATH=...


class hfile:
    def dirScript():
        file_path = sys.path[0]
        if not ":" in file_path:
            file_path = os.getcwd()
        return file_path

    def fixFileName(filename):
        platform = sys.platform
        if platform.endswith("win32"):
            if not ":" in filename:
                filename = hfile.dirScript() + "/" + filename
        filename = filename.replace("\\", "/")
        while True:
            if "//" in filename:
                filename = filename.replace("//", "/")
            else:
                break
        if platform.endswith("win32"):
            filename = filename.replace("/", "\\")
        elif platform.startswith("linux"):
            filename = filename.replace("\\", "/")
        return filename

    def listDir(dir2):
        dir2 = hfile.fixFileName(dir2)
        return next(os.walk(dir2))[1]

    def copyDir(src, dst):
        try:
            src = hfile.fixFileName(src)
            dst = hfile.fixFileName(dst)
            copy_tree(src, dst)
        except Exception as e:
            pass

    def createDir(dir):
        dir = hfile.fixFileName(dir)
        os.makedirs(dir, exist_ok=True)

    def checkExists(fileorfoler):
        fileorfoler = hfile.fixFileName(fileorfoler)
        if fileorfoler == None:
            return False
        return os.path.exists(fileorfoler)

    def writeFile(filename, text):
        f = open(filename, "w", encoding="utf-8")
        f.write(text)
        f.close()

    def readFile(filename):
        try:
            f = open(filename, "r", encoding="utf-8")
            return f.read()
        except:
            return ""

    def deleteDir(dir):
        dir = hfile.fixFileName(dir)
        shutil.rmtree(dir)

    def deleteFile(filename):
        try:
            os.remove(filename)
        except Exception as e:
            print("removeFile", e)
            pass

    def extractZip(pathzip, folder, filenamedes=None):
        if not filenamedes:
            filenamedes = pathzip
        print("Extracting: " + filenamedes)
        pathzip = hfile.fixFileName(pathzip)
        folder = hfile.fixFileName(folder)
        with zipfile.ZipFile(pathzip, "r") as zip_ref:
            folderextract = hfile.fixFileName(folder)
            zip_ref.extractall(folderextract)
        hfile.deleteFile(pathzip)
        print("Extract Success")

hfile.createDir("/data/")

from tqdm import tqdm


def startThread(funcname, list_args=None):
    if not list_args:
        list_args = []
    tuple_args = tuple(list_args)
    thread = threading.Thread(target=funcname, args=tuple_args)
    thread.isDaemon = True
    thread.start()
    return thread


def getIdDrive(id):
    if id.startswith("https://drive.google.com/file/d/"):
        id = id.replace("https://drive.google.com/file/d/", "")
        id = id.split("/")[0]
        id = id.split("?")[0]
    return id


def downloadDrive(id, destination, filenamedes=None):
    id = getIdDrive(id)
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    params = {"id": id, "confirm": "t"}
    if not filenamedes:
        filenamedes = id
    print("Downloading " + filenamedes)
    response = session.get(URL, params=params, stream=True)
    token = ""
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break
    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)
    saveResponse(response, destination)


def download(url: str, fname: str):
    resp = requests.get(url, stream=True)
    saveResponse(resp, fname)


def saveResponse(resp, fname):
    total = int(resp.headers.get("content-length", 0))
    # Can also replace 'file' with a io.BytesIO object
    with open(fname, "wb") as file, tqdm(
        desc="Downloading",
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    print("Download Success")


def createShortcut(title, target="", wDir="", arguments="", icon=""):
    try:
        if title == "" or title == ".lnk":
            title = "Main.lnk"
        if os.path.exists(title):
            return
        path = hfile.fixFileName(title)
        target = hfile.fixFileName(target)
        wDir = hfile.fixFileName(wDir)
        arguments = hfile.fixFileName(arguments)
        icon = hfile.fixFileName(icon)
        if not hfile.checkExists(icon):
            icon = hfile.fixFileName("setup/images/icon.ico")
        from win32com.client import Dispatch

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.Arguments = arguments
        shortcut.WorkingDirectory = wDir
        if icon == "":
            pass
        else:
            shortcut.IconLocation = icon
        shortcut.save()
    except Exception as e:
        pass


def roaming():
    platform = sys.platform
    if platform.endswith("win32"):
        d = "~/appdata/roaming"
    elif platform.startswith("linux"):
        d = "~/.local/share"
    elif platform.endswith("darwin"):
        d = "~/Library/Application Support"
    else:
        d = "~"
    return os.path.abspath(os.path.expanduser(d))


roamingPath = roaming()
scriptPath = roamingPath + "\\nightowl\\myscript\\"
orbitaPath = roamingPath + "\\nightowl\\orbita\\"
tempPath = roamingPath + "\\nightowl\\temp\\"
chromeProfile = roamingPath + "\\nightowl\\chrome\\"
sshPath = roamingPath + "\\nightowl\\ssh\\"
hfile.createDir(sshPath)
hfile.createDir(scriptPath)
hfile.createDir(orbitaPath)
hfile.createDir(tempPath)


def md5(str2):
    return hashlib.md5(str2.encode("utf-8")).hexdigest()


def fixFileGithub(url, folderMain, folderExtract):
    if "/my-script/" in url:
        if hfile.checkExists(folderMain):
            hfile.copyDir(folderMain, folderExtract)
            hfile.deleteDir(folderMain)


def downloadExtract(url, folderExtract, fileNameCheckDownloadDone=None):
    if fileNameCheckDownloadDone:
        if folderExtract in fileNameCheckDownloadDone:
            fileNameCheckDownloadDone = fileNameCheckDownloadDone.replace(folderExtract, "")
        if hfile.checkExists(folderExtract + "//" + fileNameCheckDownloadDone):
            return
    tempFile = tempPath + md5(url) + ".zip"
    if url.startswith("https://drive.google.com"):
        downloadDrive(url, tempFile, fileNameCheckDownloadDone)
    else:
        download(url, tempFile)
    hfile.extractZip(tempFile, folderExtract, fileNameCheckDownloadDone)
    fixFileGithub(url, folderExtract + "/my-script-main/", folderExtract)
    if fileNameCheckDownloadDone:
        return downloadExtract(url, folderExtract, fileNameCheckDownloadDone)


downloadSSH = True
sshPath_check = sshPath + "stnlc.exe"
downloadOrbita108 = True
orbita_browser_108_check = orbitaPath + "orbita-browser-108\\chrome.exe"
orbita_font_check = orbitaPath + "fonts\\noto_sans_cjk_sc_black.otf"
orbita_profiles_check = orbitaPath + "profiles\\zero_profile\\Default\\Preferences"
scriptPath_check = scriptPath + "hplaywright.py"


def downloadThread():
    downloadExtract("https://github.com/emga9xkc2/my-script/archive/refs/heads/main.zip", scriptPath, scriptPath_check)

    if downloadOrbita108:
        downloadExtract("https://drive.google.com/file/d/1iZjyC-WYjaeFJL5GPyRFiKwAtW18Ofwx/view?usp=sharing", orbitaPath, orbita_browser_108_check)
        downloadExtract("https://drive.google.com/file/d/1iTU2PH7Y8kmD1pHHW1C6pYcR0yxaQx-5/view?usp=sharing", orbitaPath, orbita_font_check)
        downloadExtract("https://drive.google.com/file/d/1ieSpNuItcE2-1syKDhZmDe6TPDBLMTMX/view?usp=sharing", orbitaPath, orbita_profiles_check)

    if downloadSSH:
        downloadExtract("https://drive.google.com/file/d/1icrqJrA0tcvhBL1FBwL8XHovZ1stllry/view?usp=sharing", sshPath, sshPath_check)


startThread(downloadThread)

scriptPathAppend = "D:/Google Drive/My Data/python/myscript/"
if not os.path.exists(scriptPathAppend):
    scriptPathAppend = scriptPath


def setupPythonPath(title):
    filename = "main.py"
    filename = hfile.fixFileName(filename)
    if not hfile.checkExists(filename):
        filename = "main.pyc"
        filename = hfile.fixFileName(filename)
    createShortcut(title.split("_")[0].strip().upper() + ".lnk", r"C:\Windows\py.exe", "", '"' + filename + '"', "web/static/favicon.ico")



printer = False
lasttime = time.time()


def waitDownload(path):
    global printer, lasttime
    if printer:
        if time.time() - lasttime > 20:
            lasttime = time.time()
        else:
            return
    print("Wait download", path)
    printer = True


while True:
    if not hfile.checkExists(scriptPath_check):
        waitDownload(scriptPath_check)
        time.sleep(1)
        continue
    elif not hfile.checkExists(orbita_browser_108_check):
        waitDownload(orbita_browser_108_check)
        time.sleep(1)
        continue
    elif not hfile.checkExists(orbita_font_check):
        waitDownload(orbita_font_check)
        time.sleep(1)
        continue
    elif not hfile.checkExists(orbita_profiles_check):
        waitDownload(orbita_profiles_check)
        time.sleep(1)
        continue
    else:
        break
