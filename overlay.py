import cv2
import numpy as np

ROW=1080
COL=1920

w=640
h=512
l=h*5

R=np.sqrt((l+h)**2+(0.5*w)**2)
Rmin=np.sqrt(l**2+(0.5*w)**2)
dr=(R-Rmin)/float(h)
w_o=int(0.5*w*R/np.sqrt((0.5*w)**2+l**2))
h_o=int(R-l)
amax=np.arctan((0.5*w)/float(l))
da=amax/float(0.5*w)

print("R=",R," Rmin=",Rmin," dr=",dr," amax=",amax," da=",da)
map=np.zeros((h,w,2))
map_x,map_y=np.full((h,w),-1,dtype=np.float32),np.full((h,w),-1,dtype=np.float32)
output = np.zeros((h,w,3), dtype=np.uint8)
dual_out = np.zeros((ROW,COL,3), dtype=np.uint8)
offset=[[0,0],[0,0]]

def st_mesh():
    for px in range(w):
        for py in range(h):
            r=R-dr*py
            theta=np.pi*0.5+amax-da*px
            x=(r*np.cos(theta)+w_o)*w/(2.0*w_o)
            y=(h_o+l-r*np.sin(theta))*h/h_o
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
    Lx0,Lx1,Ly0,Ly1=offset[0][0],w+offset[0][0],ROW-h+offset[0][1],ROW+offset[0][1]
    Rx0,Rx1,Ry0,Ry1=COL-w+offset[1][0],COL+offset[1][0],ROW-h+offset[1][1],ROW+offset[1][1]


    outmat[Ly0:Ly1,Lx0:Lx1,:]=inmat
    outmat[Ry0:Ry1,Rx0:Rx1,:]=inmat
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
        else:
            continue
                    

