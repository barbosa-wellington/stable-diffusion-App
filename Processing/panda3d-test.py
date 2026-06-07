# this is a test of 3D images
print('this is a test of 3d working with python and pandas 3d')

# This project is based on Anaconda Python
# to run the code
# C:\users\wellb\anaconda3\python.exe .\3d-project.py

from direct.showbase.ShowBase import ShowBase

app = ShowBase()

#load a simple model for test the graphics
# All models are located at pandas\models folder
model = app.loader.load_model('course2.egg')
model.reparent_to(app.render)
app.run()


# class Myapp(ShowBase):

#     def __init__(self):
#         ShowBase.__init__(self)

#         self.scene = self.loader.loadModel("course2.egg")
#         self.scene.reparentTo(self.render)
#         self.scene.setScale(0.25,0.25,0.25)
#         self.scene.setPos(-8,42,0)
# # sponza.egg

# app = Myapp()
