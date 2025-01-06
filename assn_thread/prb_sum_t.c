#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>

int nos[10]={23,12,3,42,23,54,67,32,9,7};

void* routine_sum(void* arg){ //routine with parameter passed in and value returned
    int* index=arg;
    int sum=0;
    for(int i=0;i<5;i++)
    sum+=nos[*index+i];
    *(int*)arg =sum; //void* type casted
    return arg;
}

int main(){
    pthread_t p[2];

    for(int i=0;i<2;i++){
        int* a= malloc(sizeof(int));
        *a = i*5;       // for i=0, *a =0; for i=1, *a=5;
        if(pthread_create(&p[i],NULL,&routine_sum,a)!=0)
        return 1;
    }

    int tot_sum=0;

    for(int i=0;i<2;i++){ //getting return value from routine and joining
        int *s;
        if(pthread_join(p[i],(void**)&s)!=0)
        return 1;
        tot_sum+=*s;
        free(s); // freeeing the allocated memory
    }

    printf("the total sum is %d \n",tot_sum);

}