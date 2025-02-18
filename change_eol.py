#Launches Notepad++ with a RaspberryPi based file and forces
#end of line encoding to Unix.

###TODO: make sure window is actually NPP
###TODO: Get process id of notepad++ and get child processes to get right window.

###TODO: Launch NPP. Then get window.

import win32api, win32gui, win32con
import sys

#N++ MESSAGE CONSTANTS
NPPM_GETCURRENTDOCINDEX = 2047
NPPM_GETCURRENTBUFFERID = 2084
NPPM_GETBUFFERFORMAT = 2092
NPPM_SETBUFFERFORMAT = 2093

handles = []


#Function passed to EnumWindows
def load(hwnd, lparam=None):
    global handles
    
    wnd_text = win32gui.GetWindowText(hwnd)
    
    if wnd_text.endswith(" - Notepad++"):
        print(hwnd, wnd_text)
        handles += [hwnd]

#Get a list of windows whose text ends with " - Notepad++"
def gethandles():
    global handles
    handles = []
    win32gui.EnumWindows(load, "")


#Apply selected arg (0=winCRLF, 1=macCR, 2=unixLF)
eol_arg = int(sys.argv[1])

if eol_arg not in [0, 1, 2]:
    raise Exception


#Try to find window until its loaded
#TODO: Add timeout
while True:
    gethandles()
    
    if len(handles) > 0:
        break

handle = handles[0]


#Show window if it is hidden
win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
            

CurrentDocIndex = win32api.SendMessage(handle, NPPM_GETCURRENTDOCINDEX, 0, 0)
CurrentBufferID = win32api.SendMessage(handle, NPPM_GETCURRENTBUFFERID, 0, 0)

print("Doc index:", CurrentDocIndex, "Buffer ID:", CurrentBufferID)


#Check and change EOL setting to UNIX
BUFFERFORMATS = ["CRLF", "CR", "LF", "Unknown"]


def CurrentBufferFormat():
        return win32api.SendMessage(handle, NPPM_GETBUFFERFORMAT, CurrentBufferID, 0)

print("EOL was:", BUFFERFORMATS[CurrentBufferFormat()])
win32api.SendMessage(handle, NPPM_SETBUFFERFORMAT, CurrentBufferID, eol_arg)
print("EOL is:", BUFFERFORMATS[CurrentBufferFormat()])