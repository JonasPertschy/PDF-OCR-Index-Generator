import time
import sys
import os
import pyscreenshot as ImageGrab
import pytesseract
sys.path.append(os.path.abspath("SO_site-packages"))
from AppKit import NSWorkspace
from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID
)
import pyperclip
recent_value = pyperclip.paste()

cache = dict() ## remove comment 
def currentWindow():
    curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    curr_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
    curr_app_name = curr_app.localizedName()
    options = kCGWindowListOptionOnScreenOnly
    windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for window in windowList:
        pid = window['kCGWindowOwnerPID']
        windowTitle = window.get('kCGWindowName', u'Unknown')
        if curr_pid == pid:
            windowNumber = window['kCGWindowNumber']
            ownerName = window['kCGWindowOwnerName']
            geometry = window['kCGWindowBounds']
            output = windowTitle.encode('ascii','ignore')
            if 'pdf' in str(output):
                return output.decode("utf-8")
while True:
    tmp_value = pyperclip.paste().replace('\n', ' ').replace('  ',' ')
    if tmp_value != recent_value:
        recent_value = tmp_value
        print(tmp_value)
        window = currentWindow()
        if window:
            book = window[14]
            im = ImageGrab.grab(bbox =(545, 45, 580, 71)) ## modifiy!
            page = book+'-'+str(int(pytesseract.image_to_string(im, config="-l digits --psm 10").strip())-2)
            if page in cache and recent_value != "":
                cache[page].append(recent_value)
            elif recent_value != "":
                cache[page] = [recent_value]
            if page in cache:
                #print('DETECTED PAGE',page)
                print("Page:", page, ','.join(cache[page]))
            
    time.sleep(0.1)
