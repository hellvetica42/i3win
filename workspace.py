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

        w.updateWindow(s)
        w.focus()

    def newSlot(self):

        oldSlot = self.getLargestSlot()
        if oldSlot.getSlotHeight() > oldSlot.getSlotWidth():
            return self.splitVertical(oldSlot)
        else:
            return self.splitHorizontal(oldSlot)


    def splitHorizontal(self, s: slot) -> slot:
        newMargin = margin(floor(s.rightMargin.value/2), s.rightMargin.type)
        
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

    def swapSlots(self, slot1, slot2):
        self.assingment.swapSlots(slot1, slot2)
        self.updateAll()

    def moveSlotLeft(self, s: slot):
        #Looking for slots whose right margin is the selected slot's leftMargin
        candidates = self.assingment.getSlotsByMargin(s.leftMargin, 'R')
        if len(candidates) == 0:
            print("Cant move")
        else:
            self.swapSlots(s, candidates[0])

    def moveSlotRight(self, s: slot):
        #Looking for slots whose left margin is the selected slot's rightMargin
        candidates = self.assingment.getSlotsByMargin(s.rightMargin, 'L')
        if len(candidates) == 0:
            print("Cant move")
        else:
            self.swapSlots(s, candidates[0])

    def moveSlotUp(self, s: slot):
        #Looking for slots whose bot margin is the selected slot's topMargin
        candidates = self.assingment.getSlotsByMargin(s.topMargin, 'B')
        if len(candidates) == 0:
            print("Cant move")
        else:
            self.swapSlots(s, candidates[0])

    def moveSlotDown(self, s: slot):
        #Looking for slots whose top margin is the selected slot's botMargin
        candidates = self.assingment.getSlotsByMargin(s.botMargin, 'T')
        if len(candidates) == 0:
            print("Cant move")
        else:
            self.swapSlots(s, candidates[0])


    def __str__(self) -> str:
        return str(self.slots)
    
    __repr__ = __str__

