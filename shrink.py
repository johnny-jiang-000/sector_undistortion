import cv2
import numpy as np



input=cv2.imread('3.jpg')
# irin=cv2.imread('capture2.png')
output=cv2.resize(input,(640,480))
cv2.imwrite('scaled3.png',output)

# H0=np.transpose(np.array([[0.6481,0.1404,0.0],[-0.0334,0.6719,0.0],[120.5052,11.6071,1.0000]]))
# H1=np.transpose(np.array([[0.7751,-0.1410,0.0000],[0.1199,0.3786,0.0000],[49.4882,195.0285,1.0000]]))
# H2=np.transpose(np.array([[0.6796,-0.0258,0.0000],[0.0137,0.7180,0.0],[135.4070,86.5596,1.0000]]))

# homo=cv2.warpPerspective(irin,H2,(640, 480))
# while True:
#     cv2.imshow('homo',homo)
#     cv2.waitKey(1) 