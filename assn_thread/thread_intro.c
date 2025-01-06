#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

int x=2;

void *routine1(){
    x++;
    sleep(1);
    printf(" %d \n",x);   
}

void *routine2(){
    sleep(1);
    printf(" %d \n",x);
}

int main(){
    pthread_t p1,p2;

    if(pthread_create(&p1,NULL,&routine1,NULL))
    return 1;
    if(pthread_create(&p2,NULL,&routine2,NULL))
    return 2;

    if(pthread_join(p1,NULL))
    return 3;
    if(pthread_join(p2,NULL))
    return 4;
    
    return 0;
}