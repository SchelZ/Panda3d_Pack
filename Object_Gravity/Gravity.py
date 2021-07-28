import sys, os
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase, Loader
from direct.task import Task

class Ball_Gravity(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.RelativPath	   = Filename.fromOsSpecific(os.path.abspath(sys.path[0])).getFullpath()
        base.disableMouse()

        self.CameraJoint         = self.loader.loadModel(self.RelativPath + "/Sphere.egg")
        self.Character           = self.loader.loadModel(self.RelativPath + "/Sphere.egg")

        self.CameraFOV           = 70
        self.jump_speed          = 0
        self.gravity_force       = 9.8
        self.jump_status         = False

        self.CameraJoint.setPos(0, -10, 2)
        self.CameraJoint.reparentTo(self.render)
        self.camera.reparentTo(self.CameraJoint)
        self.Character.reparentTo(self.render)

        base.camLens.setFov(self.CameraFOV)

        self.accept("space", self.set_jump)
        self.taskMgr.add(self.gravity, "gravity")


    def set_jump(self):
        if self.jump_status == False:
            self.jump_speed = 4
            self.jump_status = True

    def gravity(self, task):
        self.Character.setZ(self.Character.getZ()+self.jump_speed*globalClock.getDt())
        if self.Character.getZ() > 0:
            self.jump_speed = self.jump_speed - self.gravity_force*globalClock.getDt()
        if self.Character.getZ() < 0:
            self.Character.setZ(0)
            self.jump_speed = 0
            self.jump_status = False
        return task.cont

Ball_Gravity().run()