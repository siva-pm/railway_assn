#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

void* routine(){
    printf("routine test...%d\n",getpid());
    sleep(1);
    printf("test complete...%d\n",getpid());
}

int main()
{
    pthread_t p1,p2;

    if(pthread_create(&p1,NULL,&routine,NULL))
    return 1;
    if(pthread_create(&p2,NULL,&routine,NULL))
    return 2;
    
    if(pthread_join(p1,NULL))
    return 3;
    if(pthread_join(p2,NULL))
    return 4;
    
    return 0;
}