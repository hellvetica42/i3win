import win32gui
from panel import panel #type:ignore
from i3utils import margin #type:ignore
from math import floor

class workspace():
    def __init__(self, **resolution):
        self.width = resolution['width']
        self.height = resolution['height']
        self.panels: panel = []

    def addNewWindow(self, id):
        if self.containsWindow(id):
            print("Window already indexed")
            return
        #If first panel
        if len(self.panels) == 0:
            p = panel(self.height, margin(value=0), margin(value=self.width))
            p.addNewWindow(id)
            p.update()
            self.panels.append(p)
        else:
            target = self.getLargestPanel()

            if target.height/len(target.slots) > target.getWidth():
                #Split vertical #New slot 
                    target.addNewWindow(id)

            else:
                #Split horisontal #New panel 
                newPanel = self.addNewPanel()
                newPanel.addNewWindow(id)

            self.update()

    def update(self):
        for p in self.panels:
            p.update()

    def addNewPanel(self) -> panel:
        newPanel = panel(self.height, margin(value=0), margin(value=0))
        self.panels.append(newPanel)

        self.updateLayout()

        return newPanel

    def updateLayout(self):
        panelWidth = floor(self.width / len(self.panels))

        margins = []
        for i in range(len(self.panels) + 1):
            margins.append(margin(i*panelWidth))

        for i, p in enumerate(self.panels):
            p.setMargins(margins[i], margins[i+1])

        self.update()


    def getLargestPanel(self) -> panel:
        def diff(p: panel):
            return p.getSurface()/len(p.slots)

        sizes = list(map(diff, self.panels))

        largest = self.panels[sizes.index(max(sizes))]

        return largest

    def getPanelByMargin(self, m: margin, direction) -> panel:
        for p in self.panels:
            if direction == 'L':
                if p.leftMargin == m:
                    return p
                pass

            elif direction == 'R':
                if p.rightMargin == m:
                    return p
                pass
        return None

    def swapPanels(self, p1, p2):
        m1, m2 = p1.leftMargin, p1.rightMargin
        p1.leftMargin, p1.rightMargin = p2.leftMargin, p2.rightMargin
        p2.leftMargin, p2.rightMargin = m1, m2

    def containsWindow(self, id) -> bool:
        if any([p.containsWindow(id) for p in self.panels]):
            return True
        return False

    def getPanelWithWindow(self, id) -> panel:
        for p in self.panels:
            if p.containsWindow(id):
                return p
        return None

    def movePanel(self, source, direction):
        target = None
        if direction == 'L':
            target = self.getPanelByMargin(source.leftMargin, 'R')

        elif direction == 'R':
            target = self.getPanelByMargin(source.rightMargin, 'L')

        if target is None:
            print("Cant move panel there")
            return

        self.swapPanels(source, target)
        self.update()

    def moveFocus(self, id, direction):
        target = self.getSlotByAproxPosition(id, direction)
        if target is None:
            print("Cant move focus. No target slot")
        else:
            target.focus()

    def moveWindow(self, id, direction):
        sourcePanel = self.getPanelWithWindow(id)
        if sourcePanel is None:
            print("No such window")
            return

        sourceSlot = sourcePanel.getSlotWithWindow(id)

        if sourcePanel is None:
            print("No such window")
            return

        targetPanel = None
        #Within same panel #Only swaps
        if direction == 'U' or direction == 'D':
            sourcePanel.moveSlot(sourceSlot, direction)
            return

        #Between panels
        elif direction == 'L':
            targetPanel = self.getPanelByMargin(sourcePanel.leftMargin, 'R')
            pass
        elif direction == 'R':
            targetPanel = self.getPanelByMargin(sourcePanel.rightMargin, 'L')

        if targetPanel is None:
            print("Cant move there")
            return

        targetPanel.addSlot(sourceSlot)
        if sourcePanel.removeSlot(sourceSlot):
            self.panels.remove(sourcePanel)
            self.updateLayout()

    def getSlotByAproxPosition(self, id, direction):
        targetSlot = None
        sourcePanel = self.getPanelWithWindow(id)

        if sourcePanel is None:
            print("No such window")
            return

        sourceSlot = sourcePanel.getSlotWithWindow(id)

        #In other panel 
        if direction == 'L':
            targetPanel = self.getPanelByMargin(sourcePanel.leftMargin, 'R')
            if targetPanel is None:
                return None
            targetSlot = targetPanel.getSlotWithClosestTopMargin(sourceSlot.topMargin)

        elif direction == 'R':
            targetPanel = self.getPanelByMargin(sourcePanel.rightMargin, 'L')
            if targetPanel is None:
                return None
            targetSlot = targetPanel.getSlotWithClosestTopMargin(sourceSlot.topMargin)

        #Within panel
        elif direction == 'U':
            targetSlot = sourcePanel.getSlotByMargin(sourceSlot.topMargin, 'D')
            pass

        #Within panel
        elif direction == 'D':
            targetSlot = sourcePanel.getSlotByMargin(sourceSlot.botMargin, 'U')
            pass

        return targetSlot

