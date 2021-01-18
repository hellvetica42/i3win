import win32gui, win32con

class window():
    def __init__(self, id):
        self.id = id

    def updateWindow(self, slot):
        w = slot.rightMargin.value - slot.leftMargin.value
        h = slot.botMargin.value - slot.topMargin.value

        win32gui.ShowWindow(self.id, win32con.SW_NORMAL)
        win32gui.MoveWindow(self.id, slot.leftMargin.value, slot.topMargin.value, w, h, True)

    def resizeWindow(self, w, h):
        self.w, self.h = w, h

        win32gui.MoveWindow(self.id, self.x, self.y, self.w, self.h, True)

    def focus(self):
        try:
            if win32gui.IsIconic(self.id):
                win32gui.ShowWindow(self.id, win32con.SW_RESTORE)
                print("IsIconic")
            win32gui.SetForegroundWindow(self.id)
        except:
            print("Access?")

    def __eq__(self, o) -> bool:
        return self.id == o.id
