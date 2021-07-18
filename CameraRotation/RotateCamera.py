## Camera Rotation Resource:          https://stackoverflow.com/questions/56609044/how-create-a-camera-on-pyopengl-that-can-do-perspective-rotations-on-mouse-mov

## How Game Rotation Axis Works?:     https://math.stackexchange.com/questions/3171374/3d-axis-rotation-new-value

## First Publicated here:             https://discourse.panda3d.org/t/rotate-camera-based-on-mouse-position/1237/16

import sys, os
import ctypes
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase, Loader
from direct.task import Task

class CameraRotation3D(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.RelativPath	  = Filename.fromOsSpecific(os.path.abspath(sys.path[0])).getFullpath()
        self.props             = base.win.getProperties()
        self.WindowProps	  = WindowProperties()
        self.GetLocalPID       = os.getpid()
        self.SceneMap          = self.loader.loadModel("models/environment")
        self.CameraJoint       = self.loader.loadModel(self.RelativPath + "/CameraJoint.egg")

        self.CameraFOV         = 70
        self.RotationSpeed     = 0.5
        self.MouseMove         = [0, 0]
        self.MouseX            = 0
        self.MouseY            = 0

        self.WindowProps.setCursorHidden(True)
        base.win.requestProperties(self.WindowProps)
        base.disableMouse()

        self.SceneMap.setScale(0.25, 0.25, 0.25)
        self.SceneMap.setPos(-8, 42, 0)
        self.SceneMap.reparentTo(self.render)

        self.CameraJoint.setScale(0.25, 0.25, 0.25)
        self.CameraJoint.setPos(0, 0, 5)
        self.CameraJoint.reparentTo(self.render)
        self.camera.reparentTo(self.CameraJoint)

        base.camLens.setFov(self.CameraFOV)
        base.setBackgroundColor(0, 0, 0)

        self.taskMgr.add(self.FallowCursor, "FallowRotation")

    def WindowProp(self, task):
        self.WindowProps.setCursorHidden(True)
        base.win.requestProperties(self.WindowProps)
        return Task.done

    def FallowCursor(self, task):
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        lpdw_process_id = ctypes.c_ulong()
        result = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw_process_id))
        process_id = lpdw_process_id.value
        if base.mouseWatcherNode.hasMouse():
            self.Cursor2D_X = base.mouseWatcherNode.getMouseX()             ## Mouse X position
            self.Cursor2D_Y = base.mouseWatcherNode.getMouseY()             ## Mouse Y position

        if process_id == self.GetLocalPID:
            self.taskMgr.add(self.WindowProp, "BackToGame")                 ## Return hidden cursor
            try:
                base.win.movePointer(0, self.props.getXSize() // 2, self.props.getYSize() // 2)         ## Center cursor
                self.MouseMove = [int(self.Cursor2D_X*100), int(self.Cursor2D_Y*100)]                   ## Amplificate movement
            except:
                pass
            self.MouseX    += self.MouseMove[0] * self.RotationSpeed                                    ## Smooth roll rotation
            self.MouseY    += self.MouseMove[1] * self.RotationSpeed                                    ## Smooth pitch rotation
            if self.MouseY > 90: self.MouseY = 90
            elif self.MouseY < -90: self.MouseY = -90
        else:
            self.WindowProps.setCursorHidden(False)
            base.win.requestProperties(self.WindowProps)
        self.CameraJoint.setHpr(-self.MouseX, self.MouseY, 0)
        return Task.cont

CameraRotation3D().run()
