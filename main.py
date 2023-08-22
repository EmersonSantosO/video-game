from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, DirectionalLight, AmbientLight, TransparencyAttrib, WindowProperties, CollisionTraverser, CollisionNode, CollisionBox, CollisionTraverse, CollisionHandlerQueue
from direct.gui.OnscreenImage import OnscreenImage
from math import pi, sin, cos
loadPrcFile("settings.prc")


def degToRad(degrees):
    return degrees * (pi / 180.0)


class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()
        self.setupSkybox()
        self.captureMouse()
        self.setupControls()
        taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()
        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        camera.setPos(
            camera.getX() + x_movement,
            camera.getY() + y_movement,
            camera.getZ() + z_movement,
        )
        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangey = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangey *
                    dt * self.cameraSwingFactor)), 0
            )
            self.lastMouseX = mouseX
            self.lastMouseY = mouseY
        return task.cont

    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.accept("escape", self.relaseMouse)
        self.accept("mouse", self.captureMouse)
        self.accept("w", self.updateKeyMap, ["forward", True])
        self.accept("w-up", self.updateKeyMap, ["forward", False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])

        self.accept('1', self.setSelectedBlockType, ['grass'])
        self.accept('2', self.setSelectedBlockType, ['dirt'])
        self.accept('3', self.setSelectedBlockType, ['sand'])
        self.accept('4', self.setSelectedBlockType, ['stone'])

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def captureMouse(self):

        self.cameraSwingActivated = True
        md = self.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(properties)

    def relaseMouse(self):
        self.cameraSwingActivated = False
        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, -3, 0)

        crosshairs = OnscreenImage(
            image="crosshairs.png",
            pos=(0, 0, 0),
            scale=0.05
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

    def setupSkybox(self):
        skybox = loader.loadModel("skybox/skybox.egg")
        skybox.setScale(500)
        skybox.setBin("background", 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(render)

    def generateTerrain(self):
        for z in range(10):
            for y in range(20):
                for x in range(20):
                    newBlockNode = render.attachNewNode(
                        "nex-block-placeholder")

                    newBlockNode.setPos(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2
                    )
                    if z == 0:
                        self.grassBlock.instanceTo(newBlockNode)
                    else:
                        self.dirtBlock.instanceTo(newBlockNode)

    def loadModels(self):
        self.grassBlock = loader.loadModel("grass-block.glb")
        self.grassBlock.reparentTo(render)

        self.dirtBlock = loader.loadModel("dirt-block.glb")
        self.dirtBlock.setPos(0, 2, 0)
        self.dirtBlock.reparentTo(render)

        self.stoneBlock = loader.loadModel("stone-block.glb")
        self.stoneBlock.setPos(0, -2, 0)
        self.stoneBlock.reparentTo(render)

        self.sandBlock = loader.loadModel("sand-block.glb")
        self.sandBlock.setPos(0, 4, 0)
        self.sandBlock.reparentTo(render)

    def setupLights(self):
        mainLight = DirectionalLight("main light")
        mainLightNodePath = render.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)
        render.setLight(mainLightNodePath)

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor((0.3, 0.3, 0.3, 1))
        ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNodePath)


game = MyGame()
game.run()
