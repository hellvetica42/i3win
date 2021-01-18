from dataclasses import dataclass
from window import window
from enum import Enum

#O as in orientation
class O(Enum): #Vertical Horisontal
    V = 0,
    H = 1

@dataclass
class margin():
    value: int
    type: O

class slot():
    def __init__(self, leftMargin: margin, rightMargin: margin, topMargin: margin, botMargin: margin):
        self.leftMargin = leftMargin
        self.rightMargin = rightMargin
        self.topMargin = topMargin
        self.botMargin = botMargin

    def setMargins(self, **margins):
        if 'leftMargin' in margins:
            self.leftMargin = margins['leftMargin']
        if 'rightMargin' in margins:
            self.rightMargin = margins['rightMargin']
        if 'topMargin' in margins:
            self.topMargin = margins['topMargin']
        if 'botMargin' in margins:
            self.botMargin = margins['botMargin']

    def getSlotArea(self):
        return (self.rightMargin.value - self.leftMargin.value) * (self.botMargin.value - self.topMargin.value)

    def getSlotHeight(self):
        return self.botMargin.value - self.topMargin.value

    def getSlotWidth(self):
        return self.rightMargin.value - self.leftMargin.value

    def getMarginValuesAsTouple(self):
        return (self.leftMargin.value, self.topMargin.value, self.rightMargin.value, self.botMargin.value)

    def __str__(self) -> str:
        return 'L: {} R: {} T:{} B:{} \n'.format(self.leftMargin.value, self.rightMargin.value, self.topMargin.value, self.botMargin.value)

    __repr__ = __str__

class SlotWindow():
    def __init__(self) -> None:
        self.pairs = []
        pass

    def addPair(self, slot, window):
        self.pairs.append([slot, window])

    def getSlot(self, w: window):
        for p in self.pairs:
            if p[1] == w:
                return p[0]

        return None

    def getWin(self, s: slot):
        for p in self.pairs:
            if p[0] == s:
                return p[1]

        return None

    def exists(self, a):
        for p in self.pairs:
            if a in p:
                return True

        return False

    def swapSlots(self, s1, s2):
        i1 = -1
        i2 = -1
        for i in range(len(self.pairs)):
            if self.pairs[i][0] == s1:
                i1 = i
            if self.pairs[i][0] == s2:
                i2 = i

        self.pairs[i1][0], self.pairs[i2][0] = self.pairs[i2][0], self.pairs[i1][0]

    def getSlotsByMargin(self, margin, direction: str):
        slots = []
        for p in self.pairs:
            if direction == 'T':
                if p[0].topMargin == margin:
                    slots.append(p[0])
            elif direction == 'B':
                if p[0].botMargin == margin:
                    slots.append(p[0])
            elif direction == 'L':
                if p[0].leftMargin == margin:
                    slots.append(p[0])
            elif direction == 'R':
                if p[0].rightMargin == margin:
                    slots.append(p[0])

        return slots

    def getSlotByWindowId(self, id) -> slot:
        for p in self.pairs:
            if p[1].id == id:
                return p[0]

    def getWindowById(self, id) -> window:
        for p in self.pairs:
            if p[1].id == id:
                return p[1]

    def getSlotByAproxPosition(self, slot: slot, direction):
        candidates = []
        if direction == 'L':
            candidates = self.getSlotsByMargin(slot.leftMargin, 'R')


        topVal = slot.topMargin.value

        def diff(s: slot):
            return abs(topVal-s.topMargin.value)
        #Values of differences of top margins 
        val = list(map(diff, candidates))

        print(val)

        winner = candidates[val.index(min(val))]

        print(self.getWin(winner).id)
        


    def length(self):
        return len(self.pairs)



