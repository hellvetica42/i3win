import win32gui
from i3utils import margin 
from slot import slot 
from math import floor

class panel():
    def __init__(self, height, monitorYValue, leftMargin: margin, rightMargin:margin):
        self.monitorYValue = monitorYValue 
        self.height = height
        self.leftMargin = leftMargin
        self.rightMargin = rightMargin
        self.slots: slot = []

    def addNewWindow(self, id):
        newSlot = slot(id, margin(value=0), margin(value=0)) 
        self.slots.append(newSlot)

        self.updateLayout()

        newSlot.focus()

    def updateLayout(self):
        slotHeight = floor(self.height / len(self.slots))

        margins = []
        for i in range(len(self.slots)+1):
            margins.append(margin((i*slotHeight)+self.monitorYValue))

        for s, i in zip(self.slots, range(len(self.slots))):
            s.setMargins(margins[i], margins[i+1])
            s.updateWindow(self.leftMargin, self.rightMargin)

    def getSurface(self):
        return self.height * (self.rightMargin.value - self.leftMargin.value)

    def getWidth(self):
        return self.rightMargin.value - self.leftMargin.value

    def setMargins(self, leftMargin: margin, rightMargin: margin):
        self.leftMargin = leftMargin
        self.rightMargin = rightMargin

    def update(self):
        for s in self.slots:
            s.updateWindow(self.leftMargin, self.rightMargin)
    
    def getSlotWithWindow(self, id):
        for s in self.slots:
            if s.id == id:
                return s
        return None
    
    def swapSlots(self, s1, s2):
        m1, m2 = s1.topMargin, s1.botMargin
        s1.topMargin, s1.botMargin = s2.topMargin, s2.botMargin
        s2.topMargin, s2.botMargin = m1, m2

    def moveSlot(self, source: slot, direction):
        if direction == 'U':
            target = self.getSlotByMargin(source.topMargin, 'D')
            pass
        elif direction == 'D':
            target = self.getSlotByMargin(source.botMargin, 'U')
            pass
        else:
            print("Unhandled direction")
            return

        if target is None:
            print("No target slot, can't move")
            return

        self.swapSlots(source, target)
        source.updateWindow(self.leftMargin, self.rightMargin)
        target.updateWindow(self.leftMargin, self.rightMargin)

    def removeSlot(self, s: slot):
        self.slots.remove(s)
        if len(self.slots) == 0:
            return True
        self.updateLayout()
        return False

    def addSlot(self, s: slot):
        self.slots.append(s)
        self.updateLayout()

    def getSlotWithClosestTopMargin(self, m: margin):
        def diff(s: slot):
            return abs(m.value - s.topMargin.value)

        diffs = list(map(diff, self.slots))

        return self.slots[diffs.index(min(diffs))]

    def getSlotByMargin(self, m: margin, direction):
        for s in self.slots:
            if direction == 'U':
                if s.topMargin == m:
                    return s
            elif direction == 'D':
                if s.botMargin == m:
                    return s

        return None

    def containsWindow(self, id) -> bool:
        if id in [s.id for s in self.slots]:
            return True
        return False

    def __str__(self) -> str:
        return "L: " + str(self.leftMargin.value) + " R: " + str(self.rightMargin.value)
