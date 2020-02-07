import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import threading
from timeit import default_timer as timer

T=4
w=640
h=512
l=512
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
out1=np.zeros((h,w,4))



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
			map[py,px,0]=int(r*np.cos(theta)+w_o)
			map[py,px,1]=int(h_o+l-r*np.sin(theta))

def gl_mesh():
	dx,dy=2.0/w,2.0/h
	u=float(h)/w
	for i in range(w):
		for j in range(h):
			ax,ay=-1+dx*(i+0.5),u-dy*(j+0.5)
			px,py=0.5*w*(1+ax),0.5*h*(u-ay)
			r=R-dr*py
			theta=np.pi*0.5+amax-da*px
			map[j,i,0]=r*np.cos(theta)/w_o
			map[j,i,1]=(r*np.sin(theta)-l-0.5*h_o)/(0.5*h_o)
			print("(",map[j,i,0],",",map[j,i,1],",",ax,",",ay,",",px,",",py,",",int((map[j,i,0]+1)*w_o),",",int((1-map[j,i,1])*h_o/2.0),")","\t")
		print("\n")

def gl_mesh2():
	dx,dy=2.0/w,2.0/h
	u=float(h)/w
	l_gl=float(l)*2/w
	R_gl=np.sqrt((l_gl+2*u)**2+1)
	Rmin_gl=np.sqrt(l_gl**2+1)
	dr_gl=(R_gl-Rmin_gl)/float(h)
	h_o_gl=R_gl-l_gl
	for i in range(w):
		for j in range(h):
			ax,ay=-1+dx*(i+0.5),1-dy*(j+0.5)
			r=R_gl-dr_gl*(0.5+j)
			theta=np.pi*0.5+amax-da*(0.5+i)
			map[j,i,0]=r*np.cos(theta)*w*0.5/w_o
			map[j,i,1]=r*np.sin(theta)-l_gl-0.5*h_o_gl
			print("(",map[j,i,0],",",map[j,i,1],",",ax,",",ay,",",int((map[j,i,0]+1)*w_o),",",int((1-map[j,i,1])*h_o/2.0),")","\t")
		print("\n")

start=timer()

#thread_no=[]
#for i in range(T):
#	thread_no.append(mt_mesh(i))

#for t in thread_no:
#	t.start()

#for t in thread_no:
#	t.join()

# gl_mesh()
# gl_mesh2()
st_mesh()
end=timer()

print("p0=(",map[0,0,0],",",map[0,0,1],")","p1=(",map[h-1,w-1,0],",",map[h-1,w-1,1],")")

raw=mpimg.imread('2020.01.19-01.26.png')

for px in range(w):
    for py in range(h):
        x_o=int(map[py,px,0])
        y_o=int(map[py,px,1])
        out[y_o,x_o,:]=raw[py,px,:]
		# x_o=int(map[py,px,0]*(0.5*w/w_o))
		# y_o=int(map[py,px,1]*(h/h_o))
        # out1[y_o,x_o,:]=raw[py,px,:]



fig,ax=plt.subplots(2,1)
ax[0].imshow(raw)
ax[1].imshow(out)
plt.show()

print("time elapse: ",end-start)
