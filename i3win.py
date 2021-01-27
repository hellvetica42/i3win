from workspace import workspace 
from desktop import desktop
import win32gui, win32com.client, win32api #pylint: disable=import-error
import ctypes
from ctypes import c_int
import ctypes.wintypes
from ctypes.wintypes import HWND, DWORD
from pynput import keyboard #pylint: disable=import-error
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


monitors = win32api.EnumDisplayMonitors()
d = desktop(monitors)

def getWindows():
    cntx = []
    win32gui.EnumWindows( winEnumHandler, cntx )
    return cntx

def focusL():
    d.moveFocusDirection(win32gui.GetForegroundWindow(), 'L')
def focusR():
    d.moveFocusDirection(win32gui.GetForegroundWindow(), 'R')
def focusU():
    d.moveFocusDirection(win32gui.GetForegroundWindow(), 'U')
def focusD():
    d.moveFocusDirection(win32gui.GetForegroundWindow(), 'D')

def moveU():
    d.moveWindowDirection(win32gui.GetForegroundWindow(), 'U')
def moveD():
    d.moveWindowDirection(win32gui.GetForegroundWindow(), 'D')
def moveL():
    d.moveWindowDirection(win32gui.GetForegroundWindow(), 'L')
def moveR():
    d.moveWindowDirection(win32gui.GetForegroundWindow(), 'R')

def ws0():
    d.switchWorkspace(0)
def ws1():
    d.switchWorkspace(1)
def ws2():
    d.switchWorkspace(2)
def ws3():
    d.switchWorkspace(3)
def ws4():
    d.switchWorkspace(4)

def draw():
    d.drawWorkspaceTag()

def quit():
    h.stop()

for hwnd in getWindows():
    d.addNewWindow(hwnd)

h = keyboard.GlobalHotKeys({
    '<alt>+<shift>+j':moveD,
    '<alt>+<shift>+l':moveR,
    '<alt>+<shift>+k':moveU,
    '<alt>+<shift>+h':moveL,

    '<alt>+j': focusD,
    '<alt>+h': focusL,
    '<alt>+l': focusR,
    '<alt>+k': focusU,

    '<alt>+0': ws0,
    '<alt>+1': ws1,
    '<alt>+2': ws2,
    '<alt>+3': ws3,
    '<alt>+4': ws4,
    '<alt>+-': draw,
    '<alt>+q': quit,
})
h.start()
h.join()
