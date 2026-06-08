# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# import the necessary labraries
import open3d as o3d
import copy

#load data in variables
pcd = o3d.io.read_point_cloud('data/bun_zipper_res2.ply')
# pcd_original = o3d.io.read_point_cloud('dragon_stand/dragonStandRight_336.ply')
forest = o3d.io.read_image('data/forest-scene.png')
forest_depth = o3d.io.read_image('data/image.png')

# print('This is the original image')
# print(forest)

# print('This is the image depth')
# print(forest_depth)


# method to visualize the image on a 3D view
def generate_3D_view(img1,img2,):

    # creating a RGBD image that combines both original and depth image for a 3d visualization
    forest_RBGD = o3d.geometry.RGBDImage.create_from_color_and_depth(img1, img2,convert_rgb_to_intensity=False)
    print(forest_RBGD)

    forest_camera = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.Kinect2DepthCameraDefault)

    # creating from Pointcloud
    forest_pointcloud = o3d.geometry.PointCloud.create_from_rgbd_image(forest_RBGD,forest_camera)

    o3d.visualization.draw_geometries([forest_pointcloud])

generate_3D_view(forest, forest_depth)
# #visualization of the data
# o3d.visualization.draw_geometries([pcd])

# #combining both models
# #o3d.visualization.draw_geometries([pcd, pcd1])


# # downsample group points
# downsample_pcd = pcd_original.voxel_down_sample(voxel_size=0.01)
# #o3d.visualization.draw_geometries([pcd])

# downsample_pcd.translate([0.15, 0, 0])

# #paint them different colours to easily spot the difference
# pcd_original.paint_uniform_color([0.1,0.7,0.1])
# downsample_pcd.paint_uniform_color([0.1,0.1,0.7])

# #o3d.visualization.draw_geometries([pcd_original,downsample_pcd])



# # Computes how surfaces face to allow realistic lighting
# downsample_pcd.estimate_normals(
#     search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
# )
# o3d.visualization.draw_geometries([downsample_pcd], point_show_normal=True)
