import sys, os
import ctypes
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase, Loader
from direct.task import Task
from direct.gui.DirectGui import DirectFrame

class CameraRotation3D(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.RelativPath	   = Filename.fromOsSpecific(os.path.abspath(sys.path[0])).getFullpath()
        self.props             = base.win.getProperties()
        self.WindowProps	   = WindowProperties()
        self.GetLocalPID       = os.getpid()
        self.SceneMap          = self.loader.loadModel("models/environment")
        self.CameraJoint       = self.loader.loadModel(self.RelativPath + "/CameraJoint.egg")
        self.WallModel         = self.loader.loadModel(self.RelativPath + "/BasicWall.egg")
        self.Texture1          = self.loader.loadTexture(self.RelativPath + '/BrickTexture.jpg')
        self.ts                = TextureStage('ts')

        self.CameraFOV         = 70
        self.RotationSpeed     = 0.5
        self.MouseMove         = [0, 0]
        self.MouseX            = 0
        self.MouseY            = 0
        self.mouseWasDown      = False

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


        self.WallModel.setPos(0, 7, 5)
        self.WallModel.setScale(4, 0.25, 3)
        self.WallModel.reparentTo(self.render)
        self.WallModel.setTexture(self.ts, self.Texture1)             ## Set Texture 
        self.WallModel.setTexScale(self.ts, 3, 4)
        self.WallModel.setTexHpr(self.ts, 90, 0, 0)

        self.lines = LineSegs()
        self.lines.setColor(1, 0, 0, 1)
        self.lines.moveTo(1,1,1)
        self.lines.drawTo(3,3,3)
        self.lines.setThickness(4)
        node = self.lines.create()
        np = NodePath(node)
        np.reparentTo(self.render)

        self.picker = CollisionTraverser()
        self.picker.showCollisions(self.render)
        self.pq = CollisionHandlerQueue() 

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.WallModel.setCollideMask(BitMask32.bit(1)) 

        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pq)

        base.camLens.setFov(self.CameraFOV)
        base.setBackgroundColor(0, 0, 0)

        self.accept("mouse1", self.ShootSystem)
        self.accept('escape', sys.exit)

        self.taskMgr.add(self.FallowCursor, "FallowRotation")
        self.taskMgr.add(self.DrawCrossHair, "DrawOnScreen")

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
            self.Cursor2D_X = base.mouseWatcherNode.getMouseX()
            self.Cursor2D_Y = base.mouseWatcherNode.getMouseY()

        if process_id == self.GetLocalPID:
            self.taskMgr.add(self.WindowProp, "BackToGame")
            try:
                base.win.movePointer(0, self.props.getXSize() // 2, self.props.getYSize() // 2)
                self.MouseMove = [int(self.Cursor2D_X*100), int(self.Cursor2D_Y*100)]
            except:
                pass
            self.MouseX    += self.MouseMove[0] * self.RotationSpeed
            self.MouseY    += self.MouseMove[1] * self.RotationSpeed
            if self.MouseY > 90: self.MouseY = 90
            elif self.MouseY < -90: self.MouseY = -90
        else:
            self.WindowProps.setCursorHidden(False)
            base.win.requestProperties(self.WindowProps)
        self.CameraJoint.setHpr(-self.MouseX, self.MouseY, 0)
        return Task.cont

    def ShootSystem(self):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            self.picker.traverse(self.render)
            if self.pq.getNumEntries() > 0:
                self.pq.sortEntries()
                pickedObj = self.pq.getEntry(0).getIntoNodePath()
                print('click on ' + pickedObj.getName())
            else:
                print('mouse click')

    def DrawCrossHair(self, task):
        DirectFrame(frameColor=(0, 1, 0, 1),                ## Up
                    frameSize=(0.025, 0.05, 0.025, 0.15),
                    pos=(-0.02, 0, -0.02))
        DirectFrame(frameColor=(0, 1, 0, 1),                ## Down
                    frameSize=(0.025, 0.05, 0.025, 0.15),
                    pos=(-0.02, 0, -0.2))

        DirectFrame(frameColor=(0, 1, 0, 1),               ## Left         
                    frameSize=(0.025, 0.15, 0.025, 0.05),
                    pos=(-0.16, 0, -0.06))
        DirectFrame(frameColor=(0, 1, 0, 1),               ## Right
                    frameSize=(0.025, 0.15, 0.025, 0.05),
                    pos=(0.02, 0, -0.06))

CameraRotation3D().run()