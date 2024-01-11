import numpy as np
import cv2, PIL, os
from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
# %matplotlib nbagg



def read_chessboards(images):
    """
    Charuco base pose estimation.
    """
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    all_markers_corners_InImage = []
    all_markers_ids = []
    all_markers_corners_InBoard = []
    # all_corners_InBoard = []
    all_corners_InBoard = []
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for i,im in enumerate(images):
        print("=> Processing image {0}".format(im))
        frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        marker_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)
        all_markers_corners_InImage.append(marker_corners)
        all_markers_ids.append(ids)
        markers_corners_InBoard = []

        for id in ids:
            markers_corners_InBoard.append(board.getObjPoints()[id[0]])
        all_markers_corners_InBoard.append(markers_corners_InBoard)
        ''' ChessboardCorners '''
        allCorners.append(cv2.findChessboardCorners(gray, (6, 4))[1])
        all_corners_InBoard.append(board.getChessboardCorners())
        # ''' 插值计算角点 '''
        # if len(marker_corners)>0:
        #     # SUB PIXEL DETECTION
        #     for marker_corner in marker_corners:
        #         cv2.cornerSubPix(gray, marker_corner, 
        #                          winSize = (3,3), 
        #                          zeroZone = (-1,-1), 
        #                          criteria = criteria)
        #     charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(marker_corners, ids, frame, board)
        #     if charuco_retval and len(charuco_corners) >= 6:
        #         print('corners after interpolate', len(charuco_ids))
        #         corner_InBoard = []
        #         for id in charuco_ids:
        #             # print(id)
        #             corner_InBoard.append(board.getChessboardCorners()[id[0]])
        #         allCorners.append(charuco_corners)
        #         all_corners_InBoard.append(corner_InBoard)
        #         allIds.append(charuco_ids)             

    imsize = gray.shape
    # 拼接charuco 和 ChessBoardCorners
    # 1 像素坐标
    all_markers_corners_InImage = np.squeeze(np.array(all_markers_corners_InImage))
    all_markers_corners_InImage_array = all_markers_corners_InImage.reshape(all_markers_corners_InImage.shape[0],
                                            all_markers_corners_InImage.shape[1]*all_markers_corners_InImage.shape[2],
                                            all_markers_corners_InImage.shape[3])
    allCorners_array = np.squeeze(np.array(allCorners))
    concat_corners = np.concatenate((all_markers_corners_InImage_array, allCorners_array),axis=1)
    # 2 棋盘坐标
    all_markers_corners_InBoard = np.array(all_markers_corners_InBoard)
    all_markers_corners_InBoard_array = all_markers_corners_InBoard.reshape(all_markers_corners_InBoard.shape[0],
                                                                    all_markers_corners_InBoard.shape[1]*all_markers_corners_InBoard.shape[2],
                                                                    all_markers_corners_InBoard.shape[3])
    concat_corners_InBoard = np.concatenate((all_markers_corners_InBoard_array, np.array(all_corners_InBoard)) ,axis=1)

    return allCorners, all_corners_InBoard, allIds, imsize, all_markers_corners_InImage, all_markers_ids, all_markers_corners_InBoard, concat_corners, concat_corners_InBoard

if __name__ =="__main__":

    # if not os.path.exists('./workdir/'):
    workdir = "./workdir/"
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    # aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    square_Length,markers_Length =  1., .7
    board = aruco.CharucoBoard((7, 5),square_Length,markers_Length, aruco_dict)
    imboard = board.generateImage((2000, 2000))
    # imboard = board.draw((2000, 2000))
    # cv2.imwrite(workdir + "chessboard.tiff", imboard)
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # plt.imshow(imboard, cmap = mpl.cm.gray, interpolation = "nearest")
    # ax.axis("off")
    # plt.show()

    datadir = "./data/CHARUCO_new/"
    images = np.array([datadir + f for f in os.listdir(datadir) if f.endswith(".jpg") ])

    # order = np.argsort([int(p.split(".")[-2].split("_")[-1]) for p in images])
    order = np.argsort([int(p.split(".")[-2].split('/')[-1]) for p in images])
    images = images[order]
    print(images)

    allCorners,all_corners_InBoard,allIds,imsize,all_markers_corners_InImage,all_markers_ids_InImage,all_markers_corners_InBoard=read_chessboards(images)
    print('len' , len(all_corners_InBoard))
    print('\n shape',  len(all_corners_InBoard))
  