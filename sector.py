import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import threading
from timeit import default_timer as timer

T=4
w=2560
h=1080
l=10800
n=w/T

R=np.sqrt((l+h)**2+(0.5*w)**2)
Rmin=np.sqrt(l**2+(0.5*w)**2)
dr=(R-Rmin)/float(h)
w_o=int(0.5*w*R/np.sqrt((0.5*w)**2+l**2))
h_o=int(R-l)
amax=np.arctan((0.5*w)/float(l))
da=amax/float(0.5*w)

print("R=",R," Rmin=",Rmin," dr=",dr," amax=",amax," da=",da)

map=np.zeros((h,w,2))
out=np.zeros((h_o,w_o*2,4))



class mt_mesh(threading.Thread):
	def __init__(self,id):
		threading.Thread.__init__(self)
		self.id=id
	def run(self):
		mesh(self.id)


def mesh(id):
	for px in range(int(n*id),int(n*(1+id))):
		for py in range(h):
			r=R-dr*py
			theta=np.pi*0.5+amax-da*px
			map[py,px,0]=r*np.cos(theta)
			map[py,px,1]=r*np.sin(theta)

def st_mesh():
	for px in range(w):
		for py in range(h):
			r=R-dr*py
			theta=np.pi*0.5+amax-da*px
			map[py,px,0]=r*np.cos(theta)
			map[py,px,1]=r*np.sin(theta)

start=timer()

#thread_no=[]
#for i in range(T):
#	thread_no.append(mt_mesh(i))

#for t in thread_no:
#	t.start()

#for t in thread_no:
#	t.join()

st_mesh()
end=timer()

print("p0=(",int(map[0,0,0]+w_o),",",int(h_o+l-map[0,0,1]),")","p1=(",int(map[h-1,w-1,0]+w_o),",",int(h_o+l-map[h-1,w-1,1]),")")

raw=mpimg.imread('2020.01.19-01.26.png')

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
