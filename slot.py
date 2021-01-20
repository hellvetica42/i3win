import win32gui, win32con
from i3utils import margin #type:ignore
from math import floor


class slot():
    def __init__(self, id, topMargin: margin, botMargin: margin) -> None:
        self.id = id
        self.topMargin = topMargin
        self.botMargin = botMargin

    def setMargins(self, topMargin: margin, botMargin: margin):
        self.topMargin = topMargin
        self.botMargin = botMargin

    def updateWindow(self, leftMargin: margin, rightMargin: margin):
        w = rightMargin.value - leftMargin.value
        h = self.botMargin.value - self.topMargin.value

        win32gui.ShowWindow(self.id, win32con.SW_NORMAL)
        win32gui.MoveWindow(self.id, leftMargin.value, self.topMargin.value, w, h, True)

        rect = win32gui.GetWindowRect(self.id)

        if any([rect[0] != leftMargin.value, rect[1] != self.topMargin.value, rect[2]-rect[0] != w, rect[3]-rect[1] != h]):
            print("Window", win32gui.GetWindowText(self.id), "cannot be smaller")

    def focus(self):
        try:
            if win32gui.IsIconic(self.id):
                win32gui.ShowWindow(self.id, win32con.SW_RESTORE)
                print("IsIconic")
            win32gui.SetForegroundWindow(self.id)
        except Exception as e:
            print("Error focusing")
            print(str(e))

    def __eq__(self, o) -> bool:
        return self.id == o.id
    
    def __str__(self) -> str:
        return win32gui.GetWindowText(self.id)