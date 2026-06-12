from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import GeomVertexArrayFormat, GeomVertexData, GeomVertexFormat, Geom, GeomNode
from panda3d.core import GeomVertexReader, GeomVertexWriter, GeomPoints
from panda3d.core import RenderModeAttrib

import panda_loading_3d as plp

from math import pi, sin, cos


class Dream_app(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.nodepath = self.geom_node()
 
        # 2. Força os pontos a terem 5 pixels de tamanho (deixará a floresta visível e densa)
        self.nodepath.set_attrib(RenderModeAttrib.make(RenderModeAttrib.M_point, 3))
        
        # 3. Dá um "zoom" gigante de 500 vezes para compensar os números pequenos do MiDaS
        self.nodepath.set_scale(500, 500, 500)
        
        # 4. Afasta a floresta 10 metros para a frente e desce ela 2 metros para alinhar com a câmera
        self.nodepath.set_pos(0, 10, -2)
        self.nodepath.setHpr(0,180,0)

    def geom_node(self):
        # Create a VertexFormat to hold the arrays
        format = GeomVertexFormat.get_v3c4()
        # format.addArray(array)

        # register the Vertexformat to build up the internal tables to rendering it.
        # for adding or removing a new array must be created
        format = GeomVertexFormat.register_format(format)

        verx, colr = plp.loading_datasource_open3d()

        vdata = GeomVertexData("forest", format, Geom.UH_static)
        vdata.set_num_rows(len(verx))
        print("forest was created")
        vertex = GeomVertexWriter(vdata, 'vertex')
        color  = GeomVertexWriter(vdata, 'color')

        
        for i in range(len(verx)):
            vertex.add_data3f(tuple(verx[i]))
            color.add_data3f(tuple(colr[i]))

        prim = GeomPoints(Geom.UH_static)
        prim.add_next_vertices(len(verx))
        print("prim was created")

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        print("Geaom and primitive were created")
        node = GeomNode('forest')
        node.addGeom(geom)

        print("node was created")
        nodepath = render.attachNewNode(node)
        print("nodepath render was created")

        return nodepath
    # Design a method that obtain the vertex of image using the 




app_dream = Dream_app()
app_dream.run()

