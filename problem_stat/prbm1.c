#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include <sys/types.h>
#include <sys/wait.h> 

int arr[5]={1,2,3,4};

void* mod_list(){
arr[5]=5;
}

int thread_approach(){
    pthread_t p1;
    if(pthread_create(&p1,NULL,&mod_list,NULL)!=0)
    return 1;

    if(pthread_join(p1,NULL)!=0)
    return 2;

    for(int i=0;i<5;i++)
    printf(" %d ",arr[i]);

}

void process_approach(){
    pid_t f1;
    f1=fork();
    printf("\n");
    if(f1==0)
    {
        mod_list(arr);
        for(int i=0;i<5;i++)
        printf(" %d ",arr[i]);
    }
    wait(NULL);

}

int main(){
    process_approach();
    printf("\n");
    thread_approach();
    return 0;
}