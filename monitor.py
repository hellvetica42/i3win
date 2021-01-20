
from workspace import workspace

from workspace import workspace

class monitor():
    def __init__(self, shape, id) -> None:
        self.shape = shape
        self.workspaces: workspace = []
        self.id = id
        self.relativeMonitorcoordinates = (-300, -30)

        self.workspaces.append(workspace(len(self.workspaces), self.shape[0], self.shape[1], width=self.shape[2]-self.shape[0], height=self.shape[3]-self.shape[1] - 40))

        self.activeWorkspace: workspace = self.workspaces[0]

    def addNewWorkspace(self):
        shape = self.shape
        wsId = len(self.workspaces)

        self.workspaces.append(workspace(wsId, shape[0], shape[1], width=shape[2]-shape[0], height=shape[3]-shape[1] - 40))

    def containsWindow(self, id):
        if any([w.containsWindow(id) for w in self.workspaces]):
            return True

        return False

    def addWindow(self, id):
        self.activeWorkspace.addNewWindow(id)

    def focus(self):
        self.activeWorkspace.focus()