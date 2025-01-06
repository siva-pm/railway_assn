#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

int x;
pthread_mutex_t mutex; //usage of mutex to avoid race conditions

void* routine(){
    for(int i=0;i<10000000;i++){   //simulate a large iteration
        pthread_mutex_lock(&mutex); //used to check and lock mutex
        x++;
        pthread_mutex_unlock(&mutex); //used to unlock mutex
    }
}

int main(){
    pthread_t p1, p2, p3; //declare threads
    pthread_mutex_init(&mutex,NULL); //initiate mutex
                                                                
    if(pthread_create(&p1,NULL,&routine,NULL)!=0)           //create multiple threads
    return 1;
    if(pthread_create(&p2,NULL,&routine,NULL)!=0)
    return 2;
    if(pthread_create(&p3,NULL,&routine,NULL)!=0)
    return 3;

    if(pthread_join(p1,NULL)!=0)                    //join threads
    return 4;
    if(pthread_join(p2,NULL)!=0)
    return 5;
    if(pthread_join(p3,NULL)!=0)
    return 6;

    printf("x= %d \n",x);
    return 0;    
}