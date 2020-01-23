import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import numpy as np
import threading
from timeit import default_timer as timer

T=8
w=425
h=425
l=200

R=np.sqrt((l+h)**2+(0.5*w)**2)
Rmin=np.sqrt(l**2+(0.5*w)**2)
dr=(R-Rmin)/float(h)
w_o=int(0.5*w*R/np.sqrt((0.5*w)**2+l**2))
h_o=int(R-l)
amax=np.arctan((0.5*w)/float(l))
da=amax/float(0.5*w)


map=np.zeros((h,w,2))
out=np.zeros((h_o,w_o*2,4))

start=timer()
for px in range(w):
    for py in range(h):
        r=R-dr*py
        # alpha=
        # r=np.sqrt((px-0.5*w)**2+(h+l-py)**2)
        # arc=2*amax*np.sqrt((l-py)**2**2+())
        # alpha=np.arctan((px-0.5*w)/float(h+l-py))
        theta=np.pi*0.5+amax-da*px
        # if(alpha<0):
        #     theta=np.pi+alpha
        
        map[py,px,0]=r*np.cos(theta)
        map[py,px,1]=r*np.sin(theta)

end=timer()

with cbook.get_sample_data('C://Users//autor//Desktop//py_playground//chess.png') as image_file:
    raw=plt.imread(image_file)

for px in range(w):
    for py in range(h):
        x_o=int(map[py,px,0]+w_o)
        y_o=int(h_o+l-map[py,px,1])
        out[y_o,x_o,:]=raw[py,px,:]



fig,ax=plt.subplots(2,1)
ax[0].imshow(raw)
ax[1].imshow(out)
plt.show()

print("time elapse: ",end-start)