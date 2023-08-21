from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, DirectionalLight, AmbientLight, TransparencyAttrib
from direct.gui.OnscreenImage import OnscreenImage

loadPrcFile("settings.prc")


class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.loadModels()
        self.setupLights()
        self.generateTerrain()
        self.setupCamera()

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, -3, 0)

        crosshairs = OnscreenImage(
            image="crosshairs.png",
            pos=(0, 0, 0),
            scale=0.05
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

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
