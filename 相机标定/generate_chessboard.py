import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import numpy as np

def generate_chessboard(filename):
    square_size = 50
    chessboard_size = 8

    # 创建一个空白图像
    image = np.ones((square_size * chessboard_size, square_size * chessboard_size, 3), dtype=np.uint8) * 255

    # 绘制棋盘
    for i in range(chessboard_size):
        for j in range(chessboard_size):
            if (i + j) % 2 == 0:
                color = (0, 0, 0)  # 黑色
            else:
                color = (255, 255, 255)  # 白色

            # 计算方块位置
            x1, y1 = j * square_size, i * square_size
            x2, y2 = x1 + square_size, y1 + square_size

            # 绘制方块
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness=cv2.FILLED)

    # 保存图像
    cv2.imwrite(filename, image)

def generate_Charuco(workdir):
    actual_width_cm = 100  # 实际宽度（厘米）
    actual_height_cm = 70  # 实际高度（厘米）

    desired_ppi = 300  # 目标PPI

    # 将实际尺寸转换为英寸
    actual_width_inches = actual_width_cm * 0.3937
    actual_height_inches = actual_height_cm * 0.3937

    # 计算宽度和高度的像素数
    image_width_pixels = int(actual_width_inches * desired_ppi)
    image_height_pixels = int(actual_height_inches * desired_ppi)
    

    # 创建 ArUco 字典
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

    print('pixel_width_size, pixel_height_size',image_width_pixels, image_height_pixels)

    # 创建 Charuco 棋盘
    board = aruco.CharucoBoard((7, 5), 1, 0.7, aruco_dict)

    # 生成 Charuco 棋盘图像
    imboard = board.generateImage((image_width_pixels, image_height_pixels))

    # 保存图像
    save_path = os.path.join(workdir, "chessboard.png")
    print(save_path)
    cv2.imwrite(save_path, imboard)

    # 显示图像
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.imshow(imboard, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")
    plt.show()


# 生成并保存图像文件
image_filename = "./workdir/Charuco.png"
# 设置工作目录
workdir = "./workdir/"
if not os.path.exists(workdir):
    os.makedirs(workdir)
generate_Charuco(workdir)

print(f"棋盘已保存到图像文件: {image_filename}")
