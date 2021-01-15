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
        self.assingment = []

        self.slots.append(slot(margin(0, O.H), 
                                margin(self.width, O.H),

                                margin(0, O.V),
                                margin(self.height, O.V)))

    def getLargestSlot(self) -> slot:
        m = lambda s: s.getSlotArea() 
        return max(self.slots, key=m)


    def getEmptySlot(self) -> slot:
        for s in self.slots:
            #Ako nije dodana nekom prozoru
            if s not in [a[0] for a in self.assingment]:
                return s

        return None

    def addWindow(self, w: window):
        for a in self.assingment:
            if w == a[1]:
                print("Window Exists")
                w.updateWindow(a[0])
                w.focus()
                return
        #Ako postoji prazan slot
        s = None
        if len(self.slots) > len(self.assingment):
            print("Assigning to empty slot")
            s = self.getEmptySlot()
            if s is not None:
                self.assingment.append([s, w])
            else:
                assert len(self.slots) == len(self.assingment)

        elif len(self.slots) == len(self.assingment):
            print("Creating new slot")
            s = self.newSlot()
            self.assingment.append([s, w])

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
        for a in self.assingment:
            if s is a[0]:
                a[1].updateWindow(s)

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
        for a in self.assingment:
            if s is a[0]:
                a[1].updateWindow(s)

        return newSlot

    def __str__(self) -> str:
        return str(self.slots)
    
    __repr__ = __str__

