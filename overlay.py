import cv2
import numpy as np
import threading
import time

ROW=720
COL=1280
hCOL=COL/2

gamma=5.0
w=640
h=512
l=h*gamma

boundary=[[0,w,ROW-h,ROW],[COL-w,COL,ROW-h,ROW]]

R=np.sqrt((l+h)**2+(0.5*w)**2)
Rmin=np.sqrt(l**2+(0.5*w)**2)
dr=(R-Rmin)/float(h)
w_o=int(0.5*w*R/np.sqrt((0.5*w)**2+l**2))
h_o=int(R-l)
amax=np.arctan((0.5*w)/float(l))
da=amax/float(0.5*w)

coeff=[R,Rmin,dr,w_o,h_o,amax,da,gamma]


print("R=",R," Rmin=",Rmin," dr=",dr," amax=",amax," da=",da)
map=np.zeros((h,w,2))
map_x,map_y=np.full((h,w),-1,dtype=np.float32),np.full((h,w),-1,dtype=np.float32)
output = np.zeros((h,w,3), dtype=np.uint8)
dual_out = np.zeros((ROW,COL,3), dtype=np.uint8)
offset=[[0,0],[0,0]]


def recalc():
    l=h*coeff[7]
    coeff[0]=np.sqrt((l+h)**2+(0.5*w)**2)
    coeff[1]=np.sqrt(l**2+(0.5*w)**2)
    coeff[2]=(coeff[0]-coeff[1])/float(h)
    coeff[3]=int(0.5*w*coeff[0]/np.sqrt((0.5*w)**2+l**2))
    coeff[4]=int(coeff[0]-l)
    coeff[5]=np.arctan((0.5*w)/float(l))
    coeff[6]=coeff[5]/float(0.5*w)

def st_mesh():
    l=h*coeff[7]
    for px in range(w):
        for py in range(h):
            # map_x[py,px]=-1
            # map_y[py,px]=-1
            r=coeff[0]-coeff[2]*py
            theta=np.pi*0.5+coeff[5]-coeff[6]*px
            x=(r*np.cos(theta)+coeff[3])*w/(2.0*coeff[3])
            y=(coeff[4]+l-r*np.sin(theta))*h/coeff[4]
            map_x[int(y),int(x)]=px
            map_y[int(y),int(x)]=py

# def gl_mesh2():
#     dx,dy=1.0/w,1.0/h
#     r_2min=Rmin**2
#     r_2max=R**2
#     theta_min=np.pi/2.0-amax
#     theta_max=np.pi/2.0+amax
#     for i in range(w):
#         for j in range(h):
#             ax,ay=dx*i,dy*j
#             px,py=ax*w_o*2-w_o,h_o+l-ay*h_o
#             r_2=px**2+py**2
#             theta=np.arctan2(py,px+0.00001)
#             if(r_2>r_2min and r_2<r_2max and theta>theta_min and theta<theta_max):
#                 map[j,i,:]=(int((np.pi/2.0+amax-theta)/da),int((R-np.sqrt(r_2))/dr))
#                 # map_x[j,i],map_y[j,i]=(np.pi/2.0+amax-theta)/da,(R-np.sqrt(r_2))/dr
#             else:
#                 map[j,i,:]=(999,999)

# def remap(input,out,map):
#     for i in range(w):
#         for j in range(h):
#             if(map[j,i,0]>w-1 or map[j,i,1]>h-1):
#                 out[j,i,:]=(0,0,0)
#             else:
#                 out[j,i,:]=input[int(map[j,i,1]),int(map[j,i,0]),:]


def concat(inmat,outmat,offset):
    if(offset[0][0]>0 and offset[0][0]<hCOL-w):
        boundary[0][0],boundary[0][1]=offset[0][0],w+offset[0][0]
    if(offset[0][1]<0 and offset[0][1]>h-ROW):
        boundary[0][2],boundary[0][3]=ROW-h+offset[0][1],ROW+offset[0][1]
    if(offset[1][0]<0 and offset[1][0]>w-hCOL):
        boundary[1][0],boundary[1][1]=COL-w+offset[1][0],COL+offset[1][0]
    if(offset[1][1]<0 and offset[1][1]>h-ROW):
        boundary[1][2],boundary[1][3]=ROW-h+offset[1][1],ROW+offset[1][1]



    outmat[boundary[0][2]:boundary[0][3],boundary[0][0]:boundary[0][1],:]=inmat
    outmat[boundary[1][2]:boundary[1][3],boundary[1][0]:boundary[1][1],:]=inmat
    # outmat[567:1079,0:640,:]=inmat


cam=cv2.VideoCapture(0)
# cam=cv2.VideoCapture('My_Capture.avi')
# gl_mesh2()
st_mesh()

# cv2.namedWindow("overlay", cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("overlay",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)


while True:
    _,cam_img=cam.read()
    output=cv2.remap(cam_img,map_x,map_y,interpolation=cv2.INTER_LINEAR)
    # remap(cam_img,output,map)
    concat(output,dual_out,offset)

    cv2.imshow('overlay',dual_out)
    
    keypress=cv2.waitKey(1) & 0xFF
    
    if(keypress-255!=0):
        if keypress==ord(' '):
            break
        elif keypress==ord('w'):
            offset[0][1]-=1
        elif keypress==ord('a'):
            offset[0][0]-=1
        elif keypress==ord('s'):
            offset[0][1]+=1
        elif keypress==ord('d'):
            offset[0][0]+=1

        elif keypress==ord('i'):
            offset[1][1]-=1
        elif keypress==ord('j'):
            offset[1][0]-=1
        elif keypress==ord('k'):
            offset[1][1]+=1
        elif keypress==ord('l'):
            offset[1][0]+=1
        elif keypress==ord('9'):
            coeff[7]+=0.1
            map_x,map_y=np.full((h,w),-1,dtype=np.float32),np.full((h,w),-1,dtype=np.float32)
            recalc()
            st_mesh()
        elif keypress==ord('0'):
            coeff[7]-=0.1
            map_x,map_y=np.full((h,w),-1,dtype=np.float32),np.full((h,w),-1,dtype=np.float32)
            recalc()
            st_mesh()
        else:
            continue
                    

