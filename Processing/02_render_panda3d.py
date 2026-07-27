from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import GeomVertexArrayFormat, GeomVertexData, GeomVertexFormat, Geom, GeomNode
from panda3d.core import GeomVertexReader, GeomVertexWriter, GeomPoints

# import panda3d_loading_processing as plp
# from panda_processing_3d import panda3d_loading_processing as plp
from math import pi, sin, cos

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # load the environment model
        self.scene = self.loader.loadModel('bvw-f2004--streetscene/street-scene.egg')

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        #Apply scale and position transforms on the model
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), - 20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0 , 0)
        return Task.cont

app = MyApp()
app.run()

class Dream_app(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        nodepath = self.geom_node()


    def geom_node(self):
        # array = GeomVertexArrayFormat()
        # array.add_column("vertex", 3, Geom.NT_float32, Geom.C_point)
        # array.add_column("color", 3, Geom.NT_float32, Geom.C_color)

        # Create a VertexFormat to hold the arrays
        format = GeomVertexFormat.get_v3c4()
        # format.addArray(array)

        # register the Vertexformat to build up the internal tables to rendering it.
        # for adding or removing a new array must be created
        format = GeomVertexFormat.register_format(format)

        verx, colr = plp.loading_datasource_open3d()

        vdata = GeomVertexData("forest", format, Geom.UH_static)
        vdata.set_num_rows(len(verx))
        vertex = GeomVertexWriter(vdata, 'vertex')
        color  = GeomVertexWriter(vdata, 'color')

        
        for i in range(len(verx)):
            vertex.add_data3f(verx[i])
            color.add_data3f(colr[i])

        prim = GeomPoints(Geom.UH_static)
        prim.add_next_vertices(len(verx))

        geom = Geom(vdata)
        geom.add_Primitive(prim)

        node = GeomNode('forest')
        node.add_Geom(geom)

        nodepath = render.attachNewNode(node)
 
        forest = GeomPoints()


    # Design a method that obtain the vertex of image using the 




# app_dream = Dream_app()
# app_dream.run()

