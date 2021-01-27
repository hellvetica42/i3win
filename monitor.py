
from workspace import workspace

from workspace import workspace

class monitor():
    def __init__(self, shape, id, wsId) -> None:
        self.shape = shape
        self.workspaces: workspace = []
        self.id = id
        self.relativeMonitorcoordinates = (-300, -30)

        self.workspaces.append(workspace(wsId, self.shape[0], self.shape[1], 
                                         width=self.shape[2]-self.shape[0], height=self.shape[3]-self.shape[1] - 40))

        self.activeWorkspace: workspace = self.workspaces[0]

    def addNewWorkspace(self, id):
        shape = self.shape

        newWs = workspace(id, shape[0], shape[1], width=shape[2]-shape[0], height=shape[3]-shape[1] - 40)

        self.workspaces.append(newWs)
        return newWs

    def containsWindow(self, id):
        if any([w.containsWindow(id) for w in self.workspaces]):
            return True

        return False

    def containsWorkspace(self, id):
        if id in [w.id for w in self.workspaces]:
            return True
        return False

    def showWorkspace(self, id):
        if self.activeWorkspace.id == id:
            self.activeWorkspace.focus()
            return
        target = None
        for w in self.workspaces:
            if w.id == id:
                target = w
                break

        if target is None:
            print("No such workspace. TODO Create new")
            return
        
        self.activeWorkspace.hide()
        self.activeWorkspace = target
        self.activeWorkspace.show()

    def addWindow(self, id):
        self.activeWorkspace.addNewWindow(id)

    def focus(self):
        self.activeWorkspace.focus()
