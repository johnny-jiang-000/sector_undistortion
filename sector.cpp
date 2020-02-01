#ifdef _WIN32
	#define HAVE_STRUCT_TIMESPEC
#endif
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <cmath>
#include <chrono>

#define THREAD_NO 16
#define w 38400
#define h 21600
#define l 10800
#define M_PI           3.14159265358979323846  /* pi */

using namespace std::chrono;

typedef struct _SHM{
	float *map;
	int id,T,n,whalf_o,h_o;
	float R,Rmin,dr,amax,da;
}SHM;

void *mesh(void* ptr);
pthread_mutex_t mutex=PTHREAD_MUTEX_INITIALIZER;

int count=0;


int main(int argc,char *argv[]){	
	int i;
	high_resolution_clock::time_point start,end;
	SHM data;	
	data.T=THREAD_NO;
	if(argc>1)
		data.T=atoi(argv[1]);
	printf("thread number=%d\n",data.T);
	pthread_t *thread=new pthread_t[data.T];
	
	int *iret=new int[data.T];
	data.n=(int)ceil((float)w/data.T);
	float *map=(float*)malloc(sizeof(float)*data.n*data.T*h*2);	
	data.map=map;
		
	data.R=sqrt((l+h)*(l+h)+(0.5*w)*(0.5*w));
	printf("R=%.2f\n",data.R);
	data.Rmin=sqrt(l*l+(0.5*w)*(0.5*w));
	printf("Rmin=%.2f\n",data.Rmin);
	data.dr=(data.R-data.Rmin)/h;
	printf("dr=%.2f\n",data.dr);
	data.amax=atan((0.5*w)/l);
	printf("amax=%.2f\n",data.amax);
	data.da=data.amax/(0.5*w);
	printf("da=%.8f\n",data.da);

	data.whalf_o=(int)(0.5*w*data.R/sqrt((0.5*w)*(0.5*w)+l*l));
	data.h_o=(int)(data.R-l);
	printf("output size=(%d,%d)\n",data.whalf_o*2,data.h_o);


	start=high_resolution_clock::now();
	for(i=0;i<data.T;i++){
		data.id=i;
		iret[i]=pthread_create(thread+i,NULL,mesh,(void*)&data);
		//printf("iret=%d, id=%d\n",iret[i],data.id);
	}

	for(i=0;i<data.T;i++)
		pthread_join(thread[i],NULL);
	end=high_resolution_clock::now();
	
	duration<double> time_span=duration_cast<duration<double>>(end-start);

	printf("time elapse: %.2f sec\n",time_span.count());
	printf("p0=(%d,%d),p1=(%d,%d)\n",(int)(data.map[0]+data.whalf_o),(int)(data.h_o+l-data.map[1]),(int)(data.map[2*w*h-2]+data.whalf_o),(int)(data.h_o+l-data.map[2*w*h-1]));

	delete[] thread;
	delete[] iret;
	return 0;
}

void *mesh(void* ptr){
	int px,py;
	int id;
	double r,theta;
	//printf("thread number %ld \n",pthread_self());
	
	SHM *data=(SHM*)ptr;
	//id=data->id;
	
	pthread_mutex_lock(&mutex);
	id=count;
	++count;
	pthread_mutex_unlock(&mutex);

	
	//printf("id=%d,R=%.2f\n",id,data->R);
	for(px=data->n*id;px<data->n*(id+1);px++){
		for(py=0;py<h;py++){
			r=data->R-data->dr*(py+0.5);
			theta=M_PI*0.5+data->amax-data->da*(px+0.5);
			//printf("r=%.3f,theta=%.3f\n",r,theta);
			data->map[2*(py+px*h)]=r*cos(theta);
			data->map[2*(py+px*h)+1]=r*sin(theta);
			//printf("x_i=%d,x_o=%.3f,y_i=%d,y_o=%.3f\n",px,data->map[2*(py+px*h)],py,data->map[2*(py+1+px*h)]);
		}
	}
	return nullptr;
}

	

	
	
