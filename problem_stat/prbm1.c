#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/wait.h> 

int temp=4;
int ind=0;
int arr[6]={1,2,3,4};
pthread_mutex_t mutex;

void* mod_list(){
pthread_mutex_lock(&mutex);
temp++;
ind++;
arr[3+ind]=temp;
pthread_mutex_unlock(&mutex);
return NULL;
}

int thread_approach(){
    pthread_t p1;
    if(pthread_create(&p1,NULL,&mod_list,NULL)!=0)
    return 1;
    
    if(pthread_join(p1,NULL)!=0)
    return 2;

    for(int i=0;i<=3+ind;i++){
    printf("t-%d->",arr[i]);
    fflush(stdout);}
    printf("\n");
}

pid_t process_approach(){
   pid_t f1;
   f1=fork();
   mod_list(arr);
   for(int i=0;i<=3+ind;i++){
   printf("p-%d-%d->",f1,arr[i]); 
   fflush(stdout);}
   printf("\n");
   wait(NULL);
   return f1;
}

int main(){
    pid_t f1;
    pthread_mutex_init(&mutex,NULL);
    
    f1=process_approach();
    printf(" %d \n",getpid());
    thread_approach();
    
    if(f1){
    printf("\nj.d-");
    for(int i=0;i<=3+ind;i++){
    printf("%d->",arr[i]);
    fflush(stdout);}
    printf("\n");
    }
    return 0;
}

//flow:
//process_approach fn is called,
//after fork(), the address space is duplicated
//parent-> 1234, child->1234
//parent or child process starts to run first
//parent-> 12345, child-> 12345
//thread_approach fn is called,
//parent-> 123456, child-> 123456
//here child runs first and parent waits till child gets executed
//after both child and parent processes are done
//the end array will be 123456
//
//observation:
//the changes done to global variable in child process, doesnt reflect in parent process or vice versa.
//both the address spaces are isolated.
//
//the changes done in one/more threads in a process will reflected all around the process.