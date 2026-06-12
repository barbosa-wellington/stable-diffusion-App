from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import GeomVertexArrayFormat, GeomVertexData, GeomVertexFormat, Geom, GeomNode
from panda3d.core import GeomVertexReader, GeomVertexWriter, GeomPoints

import panda3d_loading_processing as plp

from math import pi, sin, cos


class Dream_app(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        nodepath = self.geom_node()


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
        vertex = GeomVertexWriter(vdata, 'vertex')
        color  = GeomVertexWriter(vdata, 'color')

        
        for i in range(len(verx)):
            vertex.add_data3f(tuple(verx[i]))
            color.add_data3f(tuple(colr[i]))

        prim = GeomPoints(Geom.UH_static)
        prim.add_next_vertices(len(verx))

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode('forest')
        node.addGeom(geom)

        nodepath = render.attachNewNode(node)

    # Design a method that obtain the vertex of image using the 




app_dream = Dream_app()
app_dream.run()

