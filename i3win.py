from workspace import workspace #type: ignore
import win32gui, win32com.client
import ctypes
from ctypes import c_int
import ctypes.wintypes
from ctypes.wintypes import HWND, DWORD
from pynput import keyboard
dwmapi = ctypes.WinDLL("dwmapi")
DWMWA_CLOAKED = 14 
isCloacked = c_int(0)
BLACKLIST = ['NVIDIA GeForce Overlay', 'Program Manager']

shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ) and win32gui.GetWindowText(hwnd) != '' and win32gui.GetWindowText(hwnd) not in BLACKLIST:
        dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DWMWA_CLOAKED), ctypes.byref(isCloacked), ctypes.sizeof(isCloacked))
        if(isCloacked.value == 0):
            # print (hwnd, win32gui.GetWindowText( hwnd ))
            ctx.append(hwnd)

def getWindows():
    cntx = []
    win32gui.EnumWindows( winEnumHandler, cntx )
    return cntx

def focusL():
    w.moveFocus(win32gui.GetForegroundWindow(), 'L')
def focusR():
    w.moveFocus(win32gui.GetForegroundWindow(), 'R')
def focusU():
    w.moveFocus(win32gui.GetForegroundWindow(), 'U')
def focusD():
    w.moveFocus(win32gui.GetForegroundWindow(), 'D')

def moveU():
    w.moveWindow(win32gui.GetForegroundWindow(), 'U')
def moveD():
    w.moveWindow(win32gui.GetForegroundWindow(), 'D')
def moveL():
    w.moveWindow(win32gui.GetForegroundWindow(), 'L')
def moveR():
    w.moveWindow(win32gui.GetForegroundWindow(), 'R')

w = workspace(width=2560, height=1440-40)

for hwnd in getWindows():
    w.addNewWindow(hwnd)

with keyboard.GlobalHotKeys({
    '<alt>+<shift>+j':moveD,
    '<alt>+<shift>+l':moveR,
    '<alt>+<shift>+k':moveU,
    '<alt>+<shift>+h':moveL,

    '<alt>+j': focusD,
    '<alt>+h': focusL,
    '<alt>+l': focusR,
    '<alt>+k': focusU,
}) as h:
    h.join()