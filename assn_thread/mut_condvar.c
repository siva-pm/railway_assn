#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

pthread_mutex_t mutex;
pthread_cond_t cond;
int level=0;
int cons_var=30;

void* producer(void* arg){
    pthread_mutex_lock(&mutex);
    level+=10;
    printf("producing...%d\n",level);
    pthread_mutex_unlock(&mutex);
    if(level>cons_var)
        pthread_cond_signal(&cond);
}

void* consumer(void* arg){
    pthread_mutex_lock(&mutex);
    while(level<cons_var){
        pthread_cond_wait(&cond,&mutex);
    }
    level-=cons_var;
    printf("consumed,balance units... %d \n",level);
    pthread_mutex_unlock(&mutex);
}

int main(){
    pthread_t t[5];
    pthread_mutex_init(&mutex,NULL);
    pthread_cond_init(&cond,NULL);

    if(pthread_create(&t[0],NULL,&producer,NULL)!=0)
        perror("failed to create thread");
    if(pthread_create(&t[1],NULL,&producer,NULL)!=0)
        perror("failed to create thread");
    if(pthread_create(&t[2],NULL,&consumer,NULL)!=0)
        perror("failed to create thread");
    if(pthread_create(&t[3],NULL,&producer,NULL)!=0)
        perror("failed to create thread");
    if(pthread_create(&t[4],NULL,&producer,NULL)!=0)
        perror("failed to create thread");
        
    pthread_join(t[0],NULL);
    pthread_join(t[1],NULL);
    pthread_join(t[2],NULL);
    pthread_join(t[3],NULL);
    pthread_join(t[4],NULL);
    

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond);
    return 0;
}

