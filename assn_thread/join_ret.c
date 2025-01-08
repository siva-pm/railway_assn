//get a return value from thread_function
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <time.h>

void* roll_dice(){
    int* resu= malloc(sizeof(int)); 
    *resu = (rand() % 6) +1;
    printf("will return %d on address %p \n", *resu,resu);
    //return (void*) resu; //int* returned, void* type casted
    pthread_exit((void*)resu); //usage of pthread_exit fn instead of return
}

int main(){
    int* res;  
    srand(time(NULL));
    pthread_t th;
    if(pthread_create(&th, NULL, &roll_dice, NULL)!=0){ //creating thread for fn roll_dice
        return 1;
    }
    if(pthread_join(th,(void**) &res)!=0){ //return value got from roll_dice as int*, void** type casted to int*
        return 2;
    }
    //pthread_exit(0);               //terminates the program but lets all thread end first
    printf("returned value is %d on address %p \n",*res,res);
    free(res); //deallocate memory
    return 0;
}