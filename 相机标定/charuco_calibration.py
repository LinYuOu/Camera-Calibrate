
import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
# %matplotlib nbagg
def main(image_path):
    if not os.path.exists(f"{image_path}"): 
        print(f"No such path {image_path}!")
        return
    frame = cv2.imread(f"{image_path}")
    # frame = cv2.resize(frame, (int(frame.shape[0]/2.5),  int(frame.shape[1]/2.5)))

    #frame = cv2.undistort(src = frame, cameraMatrix = mtx, distCoeffs = dist)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow(f'gray{image_path}',gray)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    # aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters =  aruco.DetectorParameters()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, 
                                                        parameters=parameters)
    

    # SUB PIXEL DETECTION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
    for corner in corners:
        cv2.cornerSubPix(gray, corner, winSize = (1,1), zeroZone = (-1,-1), criteria = criteria)
        
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    # len(corners)

    # frame_markers = cv2.resize(frame_markers, (1000,1000))
    # cv2.imshow(f'frame_markers{image_path}',frame_markers)
    cc_name = image_path.split('/')[-1]
    print(cc_name)
    cv2.imwrite(f'./data/CHARUCO_Corner/{cc_name}', frame_markers)

    return ids, corners

datadir = "./data/CHARUCO_new/"
images = np.array([datadir + f for f in os.listdir(datadir) if f.endswith(".jpg") ])
order = np.argsort([int(p.split(".")[-2].split('/')[-1][5:]) for p in images])
images = images[order]
# 记录ids corners
all_markers_ids = []
all_markers_corners = []
for image in images:
    markers_ids, markers_corners = main(image)
    all_markers_ids.append(markers_ids)
    all_markers_corners.append(markers_corners)
cv2.waitKey(0)
cv2.destroyAllWindows()

# # Add local axis on each marker

# size_of_marker =  0.0285 # side lenght of the marker in meter
# rvecs,tvecs,_ = aruco.estimatePoseSingleMarkers(corners, size_of_marker , mtx, dist)

# length_of_axis = 0.05
# imaxis = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
# # imaxis = aruco.drawDetectedCornersCharuco(frame.copy(), corners,ids) 
# # imaxis
# for i in range(len(tvecs)):
#     # imaxis = aruco.drawAxis(imaxis, mtx, dist, rvecs[i], tvecs[i], length_of_axis) 
#     imaxis = cv2.drawFrameAxes(imaxis, mtx, dist, rvecs[i], tvecs[i], length_of_axis) 
#     # imaxis = aruco.drawDetectedCornersCharuco(imaxis, corners) 

# plt.figure()
# plt.imshow(imaxis)
# plt.grid()
# plt.show()