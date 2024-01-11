import cv2
import os
# 打开摄像头
cap = cv2.VideoCapture(0)  # 参数0表示使用默认摄像头，如果有多个摄像头，可以尝试使用1、2、3，以此类推

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Could not open camera.")
    cap.release()
    exit()

# 创建窗口
cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

i = 0
if not os.path.exists('photos'):
    os.makedirs('photos')
while True:
    # 读取一帧画面
    ret, frame = cap.read()

    # 检查帧是否成功读取
    if not ret:
        print("Error: Could not read frame.")
        break

    # 在窗口中显示实时画面
    cv2.imshow("Camera", frame)

    # 检测按键，按下 ESC 键退出循环
    key = cv2.waitKey(1)
    if key == 27:  # ASCII码中27表示 ESC 键
        break
    elif key == ord(' '):
        # 保存照片
        cv2.imwrite(f"photos/photo{i}.jpg", frame)
        i+=1
        print("Photo taken!")

# 关闭窗口和摄像头
cv2.destroyAllWindows()
cap.release()
