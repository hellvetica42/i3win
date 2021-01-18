from window import window
from workspace import workspace
import win32gui
import ctypes
from ctypes import c_int
import ctypes.wintypes
from ctypes.wintypes import HWND, DWORD
from pynput import keyboard
dwmapi = ctypes.WinDLL("dwmapi")
DWMWA_CLOAKED = 14 
isCloacked = c_int(0)
BLACKLIST = ['NVIDIA GeForce Overlay', 'Program Manager']

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ) and win32gui.GetWindowText(hwnd) != '' and win32gui.GetWindowText(hwnd) not in BLACKLIST:
        dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(DWMWA_CLOAKED), ctypes.byref(isCloacked), ctypes.sizeof(isCloacked))
        if(isCloacked.value == 0):
            print (hwnd, win32gui.GetWindowText( hwnd ))
            ctx.append(hwnd)

def getWindows():
    cntx = []
    win32gui.EnumWindows( winEnumHandler, cntx )
    return cntx

print(getWindows())
