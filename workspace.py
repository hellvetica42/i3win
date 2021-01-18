import win32gui
from utils import *
from window import window
from math import floor

class workspace():

    def __init__(self, **resolution):
        self.width = resolution['width']
        self.height = resolution['height']
        self.slots: slot = []
        #Object to hold slot->window connection
        self.assingment = SlotWindow()

        self.slots.append(slot(margin(0, O.H), 
                                margin(self.width, O.H),

                                margin(0, O.V),
                                margin(self.height, O.V)))

    def getLargestSlot(self) -> slot:
        m = lambda s: s.getSlotArea() 
        return max(self.slots, key=m)


    def getEmptySlot(self) -> slot:
        #Ako nije dodana nekom prozoru
        for s in self.slots:
            if not self.assingment.exists(s):
                return s

        return None

    def addWindow(self, w: window):
        s = self.assingment.getSlot(w)
        #If windows is allready added to slot
        if s is not None:
            print("Window Exists")
            w.updateWindow(s)
            w.focus()
            return

        #If there is a vacant slot
        if len(self.slots) > self.assingment.length():
            print("Assigning to empty slot")
            s = self.getEmptySlot()
            if s is not None:
                self.assingment.addPair(s, w)
            else:
                assert len(self.slots) == self.assingment.length() 

        #If there are no vacant slots, create new one
        elif len(self.slots) == self.assingment.length():
            print("Creating new slot")
            s = self.newSlot()
            self.assingment.addPair(s, w)
            print(s)

        print(win32gui.GetWindowText(w.id))

        w.updateWindow(s)
        w.focus()

    def newSlot(self):

        oldSlot = self.getLargestSlot()
        if oldSlot.getSlotHeight() > oldSlot.getSlotWidth():
            return self.splitVertical(oldSlot)
        else:
            return self.splitHorizontal(oldSlot)


    def splitHorizontal(self, s: slot) -> slot:
        newMargin = margin(floor((s.rightMargin.value-s.leftMargin.value)/2)+s.leftMargin.value, s.rightMargin.type)
        
        #new and old margin for left/right
        newSlot = slot(leftMargin=newMargin,
                        rightMargin=s.rightMargin,
                        #Stays the same
                        topMargin=s.topMargin,
                        botMargin=s.botMargin)

        self.slots.append(newSlot)

        #Halves the width of existing slot
        s.setMargins(rightMargin=newMargin)

        #Refresh window of chosen slot
        self.assingment.getWin(s).updateWindow(s)

        return newSlot

    def splitVertical(self, s: slot) -> slot:
        newMargin = margin(floor(s.botMargin.value/2), s.botMargin.type)
        
        #Stays the same
        newSlot = slot(leftMargin=s.leftMargin,
                        rightMargin=s.rightMargin,
                        #new and old margin for bot/top
                        topMargin=newMargin,
                        botMargin=s.botMargin)

        self.slots.append(newSlot)

        #Halves the height of existing slot
        s.setMargins(botMargin=newMargin)

        #Refresh window of chosen slot
        self.assingment.getWin(s).updateWindow(s)

        return newSlot

    def updateAll(self):
        for p in self.assingment.pairs:
            p[1].updateWindow(p[0])

    def updateWindows(self, win1, win2):
        for p in self.assingment.pairs:
            if p[1] == win1 or p[1] == win2:
                p[1].updateWindow(p[0])
        pass


    def swapSlots(self, slot1, slot2):
        w1 = self.assingment.getWin(slot1)
        w2 = self.assingment.getWin(slot2)
        self.assingment.swapSlots(slot1, slot2)
        self.updateWindows(w1, w2)

    def moveSlotLeft(self, s: slot):
        #Looking for slots whose right margin is the selected slot's leftMargin
        target = self.getSlotByAproxPosition(s, 'L')
        if target is None:
            print("Cant move")
        else:
            self.swapSlots(s, target)

    def moveSlotRight(self, s: slot):
        #Looking for slots whose right margin is the selected slot's leftMargin
        target = self.getSlotByAproxPosition(s, 'R')
        if target is None:
            print("Cant move")
        else:
            self.swapSlots(s, target)

    def moveSlotUp(self, s: slot):
        #Looking for slots whose bot margin is the selected slot's topMargin
        target = self.getSlotByAproxPosition(s, 'T')
        if target is None:
            print("Cant move")
        else:
            self.swapSlots(s, target)

    def moveSlotDown(self, s: slot):
        #Looking for slots whose top margin is the selected slot's botMargin
        target = self.getSlotByAproxPosition(s, 'B')
        if target is None:
            print("Cant move")
        else:
            self.swapSlots(s, target)

    def moveFocus(self, hwdn, direction):
        source = self.assingment.getSlotByWindowId(hwdn)

        target = self.getSlotByAproxPosition(source, direction)

        if target is None:
            print("Cant move there")
            return

        win = self.assingment.getWin(target)

        # print(win32gui.GetWindowText(win.id))

        win.focus()


    def getSlotByAproxPosition(self, slot: slot, direction):
        candidates = []
        if direction == 'L':
            candidates = self.assingment.getSlotsByMargin(slot.leftMargin, 'R')
        if direction == 'R':
            candidates = self.assingment.getSlotsByMargin(slot.rightMargin, 'L')
        if direction == 'T':
            candidates = self.assingment.getSlotsByMargin(slot.topMargin, 'B')
        if direction == 'B':
            candidates = self.assingment.getSlotsByMargin(slot.botMargin, 'T')

        if len(candidates) == 0:
            return None

        if direction == 'L' or direction == 'R':

            topVal = slot.topMargin.value

            def diff(s: slot):
                return abs(topVal-s.topMargin.value)
            #Values of differences of top margins 
            val = list(map(diff, candidates))

            winner = candidates[val.index(min(val))]

        else:
            leftVal = slot.leftMargin.value

            def diff(s: slot):
                return abs(leftVal-s.leftMargin.value)
            #Values of differences of top margins 
            val = list(map(diff, candidates))

            winner = candidates[val.index(min(val))]

        # print(win32gui.GetWindowText(self.assingment.getWin(winner).id))
        print("AproxPosition is slot", winner)

        return winner



    def __str__(self) -> str:
        return str(self.slots)
    
    __repr__ = __str__

