# this is a test of 3D images
print('this is a test of 3d working with python and pandas 3d')

# This project is based on Anaconda Python
# to run the code
# C:\users\wellb\anaconda3\python.exe .\3d-project.py


# reference source for 3d image in Python
# Creating Realistic 3D Graphics In Python
# https://www.youtube.com/watch?v=9-h-8_jiktY

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeomPoints
import os
import numpy as np
import open3d as o3d


# Loading open3d data
def loading_datasource_open3d():
    """Load the source file using Open3D
        This method will only works if the file .ply was saved as a binary format
    """
    dataset = o3d.io.read_point_cloud('data/test-save.ply')

    vertex_v = np.asarray(dataset[0,1,2])
    color_c = np.asarray(dataset[3, 4])
    
    return [vertex_v, color_c]

# print(help(dataset))

def loading_datasource_python():
    """Method to read the ply file using python IO
    
    This method will only read the file if it was previously saved with flag write_ascii == True
    """

    with open('data/test-save.ply', 'r') as file:

        matrix_vertex_colour = []
        is_header  = True
          
        for i in file:
            if i.strip() == 'end_header':
                is_header = False
                continue

            if is_header:
                continue
            
            parts = i.split()
            fn = (float(parts[0]),float(parts[1]),float(parts[2]),int(parts[3]),int(parts[4]),int(parts[5]))
            # fn = float(i.split()[0]),float(i.split()[1]),float(i.split()[2]),int(i.split()[3]),int(i.split()[4]),int(i.split()[5])
            matrix_vertex_colour.append(fn)

        
        return matrix_vertex_colour

# testing the method based on python reading file
# test = loading_datasource_python()
# print(test[1][0],test[1][3])


# o3d.visualization.draw_geometries([test])
# print(test)

# app = ShowBase()

# #load a simple model for test the graphics
# # All models are located at pandas\models folder
# model = app.loader.load_model('data/course2/course2.egg')
# model.reparent_to(app.render)
# app.run()



# class Myapp(ShowBase):

#     def __init__(self):
#         ShowBase.__init__(self)

#         self.scene = self.loader.loadModel("course2.egg")
#         self.scene.reparentTo(self.render)
#         self.scene.setScale(0.25,0.25,0.25)
#         self.scene.setPos(-8,42,0)
# # sponza.egg

# app = Myapp()
