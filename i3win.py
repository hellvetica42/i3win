from workspace import workspace 
from desktop import desktop
import win32gui, win32com.client, win32api #pylint: disable=import-error
import ctypes
from ctypes import c_int
import ctypes.wintypes
from ctypes.wintypes import HWND, DWORD
from pynput import keyboard #pylint: disable=import-error
import time
import threading
import sys
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
def ws5():
    d.switchWorkspace(5)
def ws6():
    d.switchWorkspace(6)
def ws7():
    d.switchWorkspace(7)
def ws8():
    d.switchWorkspace(8)
def ws9():
    d.switchWorkspace(9)

def sendToWs0():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 0)
def sendToWs1():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 1)
def sendToWs2():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 2)
def sendToWs3():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 3)
def sendToWs4():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 4)
def sendToWs5():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 5)
def sendToWs6():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 6)
def sendToWs7():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 7)
def sendToWs8():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 8)
def sendToWs9():
    d.sendToWorkspace(win32gui.GetForegroundWindow(), 9)


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

    '<alt>+<shift>+0': sendToWs0,
    '<alt>+<shift>+1': sendToWs1,
    '<alt>+<shift>+2': sendToWs2,
    '<alt>+<shift>+3': sendToWs3,
    '<alt>+<shift>+4': sendToWs4,
    '<alt>+<shift>+5': sendToWs5,
    '<alt>+<shift>+6': sendToWs6,
    '<alt>+<shift>+7': sendToWs7,
    '<alt>+<shift>+8': sendToWs8,
    '<alt>+<shift>+9': sendToWs9,

    '<alt>+j': focusD,
    '<alt>+h': focusL,
    '<alt>+l': focusR,
    '<alt>+k': focusU,

    '<alt>+0': ws0,
    '<alt>+1': ws1,
    '<alt>+2': ws2,
    '<alt>+3': ws3,
    '<alt>+4': ws4,
    '<alt>+5': ws5,
    '<alt>+6': ws6,
    '<alt>+7': ws7,
    '<alt>+8': ws8,
    '<alt>+9': ws9,


    '<alt>+-': draw,
    '<alt>+q': quit,
})
h.start()
h.join()
