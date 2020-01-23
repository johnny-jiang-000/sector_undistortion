#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <cmath>
#include <chrono>

#define THREAD_NO 6
#define w 38400
#define h 21600
#define l 10800
# define M_PI           3.14159265358979323846  /* pi */



typedef struct _SHM{
	float *map;
	volatile int id;
	float R,Rmin,dr,amax,da;
}SHM;

void *mesh(void* ptr);
pthread_mutex_t mutex=PTHREAD_MUTEX_INITIALIZER;

int count=0;
int n=(int)ceil((float)w/THREAD_NO);
using namespace std::chrono;

int main(){
	
	pthread_t thread[THREAD_NO];
	int iret[THREAD_NO];
	int i;
	high_resolution_clock::time_point start,end;
	SHM data;	
	float *map=(float*)malloc(sizeof(float)*n*THREAD_NO*h*2);	
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


	start=high_resolution_clock::now();
	for(i=0;i<THREAD_NO;i++){
		data.id=i;
		iret[i]=pthread_create(thread+i,NULL,mesh,(void*)&data);
		//printf("iret=%d, id=%d\n",iret[i],data.id);
	}

	for(i=0;i<THREAD_NO;i++)
		pthread_join(thread[i],NULL);
	end=high_resolution_clock::now();
	
	duration<double> time_span=duration_cast<duration<double>>(end-start);

	printf("time elapse: %.2f sec\n",time_span.count());
	printf("p0=(%.2f,%.2f),p1=(%.2f,%.2f)\n",data.map[0],data.map[1],data.map[2*w*h-2],data.map[2*w*h-1]);
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
	++count;
	id=count-1;
	pthread_mutex_unlock(&mutex);

	
	//printf("id=%d,R=%.2f\n",id,data->R);
	for(px=n*id;px<n*(id+1);px++){
		for(py=0;py<h;py++){
			r=data->R-data->dr*py;
			theta=M_PI*0.5+data->amax-data->da*px;
			//printf("r=%.3f,theta=%.3f\n",r,theta);
			data->map[2*(py+px*h)]=r*cos(theta);
			data->map[2*(py+1+px*h)]=r*sin(theta);
			//printf("x_i=%d,x_o=%.3f,y_i=%d,y_o=%.3f\n",px,data->map[2*(py+px*h)],py,data->map[2*(py+1+px*h)]);
		}
	}
}

	

	
	
