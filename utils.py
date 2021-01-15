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

    def __str__(self) -> str:
        return 'L: {} R: {} T:{} B:{} \n'.format(self.leftMargin.value, self.rightMargin.value, self.topMargin.value, self.botMargin.value)

    __repr__ = __str__
