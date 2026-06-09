# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# reference source for 3d image in Python
# Python programming for 3D Data
# https://www.youtube.com/watch?v=h2QiptJYX6c


# import the necessary labraries
import open3d as o3d
import numpy as np
import cv2

#load data in variables
pcd = o3d.io.read_point_cloud('data/bun_zipper_res2.ply')
# pcd_original = o3d.io.read_point_cloud('dragon_stand/dragonStandRight_336.ply')
img_o = o3d.io.read_image('data/forest-scene.png')
img_d = o3d.io.read_image('data/forest-scene-image.png')



color_np = np.asarray(img_o)
depth_np = np.asarray(img_d)
h, w = color_np.shape[:2]

depth_resized = cv2.resize(depth_np, (w, h))
img_d = o3d.geometry.Image(depth_resized)

# method to visualize the image on a 3D view
def generate_3D_view(color_img1 : o3d.geometry.Image , depth_img2: o3d.geometry.Image) -> o3d.geometry.PointCloud:
    """ Method that combines different techniques of the Open3D library to generate a 3D view of a given assest."""

    # generate a RGBD image that join an original and indepth image
    # geometry.RGBDImage.create_from_color_and_depth(color_img1, depth_img2,convert_rgb_to_intensity=False)
    rbgd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_img1, depth_img2,depth_scale=255.0, depth_trunc=1.0,convert_rgb_to_intensity=False)
    # print(rbgd_image)

    # calling the ENUM parameter of the class PinholeCamera to calculate camera angle for a vision 3D space
    # (o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
    camera_image = o3d.camera.PinholeCameraIntrinsic(width=w, height=h,fx=w * 0.7, fy=w * 0.7,cx=w/2,cy=h/2)
    
    # creating a Pointcloud of the image by using the new rbgd and the camera for a tridimensional visualization
    pointcloud_image = o3d.geometry.PointCloud.create_from_rgbd_image(rbgd_image,camera_image)

    # removes isolated noisy points that cause the fold
    pointcloud_image, _ = pointcloud_image.remove_statistical_outlier(
        nb_neighbors=20,
        std_ratio=2.0
    )
    pointcloud_image.transform([[1,0,0,0],
                             [0,-1,0,0],
                             [0,0,-1,0],
                             [0,0,0,1]])
    # visualize the new image on a 3D view
    view_3d = o3d.visualization.draw_geometries([pointcloud_image])
    
    return pointcloud_image

generate_3D_view(img_o, img_d)
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
