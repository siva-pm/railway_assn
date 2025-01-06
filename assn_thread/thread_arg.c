//create 10 threads, each printing one unique no. from an array
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

int nos[10]={1,2,3,4,5,6,7,8,9,10};

void* routine(void* arg){
    int* index=arg;
    printf("%d ",nos[*index]);
    free(arg); //freeing the allocated space
}

int main(){
     pthread_t th[10];

     for(int i=0;i<10;i++){
     int* a= malloc(sizeof(int)); //need to allocate and pass by reference 
     *a=i;                        //because thread created and doesnt start but i moves to next value.
     if(pthread_create(&th[i],NULL,&routine,&i))
     return 1;
     }
     for(int i=0;i<10;i++)
     if(pthread_join(th[i],NULL));
     return 1;

    return 0;
}