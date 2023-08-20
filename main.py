from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, DirectionalLight

loadPrcFile("settings.prc")


class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        grassBlock = loader.loadModel("grass-block.glb")
        grassBlock.reparentTo(render)
        mainLight = DirectionalLight("main light")
        mainLightNodePath = render.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)
        render.setLight(mainLightNodePath)


game = MyGame()
game.run()
