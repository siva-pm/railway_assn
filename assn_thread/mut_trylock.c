#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
pthread_mutex_t mutex;
void* routine(void* arg)
{   
    //int a=;
    if(pthread_mutex_trylock(&mutex)==0){ //try lock doesnt wait to lock and returns 0/
        printf("locked in \n");
        sleep(1);
        pthread_mutex_unlock(&mutex);
    }
    else {
       printf("cant lock\n");
    }

    
}


int main(){
    pthread_t p[4];
    pthread_mutex_init(&mutex,NULL);
    for(int i=0;i<4;i++){
        pthread_create(&p[i],NULL,&routine,NULL);
    }

    for(int i=0;i<4;i++){
        pthread_join(p[i],NULL);
    }
    pthread_mutex_destroy(&mutex);
    return 0;
}