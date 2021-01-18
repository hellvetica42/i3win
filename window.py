import win32gui, win32con

class window():
    def __init__(self, id):
        self.id = id

    def updateWindow(self, slot):
        w = slot.rightMargin.value - slot.leftMargin.value
        h = slot.botMargin.value - slot.topMargin.value

        win32gui.ShowWindow(self.id, win32con.SW_NORMAL)
        win32gui.MoveWindow(self.id, slot.leftMargin.value, slot.topMargin.value, w, h, True)

        rect = win32gui.GetWindowRect(self.id)

        if any([rect[0] != slot.leftMargin.value, rect[1] != slot.topMargin.value, rect[2]-rect[0] != w, rect[3]-rect[1] != h]):
            print("Window", win32gui.GetWindowText(self.id), "cannot be smaller")

    def resizeWindow(self, w, h):
        self.w, self.h = w, h

        win32gui.MoveWindow(self.id, self.x, self.y, self.w, self.h, True)

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
